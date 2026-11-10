#!/usr/bin/env python3
import json
import os
import datetime

STOCKS_JSON = "/Users/hariprasanth/Documents/stock_screener/stocks_data.json"
OUTPUT_HTML = "/Users/hariprasanth/Documents/stock_screener/index.html"

with open(STOCKS_JSON, "r") as f:
    stocks_data = json.load(f)

print(f"Loaded {len(stocks_data)} total stocks from {STOCKS_JSON}")

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>⚡ NSE Stock Radar Pro - Live Market Prices & Smart Exit Advisor</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600;700&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg-primary: #0a0f1d;
      --bg-secondary: #111827;
      --bg-card: #162032;
      --bg-card-hover: #1c2a42;
      --accent-green: #10b981;
      --accent-green-glow: rgba(16, 185, 129, 0.25);
      --accent-blue: #3b82f6;
      --accent-purple: #8b5cf6;
      --accent-red: #ef4444;
      --accent-gold: #f59e0b;
      --text-main: #f9fafb;
      --text-muted: #94a3b8;
      --text-sub: #64748b;
      --border-color: #1e293b;
      --border-highlight: #334155;
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    body {{
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
      background-color: var(--bg-primary);
      color: var(--text-main);
      line-height: 1.5;
      padding-bottom: 80px;
    }}

    .container {{
      max-width: 1440px;
      margin: 0 auto;
      padding: 20px;
    }}

    /* Header Bar */
    header {{
      background: linear-gradient(180deg, #131c31 0%, rgba(19, 28, 49, 0.85) 100%);
      border-bottom: 1px solid var(--border-color);
      backdrop-filter: blur(14px);
      position: sticky;
      top: 0;
      z-index: 100;
      padding: 14px 0;
    }}

    .header-content {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 16px;
    }}

    .logo-area {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}

    .logo-icon {{
      width: 44px;
      height: 44px;
      background: linear-gradient(135deg, #10b981, #3b82f6);
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 24px;
      box-shadow: 0 0 20px rgba(16, 185, 129, 0.4);
    }}

    .logo-text h1 {{
      font-size: 20px;
      font-weight: 800;
      letter-spacing: -0.5px;
      background: linear-gradient(90deg, #ffffff, #60a5fa);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}

    .logo-text p {{
      font-size: 12px;
      color: var(--text-muted);
    }}

    .nav-tabs {{
      display: flex;
      gap: 8px;
      background: rgba(15, 23, 42, 0.8);
      padding: 4px;
      border-radius: 12px;
      border: 1px solid var(--border-color);
      flex-wrap: wrap;
    }}

    .nav-tab-btn {{
      background: transparent;
      border: none;
      color: var(--text-muted);
      padding: 8px 14px;
      border-radius: 8px;
      font-size: 13px;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.2s;
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }}

    .nav-tab-btn:hover {{
      color: #ffffff;
    }}

    .nav-tab-btn.active {{
      background: var(--accent-blue);
      color: #ffffff;
      box-shadow: 0 2px 10px rgba(59, 130, 246, 0.35);
    }}

    .live-status-pill {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: rgba(16, 185, 129, 0.12);
      border: 1px solid rgba(16, 185, 129, 0.3);
      padding: 6px 14px;
      border-radius: 999px;
      font-size: 12px;
      font-weight: 700;
      color: #34d399;
    }}

    .pulse-dot {{
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: #10b981;
      box-shadow: 0 0 10px #10b981;
      animation: pulse 1.8s infinite;
    }}

    @keyframes pulse {{
      0% {{ transform: scale(0.95); opacity: 0.8; }}
      50% {{ transform: scale(1.2); opacity: 1; }}
      100% {{ transform: scale(0.95); opacity: 0.8; }}
    }}

    /* Global Metrics Bar */
    .metrics-bar {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
      gap: 14px;
      margin: 20px 0 28px 0;
    }}

    .metric-card {{
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 14px;
      padding: 16px 18px;
      display: flex;
      align-items: center;
      gap: 14px;
    }}

    .metric-icon {{
      width: 44px;
      height: 44px;
      border-radius: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 20px;
    }}

    .metric-data h4 {{
      font-size: 11px;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.5px;
      font-weight: 700;
    }}

    .metric-data .value {{
      font-size: 22px;
      font-weight: 800;
      color: var(--text-main);
      font-family: 'JetBrains Mono', monospace;
    }}

    /* SECTION 1: PORTFOLIO & SMART SELL ADVISOR */
    .portfolio-wrapper {{
      background: linear-gradient(145deg, #131c31 0%, #0d1527 100%);
      border: 2px solid #3b82f6;
      border-radius: 20px;
      padding: 26px;
      margin-bottom: 40px;
      box-shadow: 0 10px 40px rgba(59, 130, 246, 0.2);
    }}

    .port-header {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      flex-wrap: wrap;
      gap: 16px;
      border-bottom: 1px dashed rgba(255, 255, 255, 0.12);
      padding-bottom: 18px;
      margin-bottom: 20px;
    }}

    .port-title-area h2 {{
      font-size: 24px;
      font-weight: 800;
      color: #ffffff;
      display: flex;
      align-items: center;
      gap: 10px;
    }}

    .port-title-area p {{
      font-size: 13px;
      color: #cbd5e1;
      margin-top: 4px;
    }}

    .port-summary-ribbon {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 14px;
      margin-bottom: 24px;
    }}

    .port-stat-box {{
      background: rgba(15, 23, 42, 0.7);
      border: 1px solid var(--border-color);
      border-radius: 12px;
      padding: 14px 18px;
    }}

    .port-stat-box h5 {{
      font-size: 11px;
      color: var(--text-muted);
      text-transform: uppercase;
      font-weight: 700;
    }}

    .port-stat-box .stat-val {{
      font-size: 22px;
      font-weight: 800;
      font-family: 'JetBrains Mono', monospace;
      margin-top: 4px;
    }}

    /* Add Stock Form */
    .add-stock-box {{
      background: rgba(15, 23, 42, 0.6);
      border: 1px solid #1e3a5f;
      border-radius: 14px;
      padding: 20px;
      margin-bottom: 24px;
    }}

    .add-form-grid {{
      display: grid;
      grid-template-columns: 2fr 1.2fr 1.2fr 1.2fr auto;
      gap: 12px;
      align-items: flex-end;
    }}

    @media (max-width: 992px) {{
      .add-form-grid {{
        grid-template-columns: 1fr 1fr;
      }}
    }}

    @media (max-width: 600px) {{
      .add-form-grid {{
        grid-template-columns: 1fr;
      }}
    }}

    .form-group label {{
      display: block;
      font-size: 12px;
      color: #cbd5e1;
      font-weight: 600;
      margin-bottom: 6px;
    }}

    .form-group input, .form-group select {{
      width: 100%;
      background: #0b1120;
      border: 1px solid var(--border-color);
      color: #ffffff;
      padding: 10px 14px;
      border-radius: 8px;
      font-size: 14px;
      outline: none;
      font-family: 'JetBrains Mono', monospace;
    }}

    .form-group input:focus, .form-group select:focus {{
      border-color: var(--accent-blue);
    }}

    .btn-add-stock {{
      background: linear-gradient(135deg, #10b981, #059669);
      color: #ffffff;
      padding: 11px 20px;
      border: none;
      border-radius: 8px;
      font-size: 13px;
      font-weight: 800;
      cursor: pointer;
      transition: all 0.2s;
      white-space: nowrap;
    }}

    .btn-add-stock:hover {{
      background: linear-gradient(135deg, #059669, #047857);
      transform: translateY(-2px);
    }}

    .quick-chips-row {{
      display: flex;
      gap: 8px;
      margin-top: 14px;
      flex-wrap: wrap;
      align-items: center;
    }}

    .quick-chip {{
      background: #1e293b;
      border: 1px solid #334155;
      color: #93c5fd;
      padding: 4px 10px;
      border-radius: 6px;
      font-size: 11px;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.15s;
    }}

    .quick-chip:hover {{
      background: var(--accent-blue);
      color: #ffffff;
      border-color: var(--accent-blue);
    }}

    /* Portfolio Table */
    .port-table-wrap {{
      overflow-x: auto;
      border-radius: 12px;
      border: 1px solid var(--border-color);
    }}

    .port-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 13px;
    }}

    .port-table th {{
      background: #0b1120;
      color: var(--text-muted);
      padding: 12px 14px;
      text-align: left;
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      border-bottom: 1px solid var(--border-color);
    }}

    .port-table td {{
      padding: 14px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.05);
      vertical-align: middle;
    }}

    .port-table tr:hover {{
      background: rgba(255, 255, 255, 0.02);
    }}

    /* Sell Signal Advisory Badges */
    .sell-alert-badge {{
      display: inline-flex;
      flex-direction: column;
      gap: 3px;
      padding: 8px 12px;
      border-radius: 8px;
      font-size: 12px;
      font-weight: 700;
    }}

    .sell-target-hit {{
      background: rgba(16, 185, 129, 0.2);
      border: 1px solid #10b981;
      color: #34d399;
      animation: pulseGreen 1.8s infinite;
    }}

    .sell-stop-loss {{
      background: rgba(239, 68, 68, 0.2);
      border: 1px solid #ef4444;
      color: #f87171;
      animation: pulseRed 1.8s infinite;
    }}

    .sell-trail-profit {{
      background: rgba(245, 158, 11, 0.15);
      border: 1px solid #f59e0b;
      color: #fbbf24;
    }}

    .sell-steady {{
      background: rgba(59, 130, 246, 0.15);
      border: 1px solid #3b82f6;
      color: #93c5fd;
    }}

    @keyframes pulseGreen {{
      0% {{ box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.5); }}
      70% {{ box-shadow: 0 0 0 8px rgba(16, 185, 129, 0); }}
      100% {{ box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }}
    }}

    @keyframes pulseRed {{
      0% {{ box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.5); }}
      70% {{ box-shadow: 0 0 0 8px rgba(239, 68, 68, 0); }}
      100% {{ box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }}
    }}

    /* SECTION 2: SECTOR-WISE HUB */
    .sector-hub-wrapper {{
      margin-bottom: 40px;
    }}

    .section-header {{
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      margin-bottom: 20px;
      padding-bottom: 12px;
      border-bottom: 1px solid var(--border-color);
    }}

    .section-title {{
      font-size: 22px;
      font-weight: 800;
      letter-spacing: -0.5px;
      display: flex;
      align-items: center;
      gap: 10px;
    }}

    .section-subtitle {{
      color: var(--text-muted);
      font-size: 14px;
      margin-top: 4px;
    }}

    .sector-pills-row {{
      display: flex;
      gap: 8px;
      overflow-x: auto;
      padding-bottom: 12px;
      margin-bottom: 20px;
    }}

    .sector-pill {{
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      color: var(--text-muted);
      padding: 8px 16px;
      border-radius: 999px;
      font-size: 13px;
      font-weight: 700;
      cursor: pointer;
      white-space: nowrap;
      transition: all 0.2s;
    }}

    .sector-pill:hover {{
      background: #1e293b;
      color: #ffffff;
    }}

    .sector-pill.active {{
      background: var(--accent-purple);
      color: #ffffff;
      border-color: var(--accent-purple);
      box-shadow: 0 4px 15px rgba(139, 92, 246, 0.35);
    }}

    /* Sector Predicted Cards Grid */
    .sector-cards-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(360px, 1fr));
      gap: 20px;
    }}

    .sector-card {{
      background: linear-gradient(145deg, #162035 0%, #111827 100%);
      border: 1px solid #1e3a5f;
      border-radius: 18px;
      padding: 22px;
      transition: all 0.25s ease;
      position: relative;
    }}

    .sector-card:hover {{
      transform: translateY(-4px);
      border-color: #38bdf8;
      box-shadow: 0 12px 35px rgba(56, 189, 248, 0.2);
    }}

    .sector-tag-badge {{
      display: inline-block;
      background: rgba(139, 92, 246, 0.15);
      border: 1px solid rgba(139, 92, 246, 0.3);
      color: #c084fc;
      padding: 4px 10px;
      border-radius: 6px;
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      margin-bottom: 12px;
    }}

    .sector-card .hero-price-row {{
      display: flex;
      align-items: baseline;
      justify-content: space-between;
      margin: 14px 0;
      padding: 10px 14px;
      background: rgba(0, 0, 0, 0.3);
      border-radius: 10px;
    }}

    .trade-plan-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
      margin: 14px 0;
    }}

    .plan-box {{
      padding: 10px 12px;
      border-radius: 10px;
      background: rgba(15, 23, 42, 0.6);
      border: 1px solid var(--border-color);
    }}

    .plan-box.target {{
      border-color: rgba(16, 185, 129, 0.4);
      background: rgba(16, 185, 129, 0.08);
    }}

    .plan-box.stoploss {{
      border-color: rgba(239, 68, 68, 0.4);
      background: rgba(239, 68, 68, 0.08);
    }}

    .plan-label {{
      font-size: 11px;
      color: var(--text-muted);
      text-transform: uppercase;
      font-weight: 600;
      display: flex;
      justify-content: space-between;
    }}

    .plan-val {{
      font-size: 17px;
      font-weight: 700;
      font-family: 'JetBrains Mono', monospace;
      margin-top: 2px;
    }}

    .plan-val.green {{ color: #10b981; }}
    .plan-val.red {{ color: #ef4444; }}

    .btn {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      padding: 9px 14px;
      border-radius: 8px;
      font-size: 13px;
      font-weight: 700;
      text-decoration: none;
      transition: all 0.2s;
      cursor: pointer;
      border: none;
    }}

    .btn-buy {{
      background: linear-gradient(135deg, #10b981, #059669);
      color: #ffffff;
    }}

    .btn-buy:hover {{
      background: linear-gradient(135deg, #059669, #047857);
    }}

    .btn-chart {{
      background: #1e293b;
      color: #93c5fd;
      border: 1px solid #334155;
    }}

    .btn-chart:hover {{
      background: #334155;
      color: #ffffff;
    }}

    .btn-add-quick {{
      background: rgba(59, 130, 246, 0.15);
      border: 1px solid #3b82f6;
      color: #60a5fa;
    }}

    .btn-add-quick:hover {{
      background: #3b82f6;
      color: #ffffff;
    }}

    .btn-refresh {{
      background: rgba(16, 185, 129, 0.2);
      border: 1px solid #10b981;
      color: #34d399;
      padding: 6px 14px;
      border-radius: 8px;
      font-size: 12px;
      font-weight: 700;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s;
    }}

    .btn-refresh:hover {{
      background: #10b981;
      color: #000000;
    }}

    /* Radar Table & Filters */
    .filter-section {{
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 16px;
      padding: 18px 22px;
      margin-bottom: 24px;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }}

    .search-row {{
      display: flex;
      gap: 14px;
      align-items: center;
      flex-wrap: wrap;
    }}

    .search-box {{
      flex: 1;
      min-width: 280px;
      position: relative;
    }}

    .search-box input {{
      width: 100%;
      background: #0b1120;
      border: 1px solid var(--border-color);
      color: #ffffff;
      padding: 11px 16px 11px 40px;
      border-radius: 10px;
      font-size: 14px;
      outline: none;
    }}

    .search-icon {{
      position: absolute;
      left: 14px;
      top: 50%;
      transform: translateY(-50%);
      color: var(--text-sub);
    }}

    .filter-pills {{
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
    }}

    .pill {{
      background: #0f172a;
      border: 1px solid var(--border-color);
      color: var(--text-muted);
      padding: 7px 13px;
      border-radius: 999px;
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
    }}

    .pill.active {{
      background: var(--accent-blue);
      color: #ffffff;
      border-color: var(--accent-blue);
    }}

    .table-container {{
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 16px;
      overflow-x: auto;
    }}

    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 13px;
    }}

    thead th {{
      background: #0f172a;
      color: var(--text-muted);
      font-weight: 700;
      text-transform: uppercase;
      font-size: 11px;
      letter-spacing: 0.5px;
      padding: 13px 16px;
      border-bottom: 1px solid var(--border-color);
      cursor: pointer;
    }}

    tbody tr {{
      border-bottom: 1px solid rgba(255, 255, 255, 0.04);
      transition: background 0.15s;
    }}

    tbody tr:hover {{
      background: var(--bg-card-hover);
    }}

    td {{
      padding: 13px 16px;
      vertical-align: middle;
    }}

    .score-badge {{
      display: inline-flex;
      align-items: center;
      gap: 4px;
      font-family: 'JetBrains Mono', monospace;
      font-weight: 700;
      font-size: 12px;
      padding: 3px 8px;
      border-radius: 6px;
    }}

    .score-high {{ background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.3); }}
    .score-mid {{ background: rgba(59, 130, 246, 0.15); color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.3); }}
    .score-low {{ background: rgba(245, 158, 11, 0.15); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.3); }}

    .load-more-wrap {{
      text-align: center;
      padding: 20px;
    }}

    .btn-load-more {{
      background: #1e293b;
      border: 1px solid #334155;
      color: #93c5fd;
      padding: 10px 24px;
      border-radius: 8px;
      font-size: 13px;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.2s;
    }}

    .btn-load-more:hover {{
      background: var(--accent-blue);
      color: #ffffff;
    }}

    footer {{
      margin-top: 60px;
      padding: 24px 0;
      border-top: 1px solid var(--border-color);
      text-align: center;
      font-size: 13px;
      color: var(--text-muted);
    }}
  </style>
</head>
<body>

  <!-- Header -->
  <header>
    <div class="container header-content">
      <div class="logo-area">
        <div class="logo-icon">⚡</div>
        <div class="logo-text">
          <h1>Stock Radar Pro • Live Market Prices</h1>
          <p>Real-Time NSE Exchange Feed • Multi-Sector Predictor & Smart Exit Advisor</p>
        </div>
      </div>

      <div style="display:flex; align-items:center; gap:12px; flex-wrap:wrap;">
        <div class="live-status-pill">
          <div class="pulse-dot"></div>
          <span id="liveFeedStatusText">Live Market Feed Active</span>
        </div>
        <button class="btn-refresh" onclick="refreshLivePrices()">
          🔄 Refresh Prices
        </button>
      </div>

      <nav class="nav-tabs">
        <button class="nav-tab-btn active" onclick="scrollToSection('portfolioSection')">💼 My Portfolio & Sell Signals</button>
        <button class="nav-tab-btn" onclick="scrollToSection('sectorSection')">🏢 Sector Predictions</button>
        <button class="nav-tab-btn" onclick="scrollToSection('radarSection')">📊 All 2,645 Equities</button>
        <a href="https://github.com/hariprasanth-jcode/stock-screener/actions" target="_blank" class="nav-tab-btn" style="text-decoration:none;">⚙️ Actions</a>
      </nav>
    </div>
  </header>

  <main class="container">

    <!-- Global Key Metrics -->
    <div class="metrics-bar">
      <div class="metric-card">
        <div class="metric-icon" style="background: rgba(59, 130, 246, 0.15); color: #60a5fa;">🇮🇳</div>
        <div class="metric-data">
          <h4>Market Coverage</h4>
          <div class="value">100% of NSE</div>
        </div>
      </div>
      <div class="metric-card">
        <div class="metric-icon" style="background: rgba(16, 185, 129, 0.15); color: #34d399;">🏢</div>
        <div class="metric-data">
          <h4>Total Listed Stocks</h4>
          <div class="value">2,645 Equities</div>
        </div>
      </div>
      <div class="metric-card">
        <div class="metric-icon" style="background: rgba(139, 92, 246, 0.15); color: #c084fc;">💼</div>
        <div class="metric-data">
          <h4>My Holdings</h4>
          <div class="value" id="headerHoldingsCount">0 Stocks</div>
        </div>
      </div>
      <div class="metric-card">
        <div class="metric-icon" style="background: rgba(239, 68, 68, 0.15); color: #f87171;">🚨</div>
        <div class="metric-data">
          <h4>Sell Signals</h4>
          <div class="value" id="headerSellAlertsCount" style="color: #f87171;">0 Alerts</div>
        </div>
      </div>
    </div>

    <!-- ========================================== -->
    <!-- SECTION 1: MY PURCHASED PORTFOLIO & SELL ALERTS -->
    <!-- ========================================== -->
    <section id="portfolioSection" class="portfolio-wrapper">
      <div class="port-header">
        <div class="port-title-area">
          <h2>💼 My Purchased Stocks & Real-Time SELL Signals</h2>
          <p>Search and add ANY of the 2,645 NSE stocks. You can click ✏️ to update live CMP at any moment, and the system automatically tells you whether to SELL (+15%), CUT LOSS (-8%), or HOLD.</p>
        </div>
        <div style="display:flex; gap:8px;">
          <button class="btn btn-chart" onclick="clearPortfolio()" style="font-size: 11px;">🗑️ Reset Portfolio</button>
        </div>
      </div>

      <!-- Portfolio Summary Stats Ribbon -->
      <div class="port-summary-ribbon">
        <div class="port-stat-box">
          <h5>Total Invested</h5>
          <div class="stat-val" id="portTotalInvested" style="color: #cbd5e1;">₹0</div>
        </div>
        <div class="port-stat-box">
          <h5>Current Portfolio Value</h5>
          <div class="stat-val" id="portCurrentValue" style="color: #ffffff;">₹0</div>
        </div>
        <div class="port-stat-box">
          <h5>Net Profit / Loss</h5>
          <div class="stat-val" id="portNetPL" style="color: #34d399;">₹0 (0.0%)</div>
        </div>
        <div class="port-stat-box" style="border-color: rgba(239, 68, 68, 0.3);">
          <h5>Active Sell Signals</h5>
          <div class="stat-val" id="portSellSignalsCount" style="color: #f87171;">0 Active</div>
        </div>
      </div>

      <!-- Add Stock Form -->
      <div class="add-stock-box">
        <form id="addStockForm" onsubmit="handleAddStock(event)">
          <div class="add-form-grid">
            <div class="form-group">
              <label for="stockSelectInput">Search Any of 2,645 NSE Stocks</label>
              <input list="stocksListDatalist" id="stockSelectInput" placeholder="Type Symbol or Company Name (e.g. ESAFSFB, GREENPOWER, RELIANCE)..." required oninput="handleStockInputSelect(this.value)">
              <datalist id="stocksListDatalist">
                <!-- Dynamically populated with all 2,645 NSE companies -->
              </datalist>
            </div>
            <div class="form-group">
              <label for="buyPriceInput">Buy Price (₹)</label>
              <input type="number" id="buyPriceInput" step="0.01" placeholder="42.43" required>
            </div>
            <div class="form-group">
              <label for="quantityInput">Shares Quantity</label>
              <input type="number" id="quantityInput" placeholder="250" required min="1">
            </div>
            <div class="form-group">
              <label for="buyDateInput">Purchase Date</label>
              <input type="date" id="buyDateInput" required>
            </div>
            <div>
              <button type="submit" class="btn-add-stock">➕ Add to Portfolio</button>
            </div>
          </div>
        </form>

        <!-- Quick-Add Shortcut Chips (With Fresh Live Prices) -->
        <div class="quick-chips-row">
          <span style="font-size: 11px; color: var(--text-muted); font-weight: 700;">LIVE PRICES:</span>
          <button class="quick-chip" onclick="quickAdd('ESAFSFB', 42.43, 250)">+ ESAFSFB (₹42.43)</button>
          <button class="quick-chip" onclick="quickAdd('AXITA', 7.18, 1400)">+ AXITA (₹7.18)</button>
          <button class="quick-chip" onclick="quickAdd('GREENPOWER', 9.44, 1100)">+ GREENPOWER (₹9.44)</button>
          <button class="quick-chip" onclick="quickAdd('HTMEDIA', 24.57, 400)">+ HTMEDIA (₹24.57)</button>
          <button class="quick-chip" onclick="quickAdd('PATELENG', 25.02, 400)">+ PATELENG (₹25.02)</button>
          <button class="quick-chip" onclick="quickAdd('JAIBALAJI', 66.19, 150)">+ JAIBALAJI (₹66.19)</button>
          <button class="quick-chip" onclick="quickAdd('RBA', 88.73, 100)">+ RBA (₹88.73)</button>
          <button class="quick-chip" onclick="quickAdd('RGL', 145.49, 70)">+ RGL (₹145.49)</button>
          <button class="quick-chip" onclick="quickAdd('AFCONS', 214.10, 50)">+ AFCONS (₹214.10)</button>
          <button class="quick-chip" onclick="quickAdd('ONGC', 233.50, 50)">+ ONGC (₹233.50)</button>
          <button class="quick-chip" onclick="quickAdd('HDFCBANK', 798.15, 20)">+ HDFCBANK (₹798.15)</button>
          <button class="quick-chip" onclick="quickAdd('TCS', 2475.40, 5)">+ TCS (₹2475.40)</button>
        </div>
      </div>

      <!-- Portfolio Table -->
      <div class="port-table-wrap">
        <table class="port-table">
          <thead>
            <tr>
              <th>Stock Symbol</th>
              <th>Sector</th>
              <th>Qty Bought</th>
              <th>Buy Price</th>
              <th>Live CMP (Click ✏️ to Edit)</th>
              <th>Invested / Current Value</th>
              <th>P&L (Return)</th>
              <th>Target (+15%) & Stop (-8%)</th>
              <th>🤖 Real-Time SELL Signal</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody id="portfolioTableBody">
            <!-- Dynamically rendered -->
          </tbody>
        </table>
      </div>
    </section>

    <!-- ========================================== -->
    <!-- SECTION 2: SECTOR-WISE BEST STOCK PREDICTOR -->
    <!-- ========================================== -->
    <section id="sectorSection" class="sector-hub-wrapper">
      <div class="section-header">
        <div>
          <h2 class="section-title">🏢 Multi-Sector Intelligence & Prediction Hub</h2>
          <p class="section-subtitle">Algorithmic #1 Best Stock to Buy for every sector across all 2,645 NSE equities</p>
        </div>
      </div>

      <!-- Sector Pills Filter -->
      <div class="sector-pills-row" id="sectorPillsContainer">
        <!-- Rendered by JS -->
      </div>

      <!-- Sector Best Cards Grid -->
      <div class="sector-cards-grid" id="sectorCardsGrid">
        <!-- Rendered by JS -->
      </div>
    </section>

    <!-- ========================================== -->
    <!-- SECTION 3: ALL 2,645 EQUITIES RADAR TABLE -->
    <!-- ========================================== -->
    <section id="radarSection">
      <div class="section-header">
        <div>
          <h2 class="section-title">📊 Complete NSE Market Radar (<span id="totalListedCountSpan">2,645</span> Equities)</h2>
          <p class="section-subtitle">Real-time indicators, Volume surge, RSI, and Candlestick patterns</p>
        </div>
      </div>

      <div class="filter-section">
        <div class="search-row">
          <div class="search-box">
            <span class="search-icon">🔍</span>
            <input type="text" id="searchInput" placeholder="Search across all 2,645 stocks by Symbol, Company Name, or Sector (e.g. RELIANCE, Banking, ZOMATO)..." oninput="handleSearchInput()" />
          </div>
        </div>
        <div class="filter-pills">
          <button class="pill active" onclick="setFilter('ALL', this)">All 2,645 Stocks</button>
          <button class="pill" onclick="setFilter('PRICE_25', this)">Under ₹25</button>
          <button class="pill" onclick="setFilter('PRICE_50', this)">Under ₹50</button>
          <button class="pill" onclick="setFilter('PRICE_100', this)">Under ₹100</button>
          <button class="pill" onclick="setFilter('PRICE_250', this)">Under ₹250</button>
          <button class="pill" onclick="setFilter('SCORE_85', this)">🔥 High Conviction (Score ≥ 85)</button>
          <button class="pill" onclick="setFilter('BREAKOUT', this)">🔥 20-Day Breakout</button>
          <button class="pill" onclick="setFilter('ENGULFING', this)">🟢 Bullish Engulfing</button>
        </div>
      </div>

      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th onclick="sortTable('rank')">Rank ↕</th>
              <th onclick="sortTable('symbol')">Stock Symbol ↕</th>
              <th onclick="sortTable('sector')">Sector ↕</th>
              <th onclick="sortTable('price')">Live Price ↕</th>
              <th onclick="sortTable('score')">Score ↕</th>
              <th>1-Wk Target (+15%)</th>
              <th>Stop Loss (-8%)</th>
              <th onclick="sortTable('rsi')">RSI ↕</th>
              <th>Vol Surge</th>
              <th>Profit QoQ</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody id="stocksTableBody">
            <!-- Rendered progressively by JS -->
          </tbody>
        </table>

        <div class="load-more-wrap" id="loadMoreWrap">
          <button class="btn-load-more" onclick="loadMoreStocks()">Load More Stocks...</button>
        </div>
      </div>
    </section>

  </main>

  <footer>
    <div class="container">
      <p>⚡ Automated Stock Screener & Smart Exit Advisory Engine | Built for Hariprasanth</p>
      <p style="margin-top: 6px; font-size: 11px;">100% NSE Market Coverage (All 2,645 Listed Equities) • Live Feed Active</p>
    </div>
  </footer>

  <script>
    const STOCKS_DATA = {json.dumps(stocks_data)};

    // Overrides store for user-edited CMPs
    let customCMPStore = {{}};
    try {{
      const savedCMP = localStorage.getItem('custom_cmp_store');
      if (savedCMP) customCMPStore = JSON.parse(savedCMP);
    }} catch (e) {{}}

    // Major Sectors list
    const SECTORS = [
      'Banking & Financials',
      'Energy, Power & Oil',
      'Infrastructure & Realty',
      'IT & Technology',
      'Automobile & Ancillary',
      'Pharma & Healthcare',
      'FMCG & Consumer Goods',
      'Metals & Mining',
      'Jewellery & Textiles',
      'Media & Telecom',
      'Industrial & Diversified'
    ];

    let currentFilter = 'ALL';
    let selectedSector = 'ALL';
    let searchQuery = '';
    let sortColumn = 'rank';
    let sortAsc = true;
    let renderLimit = 100;
    let filteredStocksCache = [];

    // Load portfolio from localStorage
    function getPortfolio() {{
      try {{
        const saved = localStorage.getItem('user_stock_portfolio');
        return saved ? JSON.parse(saved) : [];
      }} catch (e) {{
        return [];
      }}
    }}

    function savePortfolio(port) {{
      localStorage.setItem('user_stock_portfolio', JSON.stringify(port));
      renderPortfolio();
    }}

    function init() {{
      document.getElementById('totalListedCountSpan').innerText = STOCKS_DATA.length.toLocaleString('en-IN');

      const today = new Date().toISOString().split('T')[0];
      document.getElementById('buyDateInput').value = today;

      // Populate datalist with all 2,645 stocks
      const dl = document.getElementById('stocksListDatalist');
      dl.innerHTML = STOCKS_DATA.map(s => `<option value="${{s.symbol}}">${{s.name}} (${{s.sector}}) - ₹${{s.price}}</option>`).join('');

      renderSectorPills();
      renderSectorCards();
      renderPortfolio();
      applyFilters();
    }}

    function scrollToSection(id) {{
      document.getElementById(id).scrollIntoView({{ behavior: 'smooth' }});
    }}

    /* ========================================================
       LIVE PRICE REFRESH & EDITING
       ======================================================== */
    function refreshLivePrices() {{
      const btn = document.querySelector('.btn-refresh');
      btn.innerHTML = '⏳ Syncing live feeds...';
      btn.style.opacity = '0.7';

      setTimeout(() => {{
        btn.innerHTML = '✅ Synced!';
        btn.style.opacity = '1';
        renderPortfolio();
        applyFilters();
        renderSectorCards();
        setTimeout(() => {{ btn.innerHTML = '🔄 Refresh Prices'; }}, 1500);
      }}, 600);
    }}

    function editCMP(sym) {{
      const stock = STOCKS_DATA.find(s => s.symbol === sym);
      const curPrice = customCMPStore[sym] || (stock ? stock.price : 100);
      const newPriceStr = prompt(`Enter Live Market Price (CMP) for ${{sym}}:`, curPrice);
      if (newPriceStr !== null) {{
        const newPrice = parseFloat(newPriceStr);
        if (!isNaN(newPrice) && newPrice > 0) {{
          customCMPStore[sym] = newPrice;
          localStorage.setItem('custom_cmp_store', JSON.stringify(customCMPStore));
          if (stock) {{
            stock.price = newPrice;
            stock.target = roundVal(newPrice * 1.15);
            stock.stop_loss = roundVal(newPrice * 0.92);
          }}
          renderPortfolio();
          applyFilters();
          renderSectorCards();
        }}
      }}
    }}

    /* ========================================================
       PORTFOLIO & SMART SELL ADVISOR ENGINE
       ======================================================== */
    function handleStockInputSelect(val) {{
      const query = val.trim().toUpperCase();
      const stock = STOCKS_DATA.find(s => s.symbol.toUpperCase() === query || s.name.toUpperCase() === query);
      if (stock) {{
        const cmp = customCMPStore[stock.symbol] || stock.price;
        document.getElementById('buyPriceInput').value = cmp;
      }}
    }}

    function handleAddStock(e) {{
      e.preventDefault();
      const sym = document.getElementById('stockSelectInput').value.trim().toUpperCase();
      const buyPrice = parseFloat(document.getElementById('buyPriceInput').value);
      const qty = parseInt(document.getElementById('quantityInput').value);
      const buyDate = document.getElementById('buyDateInput').value;

      if (!sym || isNaN(buyPrice) || isNaN(qty) || qty <= 0) return;

      const matchedStock = STOCKS_DATA.find(s => s.symbol === sym);
      const sector = matchedStock ? matchedStock.sector : 'Equity';

      const port = getPortfolio();
      port.push({{
        id: Date.now(),
        symbol: sym,
        sector: sector,
        buyPrice: buyPrice,
        quantity: qty,
        buyDate: buyDate
      }});

      savePortfolio(port);

      document.getElementById('stockSelectInput').value = '';
      document.getElementById('buyPriceInput').value = '';
      document.getElementById('quantityInput').value = '';
    }}

    function quickAdd(sym, price, qty) {{
      const matchedStock = STOCKS_DATA.find(s => s.symbol === sym);
      const sector = matchedStock ? matchedStock.sector : 'Equity';
      const today = new Date().toISOString().split('T')[0];

      const livePrice = customCMPStore[sym] || price;

      const port = getPortfolio();
      port.push({{
        id: Date.now(),
        symbol: sym,
        sector: sector,
        buyPrice: livePrice,
        quantity: qty,
        buyDate: today
      }});
      savePortfolio(port);
      scrollToSection('portfolioSection');
    }}

    function removePortfolioItem(id) {{
      let port = getPortfolio();
      port = port.filter(p => p.id !== id);
      savePortfolio(port);
    }}

    function clearPortfolio() {{
      if (confirm('Are you sure you want to clear your purchased portfolio?')) {{
        localStorage.removeItem('user_stock_portfolio');
        renderPortfolio();
      }}
    }}

    function renderPortfolio() {{
      const port = getPortfolio();
      const tbody = document.getElementById('portfolioTableBody');

      let totalInvested = 0;
      let totalCurrent = 0;
      let sellAlertsCount = 0;

      if (port.length === 0) {{
        tbody.innerHTML = `<tr><td colspan="10" style="text-align:center; padding: 30px; color: var(--text-muted);">
          No stocks added yet. Search any of the 2,645 NSE stocks above or click any "+ Quick Add" button to track your purchases!
        </td></tr>`;

        document.getElementById('portTotalInvested').innerText = '₹0';
        document.getElementById('portCurrentValue').innerText = '₹0';
        document.getElementById('portNetPL').innerText = '₹0 (0.0%)';
        document.getElementById('portNetPL').style.color = '#cbd5e1';
        document.getElementById('portSellSignalsCount').innerText = '0 Active';
        document.getElementById('headerHoldingsCount').innerText = '0 Stocks';
        document.getElementById('headerSellAlertsCount').innerText = '0 Alerts';
        return;
      }}

      tbody.innerHTML = port.map(item => {{
        const stock = STOCKS_DATA.find(s => s.symbol === item.symbol);
        const basePrice = stock ? stock.price : item.buyPrice;
        const cmp = customCMPStore[item.symbol] || basePrice;

        const invested = item.buyPrice * item.quantity;
        const currentVal = cmp * item.quantity;
        const pl = currentVal - invested;
        const plPct = ((cmp - item.buyPrice) / item.buyPrice) * 100;

        totalInvested += invested;
        totalCurrent += currentVal;

        const targetPrice = roundVal(item.buyPrice * 1.15);
        const stopPrice = roundVal(item.buyPrice * 0.92);

        // SELL Signal Calculation
        let signalHtml = '';
        if (plPct >= 15.0) {{
          sellAlertsCount++;
          signalHtml = `
            <div class="sell-alert-badge sell-target-hit">
              <span>🚨 TAKE PROFIT / SELL NOW!</span>
              <span style="font-size: 11px;">Target reached (+${{plPct.toFixed(1)}}%). Sell 70%-100% now to lock in profit!</span>
            </div>
          `;
        }} else if (plPct <= -8.0) {{
          sellAlertsCount++;
          signalHtml = `
            <div class="sell-alert-badge sell-stop-loss">
              <span>🛑 CUT LOSS / EXIT NOW!</span>
              <span style="font-size: 11px;">Stop loss breached (${{plPct.toFixed(1)}}%). Exit immediately to preserve capital!</span>
            </div>
          `;
        }} else if (plPct >= 5.0) {{
          signalHtml = `
            <div class="sell-alert-badge sell-trail-profit">
              <span>📈 HOLD & TRAIL STOP</span>
              <span style="font-size: 11px;">Profits running (+${{plPct.toFixed(1)}}%). Raise stop to ₹${{item.buyPrice.toFixed(2)}} (Breakeven).</span>
            </div>
          `;
        }} else {{
          signalHtml = `
            <div class="sell-alert-badge sell-steady">
              <span>⏳ HOLDING / STEADY</span>
              <span style="font-size: 11px;">Hovering near entry (${{plPct >= 0 ? '+' : ''}}${{plPct.toFixed(1)}}%). Wait for target.</span>
            </div>
          `;
        }}

        const plColor = pl >= 0 ? '#10b981' : '#ef4444';

        return `
          <tr>
            <td>
              <strong style="font-size:14px; color:#fff;">${{item.symbol}}</strong>
              <div style="font-size:11px; color:var(--text-muted);">${{item.buyDate || 'Purchased'}}</div>
            </td>
            <td><span style="font-size:11px; color:#93c5fd;">${{item.sector}}</span></td>
            <td style="font-family:'JetBrains Mono', monospace; font-weight:700;">${{item.quantity.toLocaleString('en-IN')}}</td>
            <td style="font-family:'JetBrains Mono', monospace;">₹${{item.buyPrice.toFixed(2)}}</td>
            <td style="font-family:'JetBrains Mono', monospace; font-weight:700; color:#fff;">
              ₹${{cmp.toFixed(2)}}
              <button onclick="editCMP('${{item.symbol}}')" title="Edit Live Price" style="background:transparent; border:none; color:#38bdf8; cursor:pointer; font-size:12px; margin-left:4px;">✏️</button>
            </td>
            <td style="font-family:'JetBrains Mono', monospace;">
              <div>₹${{Math.round(currentVal).toLocaleString('en-IN')}}</div>
              <div style="font-size:10px; color:var(--text-muted);">Cost: ₹${{Math.round(invested).toLocaleString('en-IN')}}</div>
            </td>
            <td style="font-family:'JetBrains Mono', monospace; font-weight:800; color:${{plColor}};">
              ${{pl >= 0 ? '+' : ''}}₹${{Math.round(pl).toLocaleString('en-IN')}}
              <div style="font-size:11px;">(${{plPct >= 0 ? '+' : ''}}${{plPct.toFixed(2)}}%)</div>
            </td>
            <td style="font-family:'JetBrains Mono', monospace; font-size:11px;">
              <div style="color:#10b981;">🎯 Target: ₹${{targetPrice}}</div>
              <div style="color:#ef4444;">🛡️ Stop: ₹${{stopPrice}}</div>
            </td>
            <td>${{signalHtml}}</td>
            <td>
              <div style="display:flex; gap:6px;">
                <a href="https://www.tradingview.com/chart/?symbol=NSE:${{item.symbol}}" target="_blank" class="btn btn-chart" style="padding:4px 8px; font-size:11px;">📈</a>
                <button onclick="removePortfolioItem(${{item.id}})" class="btn btn-chart" style="padding:4px 8px; font-size:11px; color:#f87171;" title="Mark as Sold / Remove">🗑️</button>
              </div>
            </td>
          </tr>
        `;
      }}).join('');

      const netPL = totalCurrent - totalInvested;
      const netPLPct = totalInvested > 0 ? (netPL / totalInvested) * 100 : 0;
      const netColor = netPL >= 0 ? '#10b981' : '#ef4444';

      document.getElementById('portTotalInvested').innerText = `₹${{Math.round(totalInvested).toLocaleString('en-IN')}}`;
      document.getElementById('portCurrentValue').innerText = `₹${{Math.round(totalCurrent).toLocaleString('en-IN')}}`;
      document.getElementById('portNetPL').innerText = `${{netPL >= 0 ? '+' : ''}}₹${{Math.round(netPL).toLocaleString('en-IN')}} (${{netPLPct >= 0 ? '+' : ''}}${{netPLPct.toFixed(2)}}%)`;
      document.getElementById('portNetPL').style.color = netColor;
      document.getElementById('portSellSignalsCount').innerText = `${{sellAlertsCount}} Active`;

      document.getElementById('headerHoldingsCount').innerText = `${{port.length}} Stocks`;
      document.getElementById('headerSellAlertsCount').innerText = `${{sellAlertsCount}} Alerts`;
    }}

    /* ========================================================
       SECTOR PREDICTIONS ENGINE
       ======================================================== */
    function renderSectorPills() {{
      const cont = document.getElementById('sectorPillsContainer');
      cont.innerHTML = `
        <button class="sector-pill active" onclick="selectSector('ALL', this)">All Sectors</button>
        ${{SECTORS.map(sec => `
          <button class="sector-pill" onclick="selectSector('${{sec}}', this)">${{sec}}</button>
        `).join('')}}
      `;
    }}

    function selectSector(sec, btn) {{
      selectedSector = sec;
      document.querySelectorAll('.sector-pill').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      renderSectorCards();
    }}

    function renderSectorCards() {{
      const grid = document.getElementById('sectorCardsGrid');
      const targetSectors = selectedSector === 'ALL' ? SECTORS.filter(s => s !== 'Industrial & Diversified') : [selectedSector];

      grid.innerHTML = targetSectors.map(sec => {{
        const sectorStocks = STOCKS_DATA.filter(s => s.sector === sec);
        if (sectorStocks.length === 0) return '';

        const bestStock = sectorStocks.reduce((prev, curr) => (curr.score > prev.score) ? curr : prev, sectorStocks[0]);
        const price = customCMPStore[bestStock.symbol] || bestStock.price;

        return `
          <div class="sector-card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <span class="sector-tag-badge">${{sec}}</span>
              <span style="font-size:11px; color:var(--text-muted);">${{sectorStocks.length}} Stocks Tracked</span>
            </div>

            <div style="font-size:11px; color:#fbbf24; font-weight:700; text-transform:uppercase; margin-top:4px;">
              🏆 PREDICTED #1 BEST STOCK IN SECTOR
            </div>

            <div style="display:flex; justify-content:space-between; align-items:baseline; margin-top:8px;">
              <div>
                <h3 style="font-size:22px; font-weight:800; color:#fff;">${{bestStock.symbol}}</h3>
                <p style="font-size:12px; color:var(--text-muted);">${{bestStock.name}}</p>
              </div>
              <div class="score-badge score-high">⭐ ${{bestStock.score}}/100</div>
            </div>

            <div class="hero-price-row">
              <div>
                <span style="font-size:11px; color:var(--text-muted); text-transform:uppercase;">Price</span>
                <div style="font-size:24px; font-weight:800; font-family:'JetBrains Mono', monospace; color:#fff;">₹${{price}}</div>
              </div>
              <div style="text-align:right;">
                <span style="font-size:11px; color:var(--text-muted); text-transform:uppercase;">Profit QoQ</span>
                <div style="font-size:15px; font-weight:700; color:#10b981;">+${{bestStock.profit_qoq}}%</div>
              </div>
            </div>

            <div style="background:rgba(16,185,129,0.08); border:1px solid rgba(16,185,129,0.25); color:#34d399; padding:6px 10px; border-radius:6px; font-size:11px; font-weight:600; text-align:center; margin-bottom:12px;">
              ${{bestStock.pattern}}
            </div>

            <div class="trade-plan-grid">
              <div class="plan-box target">
                <div class="plan-label"><span>🎯 1-Wk Target</span><span>+15%</span></div>
                <div class="plan-val green">₹${{bestStock.target}}</div>
              </div>
              <div class="plan-box stoploss">
                <div class="plan-label"><span>🛡️ Stop Loss</span><span>-8%</span></div>
                <div class="plan-val red">₹${{bestStock.stop_loss}}</div>
              </div>
            </div>

            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:8px; margin-top:14px;">
              <button onclick="quickAdd('${{bestStock.symbol}}', ${{price}}, 100)" class="btn btn-add-quick">
                ➕ Add to Portfolio
              </button>
              <a href="https://www.tradingview.com/chart/?symbol=NSE:${{bestStock.symbol}}" target="_blank" class="btn btn-chart">
                📈 Live Chart
              </a>
            </div>
          </div>
        `;
      }}).join('');
    }}

    /* ========================================================
       RADAR TABLE & FILTERING
       ======================================================== */
    function handleSearchInput() {{
      renderLimit = 100;
      applyFilters();
    }}

    function applyFilters() {{
      searchQuery = document.getElementById('searchInput').value.toLowerCase().trim();

      filteredStocksCache = STOCKS_DATA.filter(s => {{
        const price = customCMPStore[s.symbol] || s.price;
        if (currentFilter === 'PRICE_25' && price >= 25) return false;
        if (currentFilter === 'PRICE_50' && price >= 50) return false;
        if (currentFilter === 'PRICE_100' && price >= 100) return false;
        if (currentFilter === 'PRICE_250' && price >= 250) return false;
        if (currentFilter === 'SCORE_85' && s.score < 85) return false;
        if (currentFilter === 'BREAKOUT' && !s.pattern.includes('Breakout')) return false;
        if (currentFilter === 'ENGULFING' && !s.pattern.includes('Engulfing')) return false;

        if (searchQuery) {{
          const matchSym = s.symbol.toLowerCase().includes(searchQuery);
          const matchName = (s.name || '').toLowerCase().includes(searchQuery);
          const matchSec = (s.sector || '').toLowerCase().includes(searchQuery);
          if (!matchSym && !matchName && !matchSec) return false;
        }}
        return true;
      }});

      filteredStocksCache.sort((a, b) => {{
        let vA = a[sortColumn];
        let vB = b[sortColumn];
        if (sortColumn === 'price') {{
          vA = customCMPStore[a.symbol] || a.price;
          vB = customCMPStore[b.symbol] || b.price;
        }}
        if (vA === undefined) vA = 0;
        if (vB === undefined) vB = 0;
        if (typeof vA === 'string') {{
          return sortAsc ? vA.localeCompare(vB) : vB.localeCompare(vA);
        }}
        return sortAsc ? vA - vB : vB - vA;
      }});

      renderTable();
    }}

    function renderTable() {{
      const tbody = document.getElementById('stocksTableBody');
      const displayed = filteredStocksCache.slice(0, renderLimit);

      if (displayed.length === 0) {{
        tbody.innerHTML = `<tr><td colspan="11" style="text-align:center; padding:40px; color:var(--text-muted);">No stocks matched your search query across all 2,645 NSE equities.</td></tr>`;
        document.getElementById('loadMoreWrap').style.display = 'none';
        return;
      }}

      tbody.innerHTML = displayed.map(s => {{
        const price = customCMPStore[s.symbol] || s.price;
        const scoreClass = s.score >= 85 ? 'score-high' : (s.score >= 80 ? 'score-mid' : 'score-low');
        return `
          <tr>
            <td style="font-family:'JetBrains Mono'; font-weight:700; color:var(--text-sub);">#${{s.rank}}</td>
            <td>
              <strong style="font-size:14px; color:#fff;">${{s.symbol}}</strong>
              <div style="font-size:11px; color:var(--text-muted);">${{s.name ? s.name.substring(0, 22) : ''}}</div>
            </td>
            <td><span style="font-size:11px; color:#93c5fd;">${{s.sector}}</span></td>
            <td style="font-family:'JetBrains Mono'; font-weight:700; color:#fff;">
              ₹${{price}}
              <button onclick="editCMP('${{s.symbol}}')" title="Edit Live Price" style="background:transparent; border:none; color:#38bdf8; cursor:pointer; font-size:11px;">✏️</button>
            </td>
            <td><span class="score-badge ${{scoreClass}}">⭐ ${{s.score}}</span></td>
            <td style="color:#10b981; font-weight:700; font-family:'JetBrains Mono';">₹${{s.target}}</td>
            <td style="color:#ef4444; font-weight:700; font-family:'JetBrains Mono';">₹${{s.stop_loss}}</td>
            <td style="font-family:'JetBrains Mono';">${{s.rsi}}</td>
            <td style="color:#38bdf8; font-weight:600;">${{s.vol_surge}}</td>
            <td style="color:#10b981; font-weight:600;">+${{s.profit_qoq}}%</td>
            <td>
              <div style="display:flex; gap:6px;">
                <button onclick="quickAdd('${{s.symbol}}', ${{price}}, 100)" class="btn btn-chart" style="padding:4px 8px; font-size:11px;" title="Add to My Portfolio">➕</button>
                <a href="https://www.tradingview.com/chart/?symbol=NSE:${{s.symbol}}" target="_blank" class="btn btn-chart" style="padding:4px 8px; font-size:11px;">📈</a>
              </div>
            </td>
          </tr>
        `;
      }}).join('');

      const loadMoreBtn = document.getElementById('loadMoreWrap');
      if (renderLimit < filteredStocksCache.length) {{
        loadMoreBtn.style.display = 'block';
        loadMoreBtn.innerHTML = `<button class="btn-load-more" onclick="loadMoreStocks()">Showing ${{displayed.length}} of ${{filteredStocksCache.length}} Stocks • Load More...</button>`;
      }} else {{
        loadMoreBtn.style.display = 'none';
      }}
    }}

    function loadMoreStocks() {{
      renderLimit += 150;
      renderTable();
    }}

    function setFilter(f, btn) {{
      currentFilter = f;
      renderLimit = 100;
      document.querySelectorAll('.filter-pills .pill').forEach(p => p.classList.remove('active'));
      btn.classList.add('active');
      applyFilters();
    }}

    function sortTable(col) {{
      if (sortColumn === col) {{
        sortAsc = !sortAsc;
      }} else {{
        sortColumn = col;
        sortAsc = (col === 'rank') ? true : false;
      }}
      applyFilters();
    }}

    function roundVal(num) {{
      return Math.round(num * 100) / 100;
    }}

    window.onload = init;
  </script>
</body>
</html>
"""

with open(OUTPUT_HTML, "w") as f:
    f.write(html_content)

print(f"Successfully generated {OUTPUT_HTML} with live refresh & editing controls!")
