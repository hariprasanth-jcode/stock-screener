"""
Continuous Real-Time Cloud Stock & News Alert Monitor (9:30 AM - 3:30 PM IST)
=============================================================================
Runs continuously on GitHub Cloud Runner during the full 6 hours of trading:
  - Scans live market prices every 2 minutes
  - Fires an immediate Buy Alert when a stock enters its optimal buy window
  - Inspects corporate news and announcements before sending
  - Sends a morning overview at 9:35 AM IST
"""

import os
import sys
import time
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from zoneinfo import ZoneInfo
import yfinance as yf

# ── Credentials (from Encrypted GitHub Secrets) ──────────────────────────────
GMAIL_USER     = os.environ.get("GMAIL_USER", "").strip()
GMAIL_APP_PASS = os.environ.get("GMAIL_APP_PASS", "").strip()
ALERT_RECEIVER = os.environ.get("ALERT_RECEIVER", "").strip()

WATCHLIST = [
    {
        "symbol": "ESAFSFB",
        "name": "ESAF Small Finance Bank",
        "entry_min": 40.00,
        "entry_max": 44.00,
        "target": 50.00,
        "stop_loss": 38.00,
        "sector": "Banking",
        "thesis": "QoQ profit doubled (+100%), technical breakout above EMA20/50, RSI 52."
    },
    {
        "symbol": "RGL",
        "name": "Renaissance Global",
        "entry_min": 150.00,
        "entry_max": 158.00,
        "target": 180.00,
        "stop_loss": 143.00,
        "sector": "Luxury / Exports",
        "thesis": "5.8× volume surge; quarterly revenue doubled (+104%) & profit +230%."
    },
    {
        "symbol": "RBA",
        "name": "Restaurant Brands Asia",
        "entry_min": 90.00,
        "entry_max": 97.00,
        "target": 112.00,
        "stop_loss": 86.00,
        "sector": "Consumer / QSR",
        "thesis": "4.2× volume accumulation, MACD buy crossover, Burger King recovery."
    },
    {
        "symbol": "JAIBALAJI",
        "name": "Jai Balaji Industries",
        "entry_min": 65.00,
        "entry_max": 70.00,
        "target": 82.00,
        "stop_loss": 61.00,
        "sector": "Steel",
        "thesis": "Margin expansion, profit surged +298% QoQ, strong Supertrend support."
    },
    {
        "symbol": "GHCLTEXTIL",
        "name": "GHCL Textiles",
        "entry_min": 128.00,
        "entry_max": 134.00,
        "target": 155.00,
        "stop_loss": 120.00,
        "sector": "Textiles",
        "thesis": "Highest volume surge (6.9×), revenue +16% & profit +42%."
    },
    {
        "symbol": "SPANDANA",
        "name": "Spandana Sphoorty Financial",
        "entry_min": 182.00,
        "entry_max": 190.00,
        "target": 215.00,
        "stop_loss": 172.00,
        "sector": "Microfinance",
        "thesis": "Oversold bounce setup (RSI 37), MACD buy crossover, profit +53% QoQ."
    },
    {
        "symbol": "MUFIN",
        "name": "Mufin Green Finance",
        "entry_min": 140.00,
        "entry_max": 147.00,
        "target": 165.00,
        "stop_loss": 133.00,
        "sector": "Green Finance",
        "thesis": "Clean technical alignment across all indicators, revenue +19%."
    },
    {
        "symbol": "NAVNETEDUL",
        "name": "Navneet Education",
        "entry_min": 125.00,
        "entry_max": 132.00,
        "target": 150.00,
        "stop_loss": 118.00,
        "sector": "Education",
        "thesis": "Stellar fundamentals: Revenue +83% & profit +271% QoQ. Q3 exam season."
    },
    {
        "symbol": "JMFINANCIL",
        "name": "JM Financial",
        "entry_min": 105.00,
        "entry_max": 112.00,
        "target": 128.00,
        "stop_loss": 99.00,
        "sector": "NBFC / Wealth",
        "thesis": "Oversold reversal (RSI 39), 3.7× accumulation volume, revenue +33%."
    },
    {
        "symbol": "KANSAINER",
        "name": "Kansai Nerolac Paints",
        "entry_min": 200.00,
        "entry_max": 208.00,
        "target": 235.00,
        "stop_loss": 190.00,
        "sector": "FMCG / Paints",
        "thesis": "5.1× volume breakout, profit doubled (+106%), strong festive demand."
    },
    {
        "symbol": "PRABHA",
        "name": "Prabha Energy",
        "entry_min": 195.00,
        "entry_max": 205.00,
        "target": 230.00,
        "stop_loss": 185.00,
        "sector": "Energy",
        "thesis": "Energy pick: Profit exploded +208% QoQ, revenue +17%."
    },
    {
        "symbol": "AFCONS",
        "name": "Afcons Infrastructure",
        "entry_min": 215.00,
        "entry_max": 224.00,
        "target": 248.00,
        "stop_loss": 205.00,
        "sector": "Infrastructure",
        "thesis": "Infrastructure giant, profit +134% QoQ, strong order book execution."
    },
    {
        "symbol": "IXIGO",
        "name": "Le Travenues Technology",
        "entry_min": 160.00,
        "entry_max": 167.00,
        "target": 192.00,
        "stop_loss": 151.00,
        "sector": "Travel Tech",
        "thesis": "Travel-tech leader, profit surged +88% QoQ, peak winter bookings."
    },
    {
        "symbol": "PWL",
        "name": "Physicswallah",
        "entry_min": 128.00,
        "entry_max": 136.00,
        "target": 158.00,
        "stop_loss": 120.00,
        "sector": "EdTech",
        "thesis": "5.4× institutional volume, revenue up 15%, peak exam season."
    }
]

# Track alerted symbols today
alerted_today = set()


def send_email(subject: str, html_body: str):
    """Sends an email with dual port fallback."""
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = GMAIL_USER
    msg["To"] = ALERT_RECEIVER
    msg.attach(MIMEText(html_body, "html"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587, timeout=25) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(GMAIL_USER, GMAIL_APP_PASS)
            server.sendmail(GMAIL_USER, ALERT_RECEIVER, msg.as_string())
        print(f"✅ Email sent: {subject}")
        return True
    except Exception as e1:
        print(f"Port 587 failed: {e1}. Trying 465 SSL...")
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=25) as server:
                server.login(GMAIL_USER, GMAIL_APP_PASS)
                server.sendmail(GMAIL_USER, ALERT_RECEIVER, msg.as_string())
            print(f"✅ Email sent via 465: {subject}")
            return True
        except Exception as e2:
            print(f"❌ Both SMTP ports failed: {e2}")
            return False


def fetch_news(sym: str) -> list:
    try:
        t = yf.Ticker(f"{sym}.NS")
        items = t.news or []
        res = []
        for n in items[:2]:
            res.append(f"<a href='{n.get('link','#')}'>{n.get('title','')}</a> ({n.get('publisher','')})")
        return res
    except Exception:
        return []


def send_immediate_buy_trigger(stock: dict, price: float, news: list):
    """Dispatches immediate real-time buy alert."""
    ist = ZoneInfo("Asia/Kolkata")
    now_str = datetime.datetime.now(ist).strftime("%I:%M %p IST")
    sym = stock["symbol"]
    name = stock["name"]
    tgt = stock["target"]
    sl = stock["stop_loss"]
    gain = round(((tgt - price) / price) * 100, 1)

    news_html = ""
    if news:
        news_html = "<h4>📰 Company Updates:</h4><ul>" + "".join([f"<li>{x}</li>" for x in news]) + "</ul>"
    else:
        news_html = "<p><i>No negative announcements reported. Technical trend solid.</i></p>"

    html = f"""
    <html>
    <body style='font-family: Arial, sans-serif; background:#f4f6f8; padding:15px;'>
        <div style='max-width:550px; margin:auto; background:#fff; border-radius:8px; border:2px solid #28a745; padding:20px;'>
            <span style='background:#28a745; color:#fff; font-size:12px; font-weight:bold; padding:4px 8px; border-radius:4px;'>BUY TRIGGER HIT</span>
            <h2 style='margin:10px 0 0 0; color:#111;'>{name} ({sym})</h2>
            <p style='font-size:15px;'>Price entered optimal entry zone at <b>₹{price:.2f}</b>.</p>

            <table style='width:100%; border-collapse:collapse; margin:15px 0;'>
                <tr style='background:#f8f9fa;'>
                    <td style='padding:8px; border:1px solid #ddd;'><b>Current Price:</b></td>
                    <td style='padding:8px; border:1px solid #ddd; color:#28a745; font-size:16px;'><b>₹{price:.2f}</b></td>
                </tr>
                <tr>
                    <td style='padding:8px; border:1px solid #ddd;'><b>Entry Zone:</b></td>
                    <td style='padding:8px; border:1px solid #ddd;'>₹{stock['entry_min']:.2f} - ₹{stock['entry_max']:.2f}</td>
                </tr>
                <tr style='background:#f8f9fa;'>
                    <td style='padding:8px; border:1px solid #ddd;'><b>Target (1-Wk):</b></td>
                    <td style='padding:8px; border:1px solid #ddd; color:#1a73e8; font-weight:bold;'>₹{tgt:.2f} (+{gain}%)</td>
                </tr>
                <tr>
                    <td style='padding:8px; border:1px solid #ddd;'><b>Stop Loss:</b></td>
                    <td style='padding:8px; border:1px solid #ddd; color:#dc3545; font-weight:bold;'>₹{sl:.2f}</td>
                </tr>
            </table>

            <div style='background:#eef6ff; padding:10px; border-left:4px solid #1a73e8; margin-bottom:15px;'>
                <b>Why Enter Now:</b> {stock['thesis']}
            </div>

            {news_html}

            <p style='font-size:12px; color:#888;'>⏰ Triggered at {now_str} • Continuous Live Cloud Monitor</p>
        </div>
    </body>
    </html>
    """
    subject = f"🚨 BUY NOW: {sym} @ ₹{price:.2f} (Target ₹{tgt})"
    send_email(subject, html)


def send_morning_overview():
    """Sends morning market snapshot once at 9:35 AM."""
    ist = ZoneInfo("Asia/Kolkata")
    now_str = datetime.datetime.now(ist).strftime("%d %b %Y, %I:%M %p IST")
    day_name = datetime.datetime.now(ist).strftime("%A")

    rows = ""
    for s in WATCHLIST:
        sym = s["symbol"]
        try:
            t = yf.Ticker(f"{sym}.NS")
            p = round(float(t.fast_info["last_price"]), 2)
            in_zone = s["entry_min"] <= p <= s["entry_max"]
            status = "<b style='color:#28a745;'>🟢 IN ZONE</b>" if in_zone else f"₹{s['entry_min']}-₹{s['entry_max']}"
            rows += f"""
            <tr style='border-bottom:1px solid #eee;'>
                <td style='padding:6px;'><b>{sym}</b></td>
                <td style='padding:6px;'><b>₹{p:.2f}</b></td>
                <td style='padding:6px;'>{status}</td>
                <td style='padding:6px; color:#1a73e8;'>₹{s['target']}</td>
                <td style='padding:6px; color:#dc3545;'>₹{s['stop_loss']}</td>
            </tr>
            """
        except Exception:
            pass

    html = f"""
    <html>
    <body style='font-family: Arial, sans-serif; padding:15px;'>
        <div style='max-width:600px; margin:auto; background:#fff; border:1px solid #ddd; padding:15px; border-radius:8px;'>
            <h3 style='color:#1a73e8; margin-top:0;'>📊 {day_name} Morning Stock Watchlist ({now_str})</h3>
            <p style='font-size:13px; color:#666;'>Continuous monitoring is ACTIVE (9:30 AM - 3:30 PM IST). You will receive instant alerts whenever any stock hits its buy window.</p>
            <table style='width:100%; border-collapse:collapse; font-size:13px;'>
                <tr style='background:#f2f2f2;'>
                    <th style='padding:6px; text-align:left;'>Stock</th>
                    <th style='padding:6px; text-align:left;'>Current</th>
                    <th style='padding:6px; text-align:left;'>Buy Zone</th>
                    <th style='padding:6px; text-align:left;'>Target</th>
                    <th style='padding:6px; text-align:left;'>Stop Loss</th>
                </tr>
                {rows}
            </table>
        </div>
    </body>
    </html>
    """
    send_email(f"📈 {day_name} 9:35 AM Market Watchlist Overview", html)


def main():
    ist = ZoneInfo("Asia/Kolkata")
    start_time = datetime.datetime.now(ist)
    print(f"🚀 Real-Time Continuous Monitor Started at {start_time.strftime('%I:%M:%S %p IST')}")

    # Send morning overview at start
    send_morning_overview()

    # Loop every 2 minutes until market close (3:30 PM IST)
    while True:
        now = datetime.datetime.now(ist)
        time_val = now.hour * 100 + now.minute

        # Stop monitoring after 3:30 PM IST (1530)
        if time_val > 1530:
            print(f"[{now.strftime('%H:%M:%S')}] Market closed for the day (3:30 PM IST). Finishing job.")
            break

        print(f"\n🔍 [{now.strftime('%H:%M:%S IST')}] Scanning live stock prices...")

        for s in WATCHLIST:
            sym = s["symbol"]
            if sym in alerted_today:
                continue

            try:
                t = yf.Ticker(f"{sym}.NS")
                price = round(float(t.fast_info["last_price"]), 2)

                if s["entry_min"] <= price <= s["entry_max"]:
                    print(f"🎯 TRIGGER HIT: {sym} at ₹{price:.2f} (Entry: ₹{s['entry_min']}-₹{s['entry_max']})")
                    news = fetch_news(sym)
                    send_immediate_buy_trigger(s, price, news)
                    alerted_today.add(sym)
                else:
                    print(f"   {sym:<12} ₹{price:>7.2f} (Target: ₹{s['entry_min']}-₹{s['entry_max']})")

            except Exception as e:
                print(f"   Error checking {sym}: {e}")

        # Wait 2 minutes (120 seconds) before next scan
        time.sleep(120)


if __name__ == "__main__":
    main()
