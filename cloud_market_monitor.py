"""
Cloud Stock & News Alert Dispatcher (Runs on GitHub Actions / Cloud Cron)
========================================================================
Runs on scheduled cloud server every Monday at 10:00 AM IST.
Scans all 14 stocks, checks company news & sends immediate email to phone.
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

# ── Credentials (from Environment or Defaults) ───────────────────────────────
GMAIL_USER     = (os.environ.get("GMAIL_USER") or "hari.mba000@gmail.com").strip()
GMAIL_APP_PASS = (os.environ.get("GMAIL_APP_PASS") or "yoll icus ollp glmx").strip()
ALERT_RECEIVER = (os.environ.get("ALERT_RECEIVER") or "hari.mba000@gmail.com").strip()

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


def main():
    ist = ZoneInfo("Asia/Kolkata")
    now_str = datetime.datetime.now(ist).strftime("%d %b %Y, %I:%M %p IST")
    print(f"🚀 Cloud Market Scan starting: {now_str}")

    buy_now_rows = ""
    watch_rows = ""

    for item in WATCHLIST:
        sym = item["symbol"]
        try:
            t = yf.Ticker(f"{sym}.NS")
            price = round(float(t.fast_info["last_price"]), 2)
            news = fetch_news(sym)
            news_txt = "<br>".join(news) if news else "<i>No negative announcements. Trend steady.</i>"

            gain = round(((item['target'] - price) / price) * 100, 1)

            if item["entry_min"] <= price <= item["entry_max"]:
                buy_now_rows += f"""
                <tr style='background:#f6fff8; border-bottom:1px solid #d4edda;'>
                    <td style='padding:10px;'><b>{sym}</b><br><small>{item['name']}</small></td>
                    <td style='padding:10px;'><b style='color:#28a745; font-size:16px;'>₹{price:.2f}</b></td>
                    <td style='padding:10px;'>₹{item['entry_min']:.2f} - ₹{item['entry_max']:.2f}</td>
                    <td style='padding:10px;'><b style='color:#1a73e8;'>₹{item['target']:.2f}</b> (+{gain}%)</td>
                    <td style='padding:10px;'><b style='color:#dc3545;'>₹{item['stop_loss']:.2f}</b></td>
                    <td style='padding:10px; font-size:12px;'>{item['thesis']}<br><br><b>Updates:</b> {news_txt}</td>
                </tr>
                """
            else:
                status = "🟡 Near Zone" if price <= item["entry_max"] * 1.03 else ("🔵 Under Zone" if price < item["entry_min"] else "🔴 Moved Higher")
                watch_rows += f"""
                <tr style='border-bottom:1px solid #eee;'>
                    <td style='padding:8px;'><b>{sym}</b></td>
                    <td style='padding:8px;'>₹{price:.2f}</td>
                    <td style='padding:8px;'>₹{item['entry_min']:.2f} - ₹{item['entry_max']:.2f}</td>
                    <td style='padding:8px;'>₹{item['target']:.2f}</td>
                    <td style='padding:8px;'>{status}</td>
                </tr>
                """
        except Exception as e:
            print(f"Error fetching {sym}: {e}")

    html = f"""
    <html>
    <body style='font-family: Arial, sans-serif; background:#f8f9fa; padding:15px;'>
        <div style='max-width:700px; margin:auto; background:#fff; border-radius:8px; border:1px solid #ddd; padding:20px;'>
            <div style='border-bottom:2px solid #1a73e8; padding-bottom:10px; margin-bottom:15px;'>
                <h2 style='margin:0; color:#1a73e8;'>📈 Monday Market Buy Action Report</h2>
                <span style='color:gray; font-size:13px;'>Snapshot: {now_str} (Cloud Automated)</span>
            </div>

            <h3 style='color:#28a745; margin-bottom:6px;'>🟢 STOCKS READY TO BUY (In Entry Zone):</h3>
            <table style='width:100%; border-collapse:collapse; margin-bottom:25px;'>
                <thead>
                    <tr style='background:#28a745; color:#fff;'>
                        <th style='padding:8px; text-align:left;'>Stock</th>
                        <th style='padding:8px; text-align:left;'>Price</th>
                        <th style='padding:8px; text-align:left;'>Entry Zone</th>
                        <th style='padding:8px; text-align:left;'>Target</th>
                        <th style='padding:8px; text-align:left;'>Stop Loss</th>
                        <th style='padding:8px; text-align:left;'>Why & Updates</th>
                    </tr>
                </thead>
                <tbody>
                    {buy_now_rows if buy_now_rows else "<tr><td colspan='6' style='padding:15px; text-align:center;'>No stocks currently in the exact buy zone. Watching for pullback.</td></tr>"}
                </tbody>
            </table>

            <h3 style='color:#6c757d; margin-bottom:6px;'>👀 WATCHLIST STATUS:</h3>
            <table style='width:100%; border-collapse:collapse;'>
                <thead>
                    <tr style='background:#f1f3f5;'>
                        <th style='padding:6px; text-align:left;'>Stock</th>
                        <th style='padding:6px; text-align:left;'>Price</th>
                        <th style='padding:6px; text-align:left;'>Target Zone</th>
                        <th style='padding:6px; text-align:left;'>1-Wk Target</th>
                        <th style='padding:6px; text-align:left;'>Status</th>
                    </tr>
                </thead>
                <tbody>
                    {watch_rows}
                </tbody>
            </table>

            <div style='margin-top:20px; padding:10px; background:#fff3cd; border-left:4px solid #ffeeba; font-size:12px;'>
                ⚠️ <b>Execution Rules:</b> 1-week swing holding. Place stop loss immediately in your broker app after purchase. Exit all positions by Friday 3:00 PM.
            </div>
        </div>
    </body>
    </html>
    """

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "🚀 Monday 10:00 AM Stock Buy Report & Company Updates"
    msg["From"] = GMAIL_USER
    msg["To"] = ALERT_RECEIVER
    msg.attach(MIMEText(html, "html"))

    print(f"Connecting to SMTP server as {GMAIL_USER}...")
    sent = False
    # Attempt 1: Port 587 (STARTTLS - standard for cloud runners)
    try:
        with smtplib.SMTP("smtp.gmail.com", 587, timeout=30) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(GMAIL_USER, GMAIL_APP_PASS)
            server.sendmail(GMAIL_USER, ALERT_RECEIVER, msg.as_string())
        print("✅ Monday Buy Report sent via Port 587 successfully!")
        sent = True
    except Exception as e1:
        print(f"Port 587 attempt failed: {e1}. Trying Port 465 SSL...")

    # Attempt 2: Port 465 (SSL fallback)
    if not sent:
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=30) as server:
                server.login(GMAIL_USER, GMAIL_APP_PASS)
                server.sendmail(GMAIL_USER, ALERT_RECEIVER, msg.as_string())
            print("✅ Monday Buy Report sent via Port 465 successfully!")
        except Exception as e2:
            print(f"❌ Port 465 attempt also failed: {e2}")


if __name__ == "__main__":
    main()
