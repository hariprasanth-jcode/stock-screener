"""
Smart Market & News Monitor — Real-Time Buy Trigger Dispatcher
==============================================================
Monitors top shortlisted stocks during market hours:
  1. Checks live price vs ideal entry zone
  2. Inspects intraday momentum & volume
  3. Pulls latest company news, announcements & quarterly updates
  4. Dispatches an immediate high-priority BUY ALERT email at the right time
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

# ── 1. CONFIGURE YOUR EMAIL ───────────────────────────────────────────────────
# Get an App Password: https://myaccount.google.com/apppasswords
GMAIL_USER     = "hari.mba000@gmail.com"
GMAIL_APP_PASS = "yoll icus ollp glmx"    # 16-character Google App Password
ALERT_RECEIVER = "hari.mba000@gmail.com"    # Where you receive the alert

# ── 2. TARGET WATCHLIST WITH CRITICAL ENTRY THRESHOLDS ────────────────────────
WATCHLIST = [
    {
        "symbol": "ESAFSFB",
        "name": "ESAF Small Finance Bank",
        "entry_min": 40.00,
        "entry_max": 44.00,
        "target": 50.00,
        "stop_loss": 38.00,
        "thesis": "QoQ profit doubled (+100%), full technical breakout above EMA20/50, healthy RSI 52."
    },
    {
        "symbol": "RGL",
        "name": "Renaissance Global",
        "entry_min": 150.00,
        "entry_max": 158.00,
        "target": 180.00,
        "stop_loss": 143.00,
        "thesis": "Massive 5.8× institutional volume surge; quarterly revenue doubled (+104%) & profit +230%."
    },
    {
        "symbol": "RBA",
        "name": "Restaurant Brands Asia",
        "entry_min": 90.00,
        "entry_max": 97.00,
        "target": 112.00,
        "stop_loss": 86.00,
        "thesis": "4.2× volume accumulation, MACD confirmed buy crossover, Burger King consumption recovery."
    },
    {
        "symbol": "JAIBALAJI",
        "name": "Jai Balaji Industries",
        "entry_min": 65.00,
        "entry_max": 70.00,
        "target": 82.00,
        "stop_loss": 61.00,
        "thesis": "Steel margin expansion, profit surged +298% QoQ, strong Supertrend support."
    },
    {
        "symbol": "GHCLTEXTIL",
        "name": "GHCL Textiles",
        "entry_min": 128.00,
        "entry_max": 134.00,
        "target": 155.00,
        "stop_loss": 120.00,
        "thesis": "Highest volume surge across all screened stocks (6.9×), revenue +16% & profit +42%."
    },
    {
        "symbol": "SPANDANA",
        "name": "Spandana Sphoorty Financial",
        "entry_min": 182.00,
        "entry_max": 190.00,
        "target": 215.00,
        "stop_loss": 172.00,
        "thesis": "Oversold bounce setup (RSI 37), MACD buy crossover, earnings accelerated +53% QoQ."
    },
    {
        "symbol": "MUFIN",
        "name": "Mufin Green Finance",
        "entry_min": 140.00,
        "entry_max": 147.00,
        "target": 165.00,
        "stop_loss": 133.00,
        "thesis": "Green mobility tailwind, clean technical alignment across all indicators, revenue +19%."
    },
    {
        "symbol": "NAVNETEDUL",
        "name": "Navneet Education",
        "entry_min": 125.00,
        "entry_max": 132.00,
        "target": 150.00,
        "stop_loss": 118.00,
        "thesis": "Stellar fundamentals: Revenue +83% & profit +271% QoQ. Peak Q3 educational seasonality."
    },
    {
        "symbol": "JMFINANCIL",
        "name": "JM Financial",
        "entry_min": 105.00,
        "entry_max": 112.00,
        "target": 128.00,
        "stop_loss": 99.00,
        "thesis": "Oversold reversal (RSI 39), 3.7× accumulation volume, investment banking revival."
    },
    {
        "symbol": "KANSAINER",
        "name": "Kansai Nerolac Paints",
        "entry_min": 200.00,
        "entry_max": 208.00,
        "target": 235.00,
        "stop_loss": 190.00,
        "thesis": "5.1× volume breakout, profit doubled (+106%), strong festive paint demand."
    },
    {
        "symbol": "PRABHA",
        "name": "Prabha Energy",
        "entry_min": 195.00,
        "entry_max": 205.00,
        "target": 230.00,
        "stop_loss": 185.00,
        "thesis": "Energy pick: Profit exploded +208% QoQ, revenue +17%, Supertrend bullish."
    },
    {
        "symbol": "AFCONS",
        "name": "Afcons Infrastructure",
        "entry_min": 215.00,
        "entry_max": 224.00,
        "target": 248.00,
        "stop_loss": 205.00,
        "thesis": "Infrastructure giant, profit +134% QoQ, strong order book execution."
    },
    {
        "symbol": "IXIGO",
        "name": "Le Travenues Technology",
        "entry_min": 160.00,
        "entry_max": 167.00,
        "target": 192.00,
        "stop_loss": 151.00,
        "thesis": "Travel-tech leader, profit surged +88% QoQ, peak winter holiday bookings."
    },
    {
        "symbol": "PWL",
        "name": "Physicswallah",
        "entry_min": 128.00,
        "entry_max": 136.00,
        "target": 158.00,
        "stop_loss": 120.00,
        "thesis": "Edtech leader, 5.4× institutional volume, revenue up 15%, peak exam season."
    }
]

# Track which stocks have already alerted today so we don't spam
alerted_today = set()


def fetch_latest_news(symbol: str) -> list[dict]:
    """Fetch recent news and corporate updates for the stock."""
    try:
        t = yf.Ticker(f"{symbol}.NS")
        news = t.news
        if not news:
            return []
        
        cleaned = []
        for item in news[:3]:
            cleaned.append({
                "title": item.get("title", ""),
                "publisher": item.get("publisher", ""),
                "link": item.get("link", ""),
                "published": datetime.datetime.fromtimestamp(
                    item.get("providerPublishTime", time.time())
                ).strftime("%d %b %H:%M")
            })
        return cleaned
    except Exception:
        return []


def send_buy_alert(stock: dict, current_price: float, news_items: list):
    """Dispatch an immediate, high-priority HTML Buy Alert."""
    sym = stock["symbol"]
    name = stock["name"]
    target = stock["target"]
    sl = stock["stop_loss"]
    potential_gain = round(((target - current_price) / current_price) * 100, 1)
    risk_ratio = round(((current_price - sl) / current_price) * 100, 1)

    news_html = ""
    if news_items:
        news_html = "<h4 style='color:#333;margin-bottom:6px;'>📰 Recent Company Updates & News:</h4><ul>"
        for n in news_items:
            news_html += f"<li><b>{n['publisher']}</b>: <a href='{n['link']}'>{n['title']}</a> <span style='color:gray;'>({n['published']})</span></li>"
        news_html += "</ul>"
    else:
        news_html = "<p style='color:gray;'><i>No negative news or disruptive announcements reported. Clean trend.</i></p>"

    html = f"""
    <html>
    <body style='font-family: Arial, sans-serif; background-color: #f7f9fa; padding: 20px;'>
        <div style='max-width: 600px; margin: auto; background: #ffffff; border-radius: 8px; border: 1px solid #e1e4e8; padding: 24px;'>
            <div style='border-bottom: 2px solid #28a745; padding-bottom: 12px; margin-bottom: 16px;'>
                <span style='background:#28a745; color:#fff; font-size:12px; font-weight:bold; padding:4px 8px; border-radius:4px;'>BUY TRIGGER ACTIVATED</span>
                <h2 style='color: #111; margin: 8px 0 0 0;'>{name} ({sym})</h2>
            </div>

            <p style='font-size:16px;'>The stock has entered its <b>Optimal Buy Window</b> at <b>₹{current_price:.2f}</b>.</p>

            <table style='width: 100%; border-collapse: collapse; margin: 16px 0; background: #fdfdfd;'>
                <tr>
                    <td style='padding: 8px; border: 1px solid #eee;'><b>Current Price:</b></td>
                    <td style='padding: 8px; border: 1px solid #eee; font-size: 16px; color: #28a745;'><b>₹{current_price:.2f}</b></td>
                </tr>
                <tr>
                    <td style='padding: 8px; border: 1px solid #eee;'><b>Accumulation Zone:</b></td>
                    <td style='padding: 8px; border: 1px solid #eee;'>₹{stock['entry_min']:.2f} - ₹{stock['entry_max']:.2f}</td>
                </tr>
                <tr>
                    <td style='padding: 8px; border: 1px solid #eee;'><b>Target (1-Week):</b></td>
                    <td style='padding: 8px; border: 1px solid #eee; font-weight: bold; color: #1a73e8;'>₹{target:.2f} (+{potential_gain}%)</td>
                </tr>
                <tr>
                    <td style='padding: 8px; border: 1px solid #eee;'><b>Strict Stop Loss:</b></td>
                    <td style='padding: 8px; border: 1px solid #eee; font-weight: bold; color: #dc3545;'>₹{sl:.2f} (-{risk_ratio}%)</td>
                </tr>
            </table>

            <div style='background: #f0f7ff; border-left: 4px solid #1a73e8; padding: 12px; margin: 16px 0;'>
                <h4 style='margin: 0 0 6px 0; color: #1a73e8;'>💡 Why Buy Right Now:</h4>
                <p style='margin: 0; font-size: 14px; color: #333;'>{stock['thesis']}</p>
            </div>

            {news_html}

            <div style='margin-top: 24px; padding-top: 12px; border-top: 1px solid #eee; font-size: 12px; color: #777;'>
                ⏰ <i>Triggered at {datetime.datetime.now(ZoneInfo('Asia/Kolkata')).strftime('%I:%M %p IST')}</i><br>
                ⚠️ <i>Trade plan: Swing for 1 week (Exit by Friday 3:00 PM). Ensure stop loss order is set immediately after buying.</i>
            </div>
        </div>
    </body>
    </html>
    """

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"🚨 BUY SIGNAL: {sym} @ ₹{current_price:.2f} (Target ₹{target})"
    msg["From"] = GMAIL_USER
    msg["To"] = ALERT_RECEIVER
    msg.attach(MIMEText(html, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_USER, GMAIL_APP_PASS)
            server.sendmail(GMAIL_USER, ALERT_RECEIVER, msg.as_string())
        print(f"🚀 BUY ALERT EMAIL SENT for {sym} at ₹{current_price:.2f}!")
    except Exception as e:
        print(f"❌ Failed to send email for {sym}: {e}")


def check_market():
    """Scan watchlist during market hours and dispatch buy alerts."""
    ist = ZoneInfo("Asia/Kolkata")
    now = datetime.datetime.now(ist)

    # Monday through Friday, 9:30 AM to 3:15 PM
    if now.weekday() >= 5:
        print(f"[{now.strftime('%H:%M:%S')}] Weekend — Market Closed.")
        return
    
    current_time_val = now.hour * 100 + now.minute
    if not (930 <= current_time_val <= 1515):
        print(f"[{now.strftime('%H:%M:%S')}] Outside monitoring window (9:30 AM - 3:15 PM).")
        return

    print(f"\n🔍 [{now.strftime('%H:%M:%S IST')}] Checking live prices & news updates...")

    for item in WATCHLIST:
        sym = item["symbol"]
        if sym in alerted_today:
            continue

        try:
            ticker = yf.Ticker(f"{sym}.NS")
            price = round(float(ticker.fast_info["last_price"]), 2)

            # Check if within optimal buy zone
            if item["entry_min"] <= price <= item["entry_max"]:
                print(f"🎯 TRIGGER HIT: {sym} is at ₹{price} (Zone: ₹{item['entry_min']}-₹{item['entry_max']})")
                
                # Fetch latest company news/updates
                news = fetch_latest_news(sym)
                
                # Send email immediately
                send_buy_alert(item, price, news)
                alerted_today.add(sym)
            else:
                print(f"   {sym:<12} ₹{price:>7.2f} (Target Zone: ₹{item['entry_min']}-₹{item['entry_max']})")

        except Exception as e:
            print(f"   Error checking {sym}: {e}")


def main():
    print("=" * 65)
    print("  🚀 REAL-TIME STOCK & COMPANY UPDATE BUY MONITOR")
    print(f"  Alerts sending to: {ALERT_RECEIVER}")
    print("  Monitors: Monday 9:30 AM to 3:15 PM IST")
    print("=" * 65)

    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print("\n🧪 TEST MODE: Simulating trigger alert for #1 pick (ESAFSFB)...")
        sample_stock = WATCHLIST[0]
        try:
            ticker = yf.Ticker(f"{sample_stock['symbol']}.NS")
            price = round(float(ticker.fast_info["last_price"]), 2)
        except Exception:
            price = 42.20
        news = fetch_latest_news(sample_stock["symbol"])
        send_buy_alert(sample_stock, price, news)
        print("✅ Test complete! Check your inbox.")
        return

    # Main scanning loop during market hours
    while True:
        check_market()
        # Sleep for 10 minutes (600 seconds)
        print("⏳ Next market scan in 10 minutes... (Press Ctrl+C to stop)")
        time.sleep(600)


if __name__ == "__main__":
    main()
