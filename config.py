"""
Configuration for BSE/NSE Stock Screener
=========================================
Fill in your Zerodha Kite Connect API credentials below.
See SETUP.md for instructions on how to get these.
"""

# ── Zerodha Kite Connect Credentials ──────────────────────────────────────────
API_KEY      = "your_api_key_here"       # From Kite Connect developer console
API_SECRET   = "your_api_secret_here"   # From Kite Connect developer console
ACCESS_TOKEN = ""                        # Generated fresh each day (see SETUP.md)

# ── Screening Filters ──────────────────────────────────────────────────────────
MAX_PRICE   = 250        # Only stocks priced BELOW this (₹)
MIN_PRICE   = 5          # Avoid penny stocks below this (₹)
MIN_VOLUME  = 100_000    # Minimum average daily volume (shares)

# ── Technical Indicator Settings ───────────────────────────────────────────────
RSI_PERIOD       = 14
RSI_OVERSOLD     = 40    # RSI below this = potential buy zone
RSI_OVERBOUGHT   = 70    # RSI above this = avoid

EMA_SHORT        = 20
EMA_LONG         = 50

ATR_PERIOD       = 14
SUPERTREND_MULT  = 3.0   # Supertrend multiplier

MACD_FAST        = 12
MACD_SLOW        = 26
MACD_SIGNAL      = 9

BBANDS_PERIOD    = 20
BBANDS_STD       = 2.0

# ── Scoring Weights (must sum to 100) ─────────────────────────────────────────
WEIGHTS = {
    "rsi_score":        15,
    "macd_score":       15,
    "ema_score":        15,
    "supertrend_score": 15,
    "volume_score":     15,
    "quarterly_score":  25,   # Fundamental QoQ performance
}

# ── Candle History ─────────────────────────────────────────────────────────────
LOOKBACK_DAYS = 180      # Days of historical OHLCV data to fetch

# ── Output ────────────────────────────────────────────────────────────────────
OUTPUT_FILE   = "screener_results_nov9.xlsx"
TOP_N_STOCKS  = 50       # Print top N results
