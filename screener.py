"""
BSE / NSE Stock Screener — Nov 9 Week Investment Shortlist
==========================================================
All indicators computed manually with pandas/numpy — no numba dependency.
Works with Python 3.14+.

Indicators: RSI, MACD, EMA(20/50), Supertrend(ATR), Bollinger Bands, Volume
Fundamental: Quarterly Revenue & Profit QoQ growth (via yfinance)

Usage:
    python screener.py              # Kite Connect mode (live NSE data)
    python screener.py --free-mode  # yfinance fallback (slower, free, no API key)
"""

import sys
import os
import time
import argparse
import datetime
import warnings

import numpy as np
import pandas as pd
from tqdm import tqdm

warnings.filterwarnings("ignore")

# ── Parse CLI args ─────────────────────────────────────────────────────────────
parser = argparse.ArgumentParser()
parser.add_argument("--free-mode", action="store_true",
                    help="Use yfinance instead of Kite Connect (no API key needed)")
args = parser.parse_args()
FREE_MODE = args.free_mode

from config import (
    API_KEY, MAX_PRICE, MIN_PRICE, MIN_VOLUME,
    RSI_PERIOD, RSI_OVERSOLD, RSI_OVERBOUGHT,
    EMA_SHORT, EMA_LONG, ATR_PERIOD, SUPERTREND_MULT,
    MACD_FAST, MACD_SLOW, MACD_SIGNAL,
    BBANDS_PERIOD, BBANDS_STD,
    WEIGHTS, LOOKBACK_DAYS, OUTPUT_FILE, TOP_N_STOCKS
)


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 1 — CUSTOM TECHNICAL INDICATORS (pure pandas/numpy, no pandas-ta)
# ══════════════════════════════════════════════════════════════════════════════

def calc_rsi(close: pd.Series, period: int = 14) -> pd.Series:
    delta  = close.diff()
    gain   = delta.clip(lower=0)
    loss   = -delta.clip(upper=0)
    avg_g  = gain.ewm(com=period - 1, min_periods=period).mean()
    avg_l  = loss.ewm(com=period - 1, min_periods=period).mean()
    rs     = avg_g / avg_l.replace(0, np.nan)
    return 100 - (100 / (1 + rs))


def calc_ema(close: pd.Series, period: int) -> pd.Series:
    return close.ewm(span=period, adjust=False).mean()


def calc_macd(close: pd.Series,
              fast: int = 12, slow: int = 26, signal: int = 9
             ) -> tuple[pd.Series, pd.Series, pd.Series]:
    ema_fast   = calc_ema(close, fast)
    ema_slow   = calc_ema(close, slow)
    macd_line  = ema_fast - ema_slow
    signal_line = calc_ema(macd_line, signal)
    histogram  = macd_line - signal_line
    return macd_line, signal_line, histogram


def calc_atr(high: pd.Series, low: pd.Series, close: pd.Series,
             period: int = 14) -> pd.Series:
    prev_close = close.shift(1)
    tr = pd.concat([
        high - low,
        (high - prev_close).abs(),
        (low  - prev_close).abs()
    ], axis=1).max(axis=1)
    return tr.ewm(com=period - 1, min_periods=period).mean()


def calc_supertrend(high: pd.Series, low: pd.Series, close: pd.Series,
                    period: int = 14, mult: float = 3.0
                   ) -> tuple[pd.Series, pd.Series]:
    """
    Returns (supertrend_line, direction) where direction = +1 (bullish) / -1 (bearish).
    """
    atr = calc_atr(high, low, close, period)
    hl2 = (high + low) / 2

    upper_band = hl2 + mult * atr
    lower_band = hl2 - mult * atr

    supertrend = pd.Series(np.nan, index=close.index)
    direction  = pd.Series(1,      index=close.index, dtype=int)

    for i in range(1, len(close)):
        # Lower band: only move up, never down
        if lower_band.iloc[i] > lower_band.iloc[i - 1] or close.iloc[i - 1] < lower_band.iloc[i - 1]:
            lb = lower_band.iloc[i]
        else:
            lb = lower_band.iloc[i - 1]

        # Upper band: only move down, never up
        if upper_band.iloc[i] < upper_band.iloc[i - 1] or close.iloc[i - 1] > upper_band.iloc[i - 1]:
            ub = upper_band.iloc[i]
        else:
            ub = upper_band.iloc[i - 1]

        lower_band.iloc[i] = lb
        upper_band.iloc[i] = ub

        prev_st  = supertrend.iloc[i - 1]
        prev_dir = direction.iloc[i - 1]

        if np.isnan(prev_st):
            prev_st = ub

        if prev_st == upper_band.iloc[i - 1]:   # was bearish
            if close.iloc[i] > ub:
                direction.iloc[i] = 1
                supertrend.iloc[i] = lb
            else:
                direction.iloc[i] = -1
                supertrend.iloc[i] = ub
        else:                                     # was bullish
            if close.iloc[i] < lb:
                direction.iloc[i] = -1
                supertrend.iloc[i] = ub
            else:
                direction.iloc[i] = 1
                supertrend.iloc[i] = lb

    return supertrend, direction


def calc_bbands(close: pd.Series,
                period: int = 20, std_dev: float = 2.0
               ) -> tuple[pd.Series, pd.Series, pd.Series]:
    mid   = close.rolling(period).mean()
    std   = close.rolling(period).std()
    upper = mid + std_dev * std
    lower = mid - std_dev * std
    return lower, mid, upper


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 2 — DATA FETCHING
# ══════════════════════════════════════════════════════════════════════════════

def get_nse_symbols_kite(kite) -> list[dict]:
    instruments = kite.instruments("NSE")
    return [i for i in instruments if i["instrument_type"] == "EQ"]


def get_nse_symbols_free() -> list[dict]:
    """Download full NSE equity list from NSE's public CSV."""
    import requests
    csv_url = "https://archives.nseindia.com/content/equities/EQUITY_L.csv"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        resp = requests.get(csv_url, headers=headers, timeout=15)
        from io import StringIO
        df = pd.read_csv(StringIO(resp.text))
        df.columns = [c.strip() for c in df.columns]
        return [
            {"tradingsymbol": str(row["SYMBOL"]).strip(),
             "name":          str(row["NAME OF COMPANY"]).strip()}
            for _, row in df.iterrows()
        ]
    except Exception as e:
        print(f"⚠️  Could not fetch NSE list from archives: {e}")
        print("    Falling back to a small sample list for testing...")
        # Minimal fallback sample so the script doesn't crash
        return [
            {"tradingsymbol": s, "name": s} for s in [
                "RELIANCE","TCS","INFY","HDFCBANK","ICICIBANK","WIPRO","AXISBANK",
                "SBIN","BAJFINANCE","KOTAKBANK","LT","HINDUNILVR","MARUTI","TITAN",
                "NESTLEIND","ULTRACEMCO","SUNPHARMA","DRREDDY","CIPLA","DIVISLAB",
                "TECHM","HCLTECH","POWERGRID","NTPC","ONGC","COALINDIA","BPCL",
                "IOCL","GAIL","TATAPOWER","ADANIPORTS","ADANIENT","JSWSTEEL","SAIL",
                "TATASTEEL","HINDALCO","VEDL","NMDC","MOIL","NATIONALUM",
                "IRCTC","RECLTD","PFC","CANBK","BANKBARODA","UNIONBANK","PNB",
                "IDEA","RCOM","YESBANK","IDFCFIRSTB","FEDERALBNK","KARURVYSYA",
                "ESCORTS","ASHOKLEY","TATAMOTOR","M&M","BAJAJ-AUTO","TVSMOTORS",
            ]
        ]


def fetch_ohlcv_kite(kite, instrument_token: int,
                     days: int = LOOKBACK_DAYS) -> pd.DataFrame:
    end   = datetime.date.today()
    start = end - datetime.timedelta(days=days)
    try:
        data = kite.historical_data(instrument_token, start, end, "day", continuous=False)
        df   = pd.DataFrame(data).set_index("date")
        return df
    except Exception:
        return pd.DataFrame()


def fetch_ohlcv_free(symbol: str, days: int = LOOKBACK_DAYS) -> pd.DataFrame:
    import yfinance as yf
    end   = datetime.date.today()
    start = end - datetime.timedelta(days=days)
    try:
        df = yf.Ticker(f"{symbol}.NS").history(start=str(start), end=str(end))
        df.columns = [c.lower() for c in df.columns]
        # yfinance returns timezone-aware index; strip tz for consistency
        if hasattr(df.index, "tz") and df.index.tz is not None:
            df.index = df.index.tz_localize(None)
        return df
    except Exception:
        return pd.DataFrame()


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 3 — TECHNICAL ANALYSIS (all in-house, no pandas-ta)
# ══════════════════════════════════════════════════════════════════════════════

def compute_technicals(df: pd.DataFrame) -> dict | None:
    if df is None or len(df) < 60:
        return None

    close  = df["close"].astype(float)
    high   = df["high"].astype(float)
    low    = df["low"].astype(float)
    volume = df["volume"].astype(float)

    result = {}

    # ── Current price ──────────────────────────────────────────────────────────
    result["price"] = round(float(close.iloc[-1]), 2)
    if not (MIN_PRICE <= result["price"] <= MAX_PRICE):
        return None

    # ── RSI ───────────────────────────────────────────────────────────────────
    rsi_series = calc_rsi(close, RSI_PERIOD)
    rsi_val    = float(rsi_series.iloc[-1]) if not rsi_series.empty else 50.0
    if np.isnan(rsi_val):
        rsi_val = 50.0
    result["rsi"] = round(rsi_val, 2)

    if rsi_val < RSI_OVERSOLD:
        rsi_score = 100
    elif rsi_val < 55:
        rsi_score = 75
    elif rsi_val < RSI_OVERBOUGHT:
        rsi_score = 40
    else:
        rsi_score = 0
    result["rsi_score"] = rsi_score

    # ── MACD ──────────────────────────────────────────────────────────────────
    macd_line, sig_line, histogram = calc_macd(close, MACD_FAST, MACD_SLOW, MACD_SIGNAL)
    if len(histogram.dropna()) >= 2:
        h_now  = float(histogram.iloc[-1])
        h_prev = float(histogram.iloc[-2])
        result["macd"]     = round(float(macd_line.iloc[-1]), 4)
        result["macd_sig"] = round(float(sig_line.iloc[-1]), 4)

        if h_now > 0 and h_prev <= 0:
            macd_score = 100   # Fresh bullish crossover
        elif h_now > 0:
            macd_score = 70    # Bullish momentum continuing
        elif h_now > h_prev:
            macd_score = 40    # Histogram shrinking (approaching crossover)
        else:
            macd_score = 10
    else:
        macd_score = 50
        result["macd"] = result["macd_sig"] = None
    result["macd_score"] = macd_score

    # ── EMA 20 / 50 ───────────────────────────────────────────────────────────
    ema20 = calc_ema(close, EMA_SHORT)
    ema50 = calc_ema(close, EMA_LONG)
    e20   = float(ema20.iloc[-1])
    e50   = float(ema50.iloc[-1])
    price = result["price"]
    result["ema20"] = round(e20, 2)
    result["ema50"] = round(e50, 2)

    if price > e20 > e50:
        ema_score = 100
    elif price > e20 and e20 < e50:
        ema_score = 60
    elif price < e20:
        ema_score = 20
    else:
        ema_score = 40
    result["ema_score"] = ema_score

    # ── Supertrend ────────────────────────────────────────────────────────────
    try:
        st_line, st_dir = calc_supertrend(high, low, close, ATR_PERIOD, SUPERTREND_MULT)
        st_direction     = int(st_dir.iloc[-1])
        result["supertrend"]       = "BULLISH" if st_direction == 1 else "BEARISH"
        result["supertrend_score"] = 100 if st_direction == 1 else 0
    except Exception:
        result["supertrend"]       = "NEUTRAL"
        result["supertrend_score"] = 50

    # ── Volume Surge ──────────────────────────────────────────────────────────
    avg_vol  = float(volume.tail(20).mean())
    last_vol = float(volume.iloc[-1])
    result["avg_volume"]  = int(avg_vol)
    result["last_volume"] = int(last_vol)

    if avg_vol < MIN_VOLUME:
        return None   # Too illiquid

    vol_ratio = last_vol / avg_vol if avg_vol > 0 else 1.0
    if vol_ratio >= 2.0:
        volume_score = 100
    elif vol_ratio >= 1.5:
        volume_score = 80
    elif vol_ratio >= 1.0:
        volume_score = 50
    else:
        volume_score = 20
    result["volume_score"] = volume_score

    # ── Bollinger Bands ────────────────────────────────────────────────────────
    bb_lower, bb_mid, bb_upper = calc_bbands(close, BBANDS_PERIOD, BBANDS_STD)
    bbl = float(bb_lower.iloc[-1])
    bbu = float(bb_upper.iloc[-1])
    result["bb_lower"]  = round(bbl, 2)
    result["bb_upper"]  = round(bbu, 2)
    if not np.isnan(bbl) and price <= bbl * 1.02:
        result["bb_signal"] = "Near Lower Band (Potential Buy)"
    elif not np.isnan(bbu) and price >= bbu * 0.98:
        result["bb_signal"] = "Near Upper Band (Caution)"
    else:
        result["bb_signal"] = "Mid Band"

    # ── 52-Week High / Low ─────────────────────────────────────────────────────
    history_252 = close.tail(252)
    result["52w_high"] = round(float(history_252.max()), 2)
    result["52w_low"]  = round(float(history_252.min()), 2)
    if result["52w_low"] > 0:
        result["pct_from_52w_low"] = round(
            (price - result["52w_low"]) / result["52w_low"] * 100, 2
        )
    else:
        result["pct_from_52w_low"] = 0.0

    # ── 1-Week Momentum ────────────────────────────────────────────────────────
    if len(close) >= 6:
        result["1w_change_pct"] = round(
            (close.iloc[-1] - close.iloc[-6]) / close.iloc[-6] * 100, 2
        )
    else:
        result["1w_change_pct"] = 0.0

    return result


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 4 — QUARTERLY FUNDAMENTAL SCORE (via yfinance — always free)
# ══════════════════════════════════════════════════════════════════════════════

def quarterly_score(symbol: str) -> tuple[int, dict]:
    try:
        import yfinance as yf
        ticker = yf.Ticker(f"{symbol}.NS")
        qi     = ticker.quarterly_income_stmt

        score   = 50
        details = {}

        if qi is not None and not qi.empty and qi.shape[1] >= 2:
            rev_growth = ni_growth = 0.0

            if "Total Revenue" in qi.index:
                rev_q1 = float(qi.loc["Total Revenue"].iloc[0])
                rev_q2 = float(qi.loc["Total Revenue"].iloc[1])
                if rev_q2 != 0:
                    rev_growth = (rev_q1 - rev_q2) / abs(rev_q2) * 100
                details["rev_qoq_pct"] = round(rev_growth, 2)

            if "Net Income" in qi.index:
                ni_q1 = float(qi.loc["Net Income"].iloc[0])
                ni_q2 = float(qi.loc["Net Income"].iloc[1])
                if ni_q2 != 0:
                    ni_growth = (ni_q1 - ni_q2) / abs(ni_q2) * 100
                details["profit_qoq_pct"] = round(ni_growth, 2)

            avg_growth = (rev_growth + ni_growth) / 2
            if avg_growth > 20:    score = 100
            elif avg_growth > 10:  score = 85
            elif avg_growth > 5:   score = 70
            elif avg_growth > 0:   score = 55
            elif avg_growth > -5:  score = 35
            else:                  score = 10

        return score, details

    except Exception:
        return 50, {}


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 5 — COMPOSITE SCORE
# ══════════════════════════════════════════════════════════════════════════════

def composite_score(tech: dict, q_score: int) -> float:
    total = 0.0
    for key, weight in WEIGHTS.items():
        if key == "quarterly_score":
            total += q_score * weight / 100
        else:
            total += tech.get(key, 50) * weight / 100
    return round(total, 2)


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 6 — MAIN SCREENING LOOP
# ══════════════════════════════════════════════════════════════════════════════

def main():
    print("\n" + "═" * 65)
    print("  📈  BSE / NSE SWING TRADE SCREENER — Week of Nov 9, 2026")
    print("═" * 65)
    print(f"  Mode    : {'Free (yfinance)' if FREE_MODE else 'Kite Connect'}")
    print(f"  Filter  : Price ₹{MIN_PRICE}–₹{MAX_PRICE}  |  Min Vol {MIN_VOLUME:,}")
    print("═" * 65 + "\n")

    # ── Set up data source ─────────────────────────────────────────────────────
    if FREE_MODE:
        kite        = None
        instruments = get_nse_symbols_free()
        print(f"📋  Found {len(instruments):,} NSE symbols\n")
    else:
        token_file = ".access_token"
        if not os.path.exists(token_file):
            print("❌  No access token found. Run:  python generate_token.py")
            sys.exit(1)

        from kiteconnect import KiteConnect
        kite = KiteConnect(api_key=API_KEY)
        with open(token_file) as f:
            kite.set_access_token(f.read().strip())

        instruments = get_nse_symbols_kite(kite)
        print(f"📋  Found {len(instruments):,} NSE equity instruments\n")

    results = []
    skipped = 0

    for inst in tqdm(instruments, desc="Scanning stocks"):
        symbol = inst["tradingsymbol"]
        name   = inst.get("name", symbol)

        try:
            # Fetch OHLCV
            if FREE_MODE:
                df = fetch_ohlcv_free(symbol)
            else:
                df = fetch_ohlcv_kite(kite, inst["instrument_token"])

            if df is None or df.empty:
                skipped += 1
                continue

            # Technical signals
            tech = compute_technicals(df)
            if tech is None:
                skipped += 1
                continue

            # Quarterly fundamentals (always via yfinance)
            q_score, q_details = quarterly_score(symbol)

            # Composite score
            score = composite_score(tech, q_score)

            results.append({
                "Symbol":        symbol,
                "Company":       name,
                "Score":         score,
                "Price (₹)":    tech["price"],
                "RSI":           tech["rsi"],
                "MACD Signal":   "BUY"     if tech.get("macd_score", 0) >= 70 else "SELL/HOLD",
                "EMA Trend":     "BULLISH" if tech.get("ema_score",  0) >= 75 else "BEARISH",
                "Supertrend":    tech.get("supertrend", "N/A"),
                "BB Signal":     tech.get("bb_signal",  "N/A"),
                "Vol Surge":     f"{tech['last_volume'] / tech['avg_volume']:.1f}×"
                                 if tech["avg_volume"] > 0 else "N/A",
                "1W Change%":    tech.get("1w_change_pct", 0),
                "52W Low%":      tech.get("pct_from_52w_low", 0),
                "Rev QoQ%":      q_details.get("rev_qoq_pct",    "N/A"),
                "Profit QoQ%":   q_details.get("profit_qoq_pct", "N/A"),
                "Avg Volume":    tech["avg_volume"],
                "52W High":      tech.get("52w_high"),
                "52W Low":       tech.get("52w_low"),
                "EMA20":         tech.get("ema20"),
                "EMA50":         tech.get("ema50"),
            })

            time.sleep(0.3 if FREE_MODE else 0.1)

        except Exception:
            skipped += 1
            continue

    # ── Sort and display results ───────────────────────────────────────────────
    if not results:
        print("\n⚠️  No stocks passed the filters. Try relaxing constraints in config.py.")
        return

    df_results = (
        pd.DataFrame(results)
          .sort_values("Score", ascending=False)
          .reset_index(drop=True)
    )
    df_results.index += 1   # Rank starts at 1

    top = df_results.head(TOP_N_STOCKS)

    print(f"\n✅  Scanned: {len(results) + skipped:,}  |  "
          f"Passed filters: {len(results):,}  |  Skipped: {skipped:,}")
    print(f"\n{'━' * 65}")
    print(f"  🏆  TOP {TOP_N_STOCKS} STOCKS FOR NOV 9–14 SWING TRADE (Price < ₹250)")
    print(f"{'━' * 65}\n")

    display_cols = ["Symbol", "Company", "Score", "Price (₹)",
                    "RSI", "MACD Signal", "EMA Trend",
                    "Supertrend", "Vol Surge", "Rev QoQ%", "Profit QoQ%"]
    print(top[display_cols].to_string())

    # ── Save to Excel ─────────────────────────────────────────────────────────
    with pd.ExcelWriter(OUTPUT_FILE, engine="openpyxl") as writer:
        df_results.to_excel(writer, sheet_name="All Results",    index_label="Rank")
        top.to_excel(       writer, sheet_name=f"Top {TOP_N_STOCKS}", index_label="Rank")

        # Style the top sheet
        ws = writer.sheets[f"Top {TOP_N_STOCKS}"]
        from openpyxl.styles import Font, PatternFill, Alignment
        green       = PatternFill("solid", fgColor="C6EFCE")
        header_font = Font(bold=True, color="FFFFFF")
        header_fill = PatternFill("solid", fgColor="2E86AB")

        for cell in ws[1]:
            cell.font      = header_font
            cell.fill      = header_fill
            cell.alignment = Alignment(horizontal="center")

        for row in ws.iter_rows(min_row=2):
            try:
                if row[2].value is not None and float(row[2].value) >= 70:
                    for cell in row:
                        cell.fill = green
            except (TypeError, ValueError):
                pass

    print(f"\n💾  Results saved → {OUTPUT_FILE}")
    print(f"\n{'═' * 65}")
    print("  ⚠️  DISCLAIMER: Technical screening only — NOT financial advice.")
    print("  Always do your own research before investing.")
    print(f"{'═' * 65}\n")


if __name__ == "__main__":
    main()
