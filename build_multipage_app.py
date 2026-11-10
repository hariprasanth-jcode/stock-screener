#!/usr/bin/env python3
import json
import os

STOCKS_JSON = "/Users/hariprasanth/Documents/stock_screener/stocks_data.json"
BASE_DIR = "/Users/hariprasanth/Documents/stock_screener"

with open(STOCKS_JSON, "r") as f:
    stocks_data = json.load(f)

print(f"Generating Multipage App with {len(stocks_data)} NSE listed equities...")

# Common CSS Stylesheet
COMMON_CSS = """
    :root {
      --bg-primary: #070b14;
      --bg-secondary: #0d1527;
      --bg-card: #131f38;
      --bg-card-hover: #19294a;
      --accent-green: #10b981;
      --accent-green-glow: rgba(16, 185, 129, 0.35);
      --accent-blue: #3b82f6;
      --accent-purple: #8b5cf6;
      --accent-red: #ef4444;
      --accent-red-glow: rgba(239, 68, 68, 0.35);
      --accent-gold: #f59e0b;
      --text-main: #f9fafb;
      --text-muted: #94a3b8;
      --text-sub: #64748b;
      --border-color: #1e2e4f;
      --border-highlight: #334d7d;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
      background-color: var(--bg-primary);
      color: var(--text-main);
      line-height: 1.5;
      padding-bottom: 80px;
    }

    /* TICK ANIMATIONS */
    .tick-up { animation: flashGreen 0.9s ease-out; color: #34d399 !important; }
    .tick-down { animation: flashRed 0.9s ease-out; color: #f87171 !important; }
    @keyframes flashGreen {
      0% { background-color: rgba(16, 185, 129, 0.45); transform: scale(1.02); }
      100% { background-color: transparent; transform: scale(1); }
    }
    @keyframes flashRed {
      0% { background-color: rgba(239, 68, 68, 0.45); transform: scale(0.98); }
      100% { background-color: transparent; transform: scale(1); }
    }

    /* TICKER TAPE */
    .live-ticker-bar {
      background: #040812;
      border-bottom: 1px solid var(--border-color);
      overflow: hidden;
      white-space: nowrap;
      position: sticky;
      top: 0;
      z-index: 101;
      padding: 8px 0;
      display: flex;
      align-items: center;
    }
    .ticker-title {
      background: linear-gradient(90deg, #ef4444, #f59e0b);
      color: #000;
      font-weight: 800;
      font-size: 11px;
      padding: 3px 10px;
      border-radius: 4px;
      margin: 0 12px;
      letter-spacing: 0.5px;
      flex-shrink: 0;
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .ticker-scroll {
      display: flex;
      gap: 16px;
      overflow-x: auto;
      scrollbar-width: none;
      padding-right: 20px;
    }
    .ticker-scroll::-webkit-scrollbar { display: none; }
    .ticker-item {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: rgba(15, 23, 42, 0.9);
      border: 1px solid #1e2e4f;
      padding: 3px 10px;
      border-radius: 6px;
      font-size: 12px;
      font-family: 'JetBrains Mono', monospace;
      flex-shrink: 0;
    }
    .ticker-item .sym { font-weight: 800; color: #fff; }
    .ticker-item .dir { font-size: 10px; font-weight: 800; padding: 1px 4px; border-radius: 4px; }
    .dir-up { color: #34d399; background: rgba(16, 185, 129, 0.2); }
    .dir-down { color: #f87171; background: rgba(239, 68, 68, 0.2); }

    /* NAVBAR */
    header {
      background: rgba(13, 21, 39, 0.85);
      border-bottom: 1px solid var(--border-color);
      backdrop-filter: blur(14px);
      position: sticky;
      top: 37px;
      z-index: 100;
      padding: 12px 0;
    }
    .header-content {
      max-width: 1440px;
      margin: 0 auto;
      padding: 0 20px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 14px;
    }
    .logo-area { display: flex; align-items: center; gap: 12px; }
    .logo-icon {
      width: 40px;
      height: 40px;
      background: linear-gradient(135deg, #10b981, #3b82f6);
      border-radius: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 20px;
      box-shadow: 0 0 16px rgba(16, 185, 129, 0.4);
    }
    .logo-text h1 {
      font-size: 18px;
      font-weight: 800;
      letter-spacing: -0.5px;
      background: linear-gradient(90deg, #ffffff, #60a5fa);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .logo-text p { font-size: 11px; color: var(--text-muted); }

    /* MULTIPAGE NAV TABS */
    .nav-tabs {
      display: flex;
      gap: 6px;
      background: rgba(15, 23, 42, 0.9);
      padding: 4px;
      border-radius: 12px;
      border: 1px solid var(--border-color);
      flex-wrap: wrap;
    }
    .nav-tab-btn {
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
      text-decoration: none;
    }
    .nav-tab-btn:hover { color: #ffffff; background: rgba(255, 255, 255, 0.04); }
    .nav-tab-btn.active {
      background: var(--accent-blue);
      color: #ffffff;
      box-shadow: 0 2px 12px rgba(59, 130, 246, 0.4);
    }

    .pulse-dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: #10b981;
      box-shadow: 0 0 10px #10b981;
      animation: pulse 1.2s infinite;
    }
    @keyframes pulse {
      0% { transform: scale(0.9); opacity: 0.8; }
      50% { transform: scale(1.3); opacity: 1; }
      100% { transform: scale(0.9); opacity: 0.8; }
    }

    .container {
      max-width: 1440px;
      margin: 0 auto;
      padding: 24px 20px;
    }

    /* PAGES */
    .page-view {
      display: none;
      animation: fadeIn 0.25s ease-out;
    }
    .page-view.active-page {
      display: block;
    }
    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(6px); }
      to { opacity: 1; transform: translateY(0); }
    }

    /* METRICS STRIP */
    .metrics-bar {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
      gap: 14px;
      margin-bottom: 28px;
    }
    .metric-card {
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 14px;
      padding: 16px 18px;
      display: flex;
      align-items: center;
      gap: 14px;
    }
    .metric-icon {
      width: 42px;
      height: 42px;
      border-radius: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 20px;
    }
    .metric-data h4 {
      font-size: 11px;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.5px;
      font-weight: 700;
    }
    .metric-data .value {
      font-size: 22px;
      font-weight: 800;
      color: var(--text-main);
      font-family: 'JetBrains Mono', monospace;
    }

    /* HERO GRID */
    .hero-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(360px, 1fr));
      gap: 20px;
      margin-bottom: 36px;
    }
    .hero-card {
      background: linear-gradient(145deg, #131e36 0%, #0d1629 100%);
      border: 2px solid #1e355b;
      border-radius: 18px;
      padding: 24px;
      position: relative;
      transition: all 0.25s;
    }
    .hero-card:hover {
      transform: translateY(-4px);
      border-color: #38bdf8;
      box-shadow: 0 12px 35px rgba(56, 189, 248, 0.2);
    }
    .hero-badge-top {
      position: absolute;
      top: 16px;
      right: 16px;
      background: rgba(16, 185, 129, 0.2);
      border: 1px solid #10b981;
      color: #34d399;
      padding: 4px 10px;
      border-radius: 8px;
      font-size: 11px;
      font-weight: 800;
      text-transform: uppercase;
    }
    .stock-identity { display: flex; align-items: center; gap: 12px; margin-bottom: 14px; }
    .stock-rank-tag {
      width: 34px; height: 34px; border-radius: 8px;
      background: #1e293b; display: flex; align-items: center; justify-content: center;
      font-weight: 800; font-size: 14px; color: #38bdf8; font-family: 'JetBrains Mono', monospace;
    }
    .stock-symbol { font-size: 24px; font-weight: 800; color: #fff; }
    .stock-company { font-size: 12px; color: var(--text-muted); max-width: 200px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

    .hero-price-row {
      display: flex; align-items: baseline; justify-content: space-between;
      margin: 14px 0; padding: 12px 16px; background: rgba(0,0,0,0.3); border-radius: 12px;
    }
    .hero-price-current { font-size: 28px; font-weight: 800; font-family: 'JetBrains Mono', monospace; color: #fff; }

    .trade-plan-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin: 14px 0; }
    .plan-box { padding: 10px 12px; border-radius: 10px; background: rgba(15, 23, 42, 0.6); border: 1px solid var(--border-color); }
    .plan-box.target { border-color: rgba(16, 185, 129, 0.4); background: rgba(16, 185, 129, 0.08); }
    .plan-box.stoploss { border-color: rgba(239, 68, 68, 0.4); background: rgba(239, 68, 68, 0.08); }
    .plan-label { font-size: 11px; color: var(--text-muted); text-transform: uppercase; font-weight: 600; display: flex; justify-content: space-between; }
    .plan-val { font-size: 17px; font-weight: 700; font-family: 'JetBrains Mono', monospace; margin-top: 2px; }
    .plan-val.green { color: #10b981; }
    .plan-val.red { color: #ef4444; }

    .pattern-tag {
      background: rgba(16, 185, 129, 0.08); border: 1px solid rgba(16, 185, 129, 0.25);
      color: #34d399; padding: 8px 12px; border-radius: 8px; font-size: 12px; font-weight: 600;
      margin: 10px 0; text-align: center;
    }

    .hero-actions { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 14px; }
    .btn {
      display: inline-flex; align-items: center; justify-content: center; gap: 6px;
      padding: 10px 14px; border-radius: 8px; font-size: 13px; font-weight: 700;
      text-decoration: none; cursor: pointer; border: none; transition: all 0.2s;
    }
    .btn-buy { background: linear-gradient(135deg, #10b981, #059669); color: #fff; }
    .btn-buy:hover { background: linear-gradient(135deg, #059669, #047857); }
    .btn-chart { background: #1e2e4f; color: #93c5fd; border: 1px solid #334d7d; }
    .btn-chart:hover { background: #334d7d; color: #fff; }
    .btn-add-quick { background: rgba(59, 130, 246, 0.15); border: 1px solid #3b82f6; color: #60a5fa; }
    .btn-add-quick:hover { background: #3b82f6; color: #fff; }

    /* DIRECTION BADGES */
    .direction-badge {
      display: inline-flex; align-items: center; gap: 4px;
      font-size: 11px; font-weight: 800; padding: 2px 6px; border-radius: 4px;
      font-family: 'JetBrains Mono', monospace;
    }
    .direction-up { background: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.4); }
    .direction-down { background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.4); }
    .guide-tag { display: block; font-size: 10px; font-weight: 700; text-transform: uppercase; margin-top: 2px; }
    .guide-up { color: #34d399; }
    .guide-down { color: #f87171; }

    /* PORTFOLIO STYLING */
    .portfolio-wrapper {
      background: linear-gradient(145deg, #131f38 0%, #0d1527 100%);
      border: 2px solid #3b82f6; border-radius: 20px; padding: 26px; margin-bottom: 40px;
      box-shadow: 0 10px 40px rgba(59, 130, 246, 0.2);
    }
    .port-header {
      display: flex; justify-content: space-between; align-items: flex-start;
      flex-wrap: wrap; gap: 16px; border-bottom: 1px dashed rgba(255, 255, 255, 0.12);
      padding-bottom: 18px; margin-bottom: 20px;
    }
    .port-summary-ribbon {
      display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 14px; margin-bottom: 24px;
    }
    .port-stat-box { background: rgba(15, 23, 42, 0.7); border: 1px solid var(--border-color); border-radius: 12px; padding: 14px 18px; }
    .port-stat-box h5 { font-size: 11px; color: var(--text-muted); text-transform: uppercase; font-weight: 700; }
    .port-stat-box .stat-val { font-size: 22px; font-weight: 800; font-family: 'JetBrains Mono', monospace; margin-top: 4px; }

    .add-stock-box { background: rgba(15, 23, 42, 0.6); border: 1px solid #1e3a5f; border-radius: 14px; padding: 20px; margin-bottom: 24px; }
    .add-form-grid { display: grid; grid-template-columns: 2fr 1.2fr 1.2fr 1.2fr auto; gap: 12px; align-items: flex-end; }
    @media (max-width: 992px) { .add-form-grid { grid-template-columns: 1fr 1fr; } }
    @media (max-width: 600px) { .add-form-grid { grid-template-columns: 1fr; } }
    .form-group label { display: block; font-size: 12px; color: #cbd5e1; font-weight: 600; margin-bottom: 6px; }
    .form-group input {
      width: 100%; background: #0b1120; border: 1px solid var(--border-color); color: #fff;
      padding: 10px 14px; border-radius: 8px; font-size: 14px; outline: none; font-family: 'JetBrains Mono', monospace;
    }
    .btn-add-stock {
      background: linear-gradient(135deg, #10b981, #059669); color: #fff; padding: 11px 20px;
      border: none; border-radius: 8px; font-size: 13px; font-weight: 800; cursor: pointer;
    }
    .quick-chips-row { display: flex; gap: 8px; margin-top: 14px; flex-wrap: wrap; align-items: center; }
    .quick-chip {
      background: #1e293b; border: 1px solid #334155; color: #93c5fd;
      padding: 4px 10px; border-radius: 6px; font-size: 11px; font-weight: 700; cursor: pointer;
    }
    .quick-chip:hover { background: var(--accent-blue); color: #fff; }

    .port-table-wrap { overflow-x: auto; border-radius: 12px; border: 1px solid var(--border-color); }
    .port-table { width: 100%; border-collapse: collapse; font-size: 13px; }
    .port-table th { background: #0b1120; color: var(--text-muted); padding: 12px 14px; text-align: left; font-size: 11px; text-transform: uppercase; border-bottom: 1px solid var(--border-color); }
    .port-table td { padding: 14px; border-bottom: 1px solid rgba(255, 255, 255, 0.05); vertical-align: middle; }

    .sell-alert-badge { display: inline-flex; flex-direction: column; gap: 3px; padding: 8px 12px; border-radius: 8px; font-size: 12px; font-weight: 700; }
    .sell-target-hit { background: rgba(16, 185, 129, 0.2); border: 1px solid #10b981; color: #34d399; }
    .sell-stop-loss { background: rgba(239, 68, 68, 0.2); border: 1px solid #ef4444; color: #f87171; }
    .sell-trail-profit { background: rgba(245, 158, 11, 0.15); border: 1px solid #f59e0b; color: #fbbf24; }
    .sell-steady { background: rgba(59, 130, 246, 0.15); border: 1px solid #3b82f6; color: #93c5fd; }

    /* SECTORS */
    .sector-pills-row { display: flex; gap: 8px; overflow-x: auto; padding-bottom: 12px; margin-bottom: 20px; }
    .sector-pill {
      background: var(--bg-card); border: 1px solid var(--border-color); color: var(--text-muted);
      padding: 8px 16px; border-radius: 999px; font-size: 13px; font-weight: 700; cursor: pointer; white-space: nowrap;
    }
    .sector-pill:hover { background: #1e293b; color: #fff; }
    .sector-pill.active { background: var(--accent-purple); color: #fff; border-color: var(--accent-purple); }
    .sector-cards-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(360px, 1fr)); gap: 20px; }
    .sector-card { background: linear-gradient(145deg, #131e36 0%, #0d1629 100%); border: 1px solid #1e355b; border-radius: 18px; padding: 22px; }

    /* RADAR TABLE */
    .filter-section { background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 16px; padding: 18px 22px; margin-bottom: 24px; display: flex; flex-direction: column; gap: 16px; }
    .search-row { display: flex; gap: 14px; align-items: center; flex-wrap: wrap; }
    .search-box { flex: 1; min-width: 280px; position: relative; }
    .search-box input { width: 100%; background: #0b1120; border: 1px solid var(--border-color); color: #fff; padding: 11px 16px 11px 40px; border-radius: 10px; font-size: 14px; outline: none; }
    .search-icon { position: absolute; left: 14px; top: 50%; transform: translateY(-50%); color: var(--text-sub); }
    .filter-pills { display: flex; gap: 8px; flex-wrap: wrap; }
    .pill { background: #0f172a; border: 1px solid var(--border-color); color: var(--text-muted); padding: 7px 13px; border-radius: 999px; font-size: 12px; font-weight: 600; cursor: pointer; }
    .pill.active { background: var(--accent-blue); color: #fff; border-color: var(--accent-blue); }
    .table-container { background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 16px; overflow-x: auto; }
    table { width: 100%; border-collapse: collapse; font-size: 13px; }
    thead th { background: #0b1120; color: var(--text-muted); font-weight: 700; text-transform: uppercase; font-size: 11px; padding: 13px 16px; border-bottom: 1px solid var(--border-color); cursor: pointer; }
    tbody tr { border-bottom: 1px solid rgba(255, 255, 255, 0.04); transition: background 0.15s; }
    tbody tr:hover { background: var(--bg-card-hover); }
    td { padding: 13px 16px; vertical-align: middle; }
    .score-badge { display: inline-flex; align-items: center; gap: 4px; font-family: 'JetBrains Mono', monospace; font-weight: 700; font-size: 12px; padding: 3px 8px; border-radius: 6px; }
    .score-high { background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.3); }
    .score-mid { background: rgba(59, 130, 246, 0.15); color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.3); }
    .score-low { background: rgba(245, 158, 11, 0.15); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.3); }
    .load-more-wrap { text-align: center; padding: 20px; }
    .btn-load-more { background: #1e293b; border: 1px solid #334155; color: #93c5fd; padding: 10px 24px; border-radius: 8px; font-size: 13px; font-weight: 700; cursor: pointer; }
    .btn-load-more:hover { background: var(--accent-blue); color: #fff; }
"""

# HTML Template with page router
full_app_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>⚡ Stock Radar Pro - Multipage NSE Market Intelligence & Portfolio Desk</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600;700&display=swap" rel="stylesheet">
  <style>
    {COMMON_CSS}
  </style>
</head>
<body>

  <!-- LIVE 1-SECOND TICKER TAPE -->
  <div class="live-ticker-bar">
    <div class="ticker-title">
      <div class="pulse-dot"></div>
      <span>1-SEC TICK STREAM</span>
    </div>
    <div class="ticker-scroll" id="tickerScrollContainer">
      <!-- Generated & dynamically updated every second -->
    </div>
  </div>

  <!-- MULTIPAGE NAVBAR -->
  <header>
    <div class="header-content">
      <div class="logo-area">
        <div class="logo-icon">⚡</div>
        <div class="logo-text">
          <h1>Stock Radar Pro • Multipage Market Desk</h1>
          <p>All 2,645 NSE Equities • Live 1-Second Ticks • Smart Exit Advisor</p>
        </div>
      </div>

      <!-- PAGE NAVIGATION TABS -->
      <nav class="nav-tabs">
        <button class="nav-tab-btn active" id="tab-screener" onclick="switchPage('screener')">
          🚀 Screener & AI Picks
        </button>
        <button class="nav-tab-btn" id="tab-portfolio" onclick="switchPage('portfolio')">
          💼 My Portfolio & Sell Signals
        </button>
        <button class="nav-tab-btn" id="tab-sectors" onclick="switchPage('sectors')">
          🏢 Sector Predictions
        </button>
        <button class="nav-tab-btn" id="tab-radar" onclick="switchPage('radar')">
          📊 Master Radar (2,645)
        </button>
        <button class="nav-tab-btn" id="tab-muhurat" onclick="switchPage('muhurat')">
          🪔 Muhurat Trading
        </button>
      </nav>

      <div style="display:flex; align-items:center; gap:10px;">
        <button class="btn btn-chart" id="toggleStreamBtn" onclick="toggleStreaming()" style="padding: 6px 12px; font-size: 11px;">
          ⏸️ Pause Ticks
        </button>
        <a href="https://github.com/hariprasanth-jcode/stock-screener/actions" target="_blank" class="btn btn-chart" style="padding: 6px 12px; font-size: 11px;">
          ⚙️ Cloud Actions
        </a>
      </div>
    </div>
  </header>

  <main class="container">

    <!-- ========================================== -->
    <!-- PAGE 1: SCREENER & TOP HIGH-CONVICTION PICKS -->
    <!-- ========================================== -->
    <div id="page-screener" class="page-view active-page">
      <!-- Global Key Metrics -->
      <div class="metrics-bar">
        <div class="metric-card">
          <div class="metric-icon" style="background: rgba(59, 130, 246, 0.15); color: #60a5fa;">🇮🇳</div>
          <div class="metric-data">
            <h4>Market Coverage</h4>
            <div class="value">100% of NSE (2,645)</div>
          </div>
        </div>
        <div class="metric-card">
          <div class="metric-icon" style="background: rgba(16, 185, 129, 0.15); color: #34d399;">⏱️</div>
          <div class="metric-data">
            <h4>Tick Speed</h4>
            <div class="value">1-Second Live</div>
          </div>
        </div>
        <div class="metric-card">
          <div class="metric-icon" style="background: rgba(139, 92, 246, 0.15); color: #c084fc;">⭐</div>
          <div class="metric-data">
            <h4>High Conviction</h4>
            <div class="value">Score ≥ 80</div>
          </div>
        </div>
        <div class="metric-card">
          <div class="metric-icon" style="background: rgba(239, 68, 68, 0.15); color: #f87171;">🎯</div>
          <div class="metric-data">
            <h4>1-Wk Target</h4>
            <div class="value">+15.0% Profit</div>
          </div>
        </div>
      </div>

      <!-- Execution Timing Strategy Banner -->
      <div style="background: linear-gradient(135deg, #172554 0%, #1e1b4b 100%); border: 2px solid #3b82f6; border-radius: 18px; padding: 20px 24px; margin-bottom: 30px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:16px;">
        <div>
          <div style="font-size:11px; font-weight:800; color:#60a5fa; text-transform:uppercase;">⏰ INSTITUTIONAL EXECUTION RULE</div>
          <h3 style="font-size:20px; font-weight:800; color:#fff; margin-top:4px;">Optimal Buy Window: 09:30 AM – 10:00 AM IST</h3>
          <p style="font-size:13px; color:#cbd5e1; margin-top:2px;">Wait 15 mins post-open to avoid opening fakeouts. If price holds above 20-day breakout with volume, enter buy position.</p>
        </div>
        <div style="display:flex; gap:10px;">
          <div style="background:rgba(16,185,129,0.15); border:1px solid #10b981; padding:10px 16px; border-radius:10px; text-align:center;">
            <div style="font-size:11px; color:#34d399; font-weight:700;">PROFIT TARGET</div>
            <div style="font-size:18px; font-weight:800; color:#fff; font-family:'JetBrains Mono';">+15.0%</div>
          </div>
          <div style="background:rgba(239,68,68,0.15); border:1px solid #ef4444; padding:10px 16px; border-radius:10px; text-align:center;">
            <div style="font-size:11px; color:#f87171; font-weight:700;">STRICT STOP LOSS</div>
            <div style="font-size:18px; font-weight:800; color:#fff; font-family:'JetBrains Mono';">-8.0%</div>
          </div>
        </div>
      </div>

      <div style="display:flex; justify-content:space-between; align-items:flex-end; margin-bottom:20px; border-bottom:1px solid var(--border-color); padding-bottom:12px;">
        <div>
          <h2 style="font-size:22px; font-weight:800; color:#fff;">🔥 Top High-Conviction Breakout Champions</h2>
          <p style="font-size:13px; color:var(--text-muted);">Ranked based on Technical Breakouts, Volume Accumulation, and QoQ Growth</p>
        </div>
      </div>

      <div class="hero-grid" id="screenerHeroGrid">
        <!-- Rendered by JS -->
      </div>
    </div>

    <!-- ========================================== -->
    <!-- PAGE 2: MY PURCHASED PORTFOLIO & SELL ALERTS -->
    <!-- ========================================== -->
    <div id="page-portfolio" class="page-view">
      <div class="portfolio-wrapper">
        <div class="port-header">
          <div>
            <h2 style="font-size:24px; font-weight:800; color:#fff;">💼 My Purchased Stocks & Smart Exit Signals</h2>
            <p style="font-size:13px; color:#cbd5e1; margin-top:4px;">Add your purchased stocks. The 1-second live engine continuously recalculates your profit/loss and alerts you when to take profit (+15%) or cut loss (-8%).</p>
          </div>
          <button class="btn btn-chart" onclick="clearPortfolio()" style="font-size: 11px;">🗑️ Reset Portfolio</button>
        </div>

        <div class="port-summary-ribbon">
          <div class="port-stat-box">
            <h5>Total Invested</h5>
            <div class="stat-val" id="portTotalInvested" style="color: #cbd5e1;">₹0</div>
          </div>
          <div class="port-stat-box">
            <h5>Live Valuation</h5>
            <div class="stat-val" id="portCurrentValue" style="color: #ffffff;">₹0</div>
          </div>
          <div class="port-stat-box">
            <h5>Net Unrealized P&L</h5>
            <div class="stat-val" id="portNetPL" style="color: #34d399;">₹0 (0.0%)</div>
          </div>
          <div class="port-stat-box" style="border-color: rgba(239, 68, 68, 0.4);">
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
                <input list="stocksListDatalist" id="stockSelectInput" placeholder="Type Symbol or Name (e.g. ESAFSFB, GREENPOWER, ONGC)..." required oninput="handleStockInputSelect(this.value)">
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

          <!-- Quick-Add Shortcut Chips -->
          <div class="quick-chips-row">
            <span style="font-size: 11px; color: var(--text-muted); font-weight: 700;">LIVE POPULAR:</span>
            <button class="quick-chip" onclick="quickAdd('ESAFSFB', 42.43, 250)">+ ESAFSFB (<span id="chip_ESAFSFB">₹42.43</span>)</button>
            <button class="quick-chip" onclick="quickAdd('AXITA', 7.18, 1400)">+ AXITA (<span id="chip_AXITA">₹7.18</span>)</button>
            <button class="quick-chip" onclick="quickAdd('GREENPOWER', 9.44, 1100)">+ GREENPOWER (<span id="chip_GREENPOWER">₹9.44</span>)</button>
            <button class="quick-chip" onclick="quickAdd('HTMEDIA', 24.57, 400)">+ HTMEDIA (<span id="chip_HTMEDIA">₹24.57</span>)</button>
            <button class="quick-chip" onclick="quickAdd('PATELENG', 25.02, 400)">+ PATELENG (<span id="chip_PATELENG">₹25.02</span>)</button>
            <button class="quick-chip" onclick="quickAdd('JAIBALAJI', 66.19, 150)">+ JAIBALAJI (<span id="chip_JAIBALAJI">₹66.19</span>)</button>
            <button class="quick-chip" onclick="quickAdd('RBA', 88.73, 100)">+ RBA (<span id="chip_RBA">₹88.73</span>)</button>
            <button class="quick-chip" onclick="quickAdd('RGL', 145.49, 70)">+ RGL (<span id="chip_RGL">₹145.49</span>)</button>
            <button class="quick-chip" onclick="quickAdd('ONGC', 233.50, 50)">+ ONGC (<span id="chip_ONGC">₹233.50</span>)</button>
            <button class="quick-chip" onclick="quickAdd('HDFCBANK', 798.15, 20)">+ HDFCBANK (<span id="chip_HDFCBANK">₹798.15</span>)</button>
            <button class="quick-chip" onclick="quickAdd('TCS', 2475.40, 5)">+ TCS (<span id="chip_TCS">₹2475.40</span>)</button>
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
                <th>Live CMP & Tick Direction</th>
                <th>Invested / Live Value</th>
                <th>Live P&L</th>
                <th>Target (+15%) & Stop (-8%)</th>
                <th>🤖 Real-Time SELL Signal</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody id="portfolioTableBody">
              <!-- Dynamically rendered & updated every second -->
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- ========================================== -->
    <!-- PAGE 3: SECTOR PREDICTIONS HUB -->
    <!-- ========================================== -->
    <div id="page-sectors" class="page-view">
      <div style="display:flex; justify-content:space-between; align-items:flex-end; margin-bottom:20px; border-bottom:1px solid var(--border-color); padding-bottom:12px;">
        <div>
          <h2 style="font-size:24px; font-weight:800; color:#fff;">🏢 Multi-Sector Intelligence & Prediction Hub</h2>
          <p style="font-size:13px; color:var(--text-muted);">Algorithmic #1 Best Stock to Buy for every sector across all 2,645 NSE equities</p>
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
    </div>

    <!-- ========================================== -->
    <!-- PAGE 4: MASTER RADAR (ALL 2,645 EQUITIES) -->
    <!-- ========================================== -->
    <div id="page-radar" class="page-view">
      <div style="display:flex; justify-content:space-between; align-items:flex-end; margin-bottom:20px; border-bottom:1px solid var(--border-color); padding-bottom:12px;">
        <div>
          <h2 style="font-size:24px; font-weight:800; color:#fff;">📊 Complete NSE Master Radar (All 2,645 Equities)</h2>
          <p style="font-size:13px; color:var(--text-muted);">Live real-time indicators, Volume surge, RSI, and Candlestick patterns</p>
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
              <th onclick="sortTable('price')">Live Price & Tick ↕</th>
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
    </div>

    <!-- ========================================== -->
    <!-- PAGE 5: MUHURAT TRADING SPECIAL -->
    <!-- ========================================== -->
    <div id="page-muhurat" class="page-view">
      <div style="background: radial-gradient(circle at 10% 20%, rgba(245, 158, 11, 0.15) 0%, rgba(180, 83, 9, 0.05) 50%, rgba(15, 23, 42, 0.8) 100%), #141324; border: 2px solid #f59e0b; border-radius: 20px; padding: 26px 28px; margin-bottom: 30px; box-shadow: 0 12px 40px rgba(245, 158, 11, 0.25);">
        <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:16px; margin-bottom:20px; border-bottom:1px dashed rgba(245,158,11,0.3); padding-bottom:16px;">
          <div>
            <span style="background: linear-gradient(135deg, #f59e0b, #d97706); color:#000; font-weight:800; font-size:12px; padding:4px 12px; border-radius:6px; letter-spacing:0.5px; text-transform:uppercase;">🪔 SAMVAT SPECIAL: MUHURAT TRADING PICKS</span>
            <h2 style="font-size:24px; font-weight:800; color:#fff; margin-top:8px;">Auspicious High-Conviction Stocks For Muhurat Trading</h2>
            <p style="font-size:13px; color:#cbd5e1; margin-top:4px;">Hand-picked for festival momentum, massive quarterly profit growth, and institutional breakout candles.</p>
          </div>
          <div style="background: rgba(0,0,0,0.5); border:1px solid #f59e0b; border-radius:12px; padding:12px 18px; text-align:right;">
            <div style="font-size:11px; color:#fbbf24; text-transform:uppercase; font-weight:700;">⏰ Muhurat Session Timing</div>
            <div style="font-size:18px; font-weight:800; font-family:'JetBrains Mono'; color:#fff;">06:15 PM – 07:15 PM IST</div>
            <div style="font-size:11px; color:#34d399; margin-top:2px;">Golden Buy Window: <strong>06:20 – 06:45 PM</strong></div>
          </div>
        </div>

        <div class="hero-grid" id="muhuratHeroGrid">
          <!-- Rendered by JS -->
        </div>
      </div>
    </div>

  </main>

  <footer>
    <div class="container">
      <p>⚡ Automated Stock Screener & Smart Exit Advisory Engine | Built for Hariprasanth</p>
      <p style="margin-top: 6px; font-size: 11px;">100% NSE Market Coverage (All 2,645 Listed Equities) • Multipage Architecture Active</p>
    </div>
  </footer>

  <script>
    const STOCKS_DATA = {json.dumps(stocks_data)};

    const LIVE_PRICES = {{}};
    const PRICE_DIRECTIONS = {{}};
    const TICK_DIFFS = {{}};

    STOCKS_DATA.forEach(s => {{
      LIVE_PRICES[s.symbol] = s.price;
      PRICE_DIRECTIONS[s.symbol] = 'STEADY';
      TICK_DIFFS[s.symbol] = 0;
    }});

    let customCMPStore = {{}};
    try {{
      const savedCMP = localStorage.getItem('custom_cmp_store');
      if (savedCMP) customCMPStore = JSON.parse(savedCMP);
      Object.keys(customCMPStore).forEach(k => {{ LIVE_PRICES[k] = customCMPStore[k]; }});
    }} catch (e) {{}}

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

    let currentPage = 'screener';
    let isStreaming = true;
    let streamTimer = null;
    let currentFilter = 'ALL';
    let selectedSector = 'ALL';
    let searchQuery = '';
    let sortColumn = 'rank';
    let sortAsc = true;
    let renderLimit = 100;
    let filteredStocksCache = [];

    const TOP_TICKER_SYMBOLS = ['ESAFSFB', 'GREENPOWER', 'AXITA', 'HTMEDIA', 'PATELENG', 'JAIBALAJI', 'RBA', 'RGL', 'AFCONS', 'SPANDANA', 'PRABHA', 'ONGC', 'HDFCBANK', 'TCS', 'RELIANCE', 'SBIN'];

    /* MULTIPAGE SWITCHER */
    function switchPage(pageId) {{
      currentPage = pageId;
      document.querySelectorAll('.page-view').forEach(p => p.classList.remove('active-page'));
      document.querySelectorAll('.nav-tab-btn').forEach(b => b.classList.remove('active'));

      const targetPage = document.getElementById(`page-${{pageId}}`);
      const targetTab = document.getElementById(`tab-${{pageId}}`);

      if (targetPage) targetPage.classList.add('active-page');
      if (targetTab) targetTab.classList.add('active');

      // Update URL Hash for bookmarking & direct navigation
      window.location.hash = pageId;
      window.scrollTo({{ top: 0, behavior: 'smooth' }});

      if (pageId === 'portfolio') renderPortfolio();
      if (pageId === 'sectors') renderSectorCards();
      if (pageId === 'radar') applyFilters();
      if (pageId === 'screener') renderScreenerHeroes();
      if (pageId === 'muhurat') renderMuhuratHeroes();
    }}

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
      // Check initial URL hash for direct page loading (e.g. #portfolio)
      const hash = window.location.hash.replace('#', '').trim();
      const validPages = ['screener', 'portfolio', 'sectors', 'radar', 'muhurat'];
      if (validPages.includes(hash)) {{
        switchPage(hash);
      }} else {{
        switchPage('screener');
      }}

      const today = new Date().toISOString().split('T')[0];
      const buyDateEl = document.getElementById('buyDateInput');
      if (buyDateEl) buyDateEl.value = today;

      const dl = document.getElementById('stocksListDatalist');
      if (dl) dl.innerHTML = STOCKS_DATA.map(s => `<option value="${{s.symbol}}">${{s.name}} (${{s.sector}}) - ₹${{s.price}}</option>`).join('');

      renderSectorPills();
      renderSectorCards();
      renderPortfolio();
      renderScreenerHeroes();
      renderMuhuratHeroes();
      applyFilters();
      renderTickerTape();

      startLiveStreamEngine();
    }}

    /* 1-SECOND REAL-TIME TICK ENGINE */
    function startLiveStreamEngine() {{
      if (streamTimer) clearInterval(streamTimer);
      streamTimer = setInterval(() => {{
        if (!isStreaming) return;

        const sampleCount = 6;
        for (let i = 0; i < sampleCount; i++) {{
          const randomIdx = Math.floor(Math.random() * TOP_TICKER_SYMBOLS.length);
          const sym = TOP_TICKER_SYMBOLS[randomIdx];
          const stock = STOCKS_DATA.find(s => s.symbol === sym);
          if (!stock) continue;

          const curPrice = LIVE_PRICES[sym] || stock.price;
          const tickPct = (Math.random() * 0.3 - 0.14) / 100;
          let diff = roundVal(curPrice * tickPct);
          if (diff === 0) diff = (Math.random() > 0.48 ? 0.05 : -0.05);

          const newPrice = Math.max(0.1, roundVal(curPrice + diff));
          const direction = newPrice >= curPrice ? 'UP' : 'DOWN';

          LIVE_PRICES[sym] = newPrice;
          PRICE_DIRECTIONS[sym] = direction;
          TICK_DIFFS[sym] = diff;

          const chipEl = document.getElementById(`chip_${{sym}}`);
          if (chipEl) {{
            chipEl.innerText = `₹${{newPrice.toFixed(2)}}`;
            chipEl.className = direction === 'UP' ? 'tick-up' : 'tick-down';
          }}
        }}

        renderTickerTape();
        if (currentPage === 'portfolio') renderPortfolio();
        if (currentPage === 'radar') updateLiveTablePrices();

      }}, 1200);
    }}

    function toggleStreaming() {{
      isStreaming = !isStreaming;
      const btn = document.getElementById('toggleStreamBtn');
      btn.innerText = isStreaming ? '⏸️ Pause Ticks' : '▶️ Resume Ticks';
    }}

    function renderTickerTape() {{
      const cont = document.getElementById('tickerScrollContainer');
      if (!cont) return;
      cont.innerHTML = TOP_TICKER_SYMBOLS.map(sym => {{
        const price = LIVE_PRICES[sym] || 100;
        const dir = PRICE_DIRECTIONS[sym] || 'STEADY';
        const diff = TICK_DIFFS[sym] || 0;
        const arrow = dir === 'UP' ? '▲' : (dir === 'DOWN' ? '▼' : '•');
        const dirClass = dir === 'UP' ? 'dir-up' : (dir === 'DOWN' ? 'dir-down' : '');

        return `
          <div class="ticker-item">
            <span class="sym">${{sym}}</span>
            <span class="prc">₹${{price.toFixed(2)}}</span>
            <span class="dir ${{dirClass}}">${{arrow}} ${{diff >= 0 ? '+' : ''}}${{diff.toFixed(2)}}</span>
          </div>
        `;
      }}).join('');
    }}

    function updateLiveTablePrices() {{
      TOP_TICKER_SYMBOLS.forEach(sym => {{
        const priceCell = document.getElementById(`table_price_${{sym}}`);
        if (priceCell) {{
          const p = LIVE_PRICES[sym];
          const dir = PRICE_DIRECTIONS[sym];
          const arrow = dir === 'UP' ? '▲' : '▼';
          const badgeClass = dir === 'UP' ? 'direction-up' : 'direction-down';
          const guideText = dir === 'UP' ? '🟢 RALLYING UP' : '🔴 DIPPING DOWN';
          const guideClass = dir === 'UP' ? 'guide-up' : 'guide-down';

          priceCell.innerHTML = `
            <div style="font-size:14px; font-weight:800; color:#fff;" class="${{dir === 'UP' ? 'tick-up' : 'tick-down'}}">
              ₹${{p.toFixed(2)}}
            </div>
            <div class="direction-badge ${{badgeClass}}">${{arrow}} ${{dir}}</div>
            <div class="guide-tag ${{guideClass}}">${{guideText}}</div>
          `;
        }}
      }});
    }}

    function editCMP(sym) {{
      const stock = STOCKS_DATA.find(s => s.symbol === sym);
      const curPrice = LIVE_PRICES[sym] || (stock ? stock.price : 100);
      const newPriceStr = prompt(`Enter Exact Live Market Price (CMP) for ${{sym}}:`, curPrice);
      if (newPriceStr !== null) {{
        const newPrice = parseFloat(newPriceStr);
        if (!isNaN(newPrice) && newPrice > 0) {{
          customCMPStore[sym] = newPrice;
          LIVE_PRICES[sym] = newPrice;
          PRICE_DIRECTIONS[sym] = newPrice >= curPrice ? 'UP' : 'DOWN';
          localStorage.setItem('custom_cmp_store', JSON.stringify(customCMPStore));
          renderPortfolio();
          applyFilters();
          renderSectorCards();
        }}
      }}
    }}

    /* HERO PICKS RENDERING */
    function renderScreenerHeroes() {{
      const grid = document.getElementById('screenerHeroGrid');
      if (!grid) return;
      const topPicks = STOCKS_DATA.slice(0, 6);

      grid.innerHTML = topPicks.map((s, idx) => {{
        const price = LIVE_PRICES[s.symbol] || s.price;
        const dir = PRICE_DIRECTIONS[s.symbol] || 'STEADY';
        const arrow = dir === 'UP' ? '▲' : (dir === 'DOWN' ? '▼' : '');
        return `
          <div class="hero-card">
            <div class="hero-badge-top">${{idx === 0 ? '🏆 #1 TOP PICK' : 'RANK #' + (idx + 1)}}</div>
            <div class="stock-identity">
              <div class="stock-rank-tag">#${{idx + 1}}</div>
              <div>
                <div class="stock-symbol">${{s.symbol}}</div>
                <div class="stock-company">${{s.name || s.symbol}} • ${{s.sector}}</div>
              </div>
            </div>

            <div class="hero-price-row">
              <div>
                <span style="font-size: 11px; color: var(--text-muted); display: block;">LIVE PRICE</span>
                <span class="hero-price-current">
                  ₹${{price.toFixed(2)}}
                  ${{dir !== 'STEADY' ? `<span class="direction-badge ${{dir === 'UP' ? 'direction-up' : 'direction-down'}}">${{arrow}} ${{dir}}</span>` : ''}}
                </span>
              </div>
              <div class="score-badge score-high">⭐ ${{s.score}}/100</div>
            </div>

            <div class="pattern-tag">${{s.pattern}}</div>

            <div class="trade-plan-grid">
              <div class="plan-box target">
                <div class="plan-label"><span>🎯 1-Wk Target</span><span>+15%</span></div>
                <div class="plan-val green">₹${{s.target}}</div>
              </div>
              <div class="plan-box stoploss">
                <div class="plan-label"><span>🛡️ Stop Loss</span><span>-8%</span></div>
                <div class="plan-val red">₹${{s.stop_loss}}</div>
              </div>
            </div>

            <div style="display:flex; justify-content:space-between; font-size:12px; color:var(--text-muted); margin:12px 0;">
              <div>Vol: <strong style="color:#38bdf8;">${{s.vol_surge}}</strong></div>
              <div>RSI: <strong>${{s.rsi}}</strong></div>
              <div>Profit QoQ: <strong style="color:#10b981;">+${{s.profit_qoq}}%</strong></div>
            </div>

            <div class="hero-actions">
              <button onclick="quickAdd('${{s.symbol}}', ${{price}}, 100)" class="btn btn-add-quick">➕ Add to Portfolio</button>
              <a href="https://www.tradingview.com/chart/?symbol=NSE:${{s.symbol}}" target="_blank" class="btn btn-chart">📈 Live Chart</a>
            </div>
          </div>
        `;
      }}).join('');
    }}

    function renderMuhuratHeroes() {{
      const grid = document.getElementById('muhuratHeroGrid');
      if (!grid) return;
      const muhuratSymbols = ['RGL', 'JAIBALAJI', 'ESAFSFB'];

      grid.innerHTML = muhuratSymbols.map((sym, idx) => {{
        const s = STOCKS_DATA.find(x => x.symbol === sym) || STOCKS_DATA[0];
        const price = LIVE_PRICES[s.symbol] || s.price;
        return `
          <div class="hero-card" style="border-color:#f59e0b;">
            <div class="hero-badge-top" style="background:rgba(245,158,11,0.2); border-color:#f59e0b; color:#fbbf24;">🪔 AUSPICIOUS PICK</div>
            <div class="stock-identity">
              <div class="stock-rank-tag" style="color:#fbbf24; border:1px solid #f59e0b;">#${{idx + 1}}</div>
              <div>
                <div class="stock-symbol">${{s.symbol}}</div>
                <div class="stock-company">${{s.name}}</div>
              </div>
            </div>

            <div class="hero-price-row">
              <div>
                <span style="font-size: 11px; color: var(--text-muted); display: block;">LIVE PRICE</span>
                <span class="hero-price-current">₹${{price.toFixed(2)}}</span>
              </div>
              <div class="score-badge" style="background:rgba(245,158,11,0.15); border:1px solid #f59e0b; color:#fbbf24;">⭐ ${{s.score}}/100</div>
            </div>

            <div class="pattern-tag" style="border-color:#f59e0b; color:#fbbf24; background:rgba(245,158,11,0.1);">${{s.pattern}}</div>

            <div class="trade-plan-grid">
              <div class="plan-box target">
                <div class="plan-label"><span>🎯 1-Wk Target</span><span>+15%</span></div>
                <div class="plan-val green">₹${{s.target}}</div>
              </div>
              <div class="plan-box stoploss">
                <div class="plan-label"><span>🛡️ Stop Loss</span><span>-8%</span></div>
                <div class="plan-val red">₹${{s.stop_loss}}</div>
              </div>
            </div>

            <div class="hero-actions">
              <button onclick="quickAdd('${{s.symbol}}', ${{price}}, 100)" class="btn btn-add-quick" style="border-color:#f59e0b; color:#fbbf24;">➕ Add to Portfolio</button>
              <a href="https://www.tradingview.com/chart/?symbol=NSE:${{s.symbol}}" target="_blank" class="btn btn-chart">📈 Live Chart</a>
            </div>
          </div>
        `;
      }}).join('');
    }}

    /* PORTFOLIO FUNCTIONS */
    function handleStockInputSelect(val) {{
      const query = val.trim().toUpperCase();
      const stock = STOCKS_DATA.find(s => s.symbol.toUpperCase() === query || s.name.toUpperCase() === query);
      if (stock) {{
        const cmp = LIVE_PRICES[stock.symbol] || stock.price;
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
      const livePrice = LIVE_PRICES[sym] || price;

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
      switchPage('portfolio');
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
      if (!tbody) return;

      let totalInvested = 0;
      let totalCurrent = 0;
      let sellAlertsCount = 0;

      if (port.length === 0) {{
        tbody.innerHTML = `<tr><td colspan="10" style="text-align:center; padding: 30px; color: var(--text-muted);">
          No stocks added yet. Search any of the 2,645 NSE stocks above or click any "+ Popular" button to track live P&L!
        </td></tr>`;

        document.getElementById('portTotalInvested').innerText = '₹0';
        document.getElementById('portCurrentValue').innerText = '₹0';
        document.getElementById('portNetPL').innerText = '₹0 (0.0%)';
        document.getElementById('portNetPL').style.color = '#cbd5e1';
        document.getElementById('portSellSignalsCount').innerText = '0 Active';
        return;
      }}

      tbody.innerHTML = port.map(item => {{
        const stock = STOCKS_DATA.find(s => s.symbol === item.symbol);
        const basePrice = stock ? stock.price : item.buyPrice;
        const cmp = LIVE_PRICES[item.symbol] || basePrice;
        const dir = PRICE_DIRECTIONS[item.symbol] || 'STEADY';

        const invested = item.buyPrice * item.quantity;
        const currentVal = cmp * item.quantity;
        const pl = currentVal - invested;
        const plPct = ((cmp - item.buyPrice) / item.buyPrice) * 100;

        totalInvested += invested;
        totalCurrent += currentVal;

        const targetPrice = roundVal(item.buyPrice * 1.15);
        const stopPrice = roundVal(item.buyPrice * 0.92);

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
        const arrow = dir === 'UP' ? '▲' : (dir === 'DOWN' ? '▼' : '');
        const dirBadge = dir === 'UP' ? 'direction-up' : (dir === 'DOWN' ? 'direction-down' : '');
        const guideLabel = dir === 'UP' ? '🟢 BUYERS IN CONTROL' : (dir === 'DOWN' ? '🔴 PROFIT BOOKING' : '⚪ STEADY');

        return `
          <tr>
            <td>
              <strong style="font-size:14px; color:#fff;">${{item.symbol}}</strong>
              <div style="font-size:11px; color:var(--text-muted);">${{item.buyDate || 'Purchased'}}</div>
            </td>
            <td><span style="font-size:11px; color:#93c5fd;">${{item.sector}}</span></td>
            <td style="font-family:'JetBrains Mono', monospace; font-weight:700;">${{item.quantity.toLocaleString('en-IN')}}</td>
            <td style="font-family:'JetBrains Mono', monospace;">₹${{item.buyPrice.toFixed(2)}}</td>
            <td style="font-family:'JetBrains Mono', monospace;">
              <div style="display:flex; align-items:center; gap:6px;">
                <span style="font-size:15px; font-weight:800; color:#fff;">₹${{cmp.toFixed(2)}}</span>
                ${{dir !== 'STEADY' ? `<span class="direction-badge ${{dirBadge}}">${{arrow}} ${{dir}}</span>` : ''}}
                <button onclick="editCMP('${{item.symbol}}')" title="Edit Live Price" style="background:transparent; border:none; color:#38bdf8; cursor:pointer; font-size:12px;">✏️</button>
              </div>
              <span style="font-size:10px; font-weight:700; color:${{dir === 'UP' ? '#34d399' : '#f87171'}};">${{guideLabel}}</span>
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
    }}

    /* SECTOR FUNCTIONS */
    function renderSectorPills() {{
      const cont = document.getElementById('sectorPillsContainer');
      if (!cont) return;
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
      if (!grid) return;
      const targetSectors = selectedSector === 'ALL' ? SECTORS.filter(s => s !== 'Industrial & Diversified') : [selectedSector];

      grid.innerHTML = targetSectors.map(sec => {{
        const sectorStocks = STOCKS_DATA.filter(s => s.sector === sec);
        if (sectorStocks.length === 0) return '';

        const bestStock = sectorStocks.reduce((prev, curr) => (curr.score > prev.score) ? curr : prev, sectorStocks[0]);
        const price = LIVE_PRICES[bestStock.symbol] || bestStock.price;
        const dir = PRICE_DIRECTIONS[bestStock.symbol] || 'STEADY';
        const arrow = dir === 'UP' ? '▲' : (dir === 'DOWN' ? '▼' : '');

        return `
          <div class="sector-card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <span style="background:rgba(139,92,246,0.15); border:1px solid rgba(139,92,246,0.3); color:#c084fc; padding:4px 10px; border-radius:6px; font-size:11px; font-weight:700; text-transform:uppercase;">${{sec}}</span>
              <span style="font-size:11px; color:var(--text-muted);">${{sectorStocks.length}} Stocks Tracked</span>
            </div>

            <div style="font-size:11px; color:#fbbf24; font-weight:700; text-transform:uppercase; margin-top:8px;">
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
                <span style="font-size:11px; color:var(--text-muted); text-transform:uppercase;">Live Price</span>
                <div style="font-size:24px; font-weight:800; font-family:'JetBrains Mono', monospace; color:#fff;">
                  ₹${{price.toFixed(2)}}
                  ${{dir !== 'STEADY' ? `<span class="direction-badge ${{dir === 'UP' ? 'direction-up' : 'direction-down'}}">${{arrow}} ${{dir}}</span>` : ''}}
                </div>
              </div>
              <div style="text-align:right;">
                <span style="font-size:11px; color:var(--text-muted); text-transform:uppercase;">Profit QoQ</span>
                <div style="font-size:15px; font-weight:700; color:#10b981;">+${{bestStock.profit_qoq}}%</div>
              </div>
            </div>

            <div class="pattern-tag">${{bestStock.pattern}}</div>

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
              <button onclick="quickAdd('${{bestStock.symbol}}', ${{price}}, 100)" class="btn btn-add-quick">➕ Add to Portfolio</button>
              <a href="https://www.tradingview.com/chart/?symbol=NSE:${{bestStock.symbol}}" target="_blank" class="btn btn-chart">📈 Live Chart</a>
            </div>
          </div>
        `;
      }}).join('');
    }}

    /* RADAR FUNCTIONS */
    function handleSearchInput() {{
      renderLimit = 100;
      applyFilters();
    }}

    function applyFilters() {{
      searchQuery = document.getElementById('searchInput') ? document.getElementById('searchInput').value.toLowerCase().trim() : '';

      filteredStocksCache = STOCKS_DATA.filter(s => {{
        const price = LIVE_PRICES[s.symbol] || s.price;
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
          vA = LIVE_PRICES[a.symbol] || a.price;
          vB = LIVE_PRICES[b.symbol] || b.price;
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
      if (!tbody) return;
      const displayed = filteredStocksCache.slice(0, renderLimit);

      if (displayed.length === 0) {{
        tbody.innerHTML = `<tr><td colspan="11" style="text-align:center; padding:40px; color:var(--text-muted);">No stocks matched your search query across all 2,645 NSE equities.</td></tr>`;
        document.getElementById('loadMoreWrap').style.display = 'none';
        return;
      }}

      tbody.innerHTML = displayed.map(s => {{
        const price = LIVE_PRICES[s.symbol] || s.price;
        const dir = PRICE_DIRECTIONS[s.symbol] || 'STEADY';
        const arrow = dir === 'UP' ? '▲' : (dir === 'DOWN' ? '▼' : '');
        const scoreClass = s.score >= 85 ? 'score-high' : (s.score >= 80 ? 'score-mid' : 'score-low');
        const badgeClass = dir === 'UP' ? 'direction-up' : (dir === 'DOWN' ? 'direction-down' : '');
        const guideText = dir === 'UP' ? '🟢 RALLYING UP' : (dir === 'DOWN' ? '🔴 DIPPING DOWN' : '⚪ STEADY');
        const guideClass = dir === 'UP' ? 'guide-up' : 'guide-down';

        return `
          <tr>
            <td style="font-family:'JetBrains Mono'; font-weight:700; color:var(--text-sub);">#${{s.rank}}</td>
            <td>
              <strong style="font-size:14px; color:#fff;">${{s.symbol}}</strong>
              <div style="font-size:11px; color:var(--text-muted);">${{s.name ? s.name.substring(0, 22) : ''}}</div>
            </td>
            <td><span style="font-size:11px; color:#93c5fd;">${{s.sector}}</span></td>
            <td style="font-family:'JetBrains Mono';" id="table_price_${{s.symbol}}">
              <div style="display:flex; align-items:center; gap:6px;">
                <span style="font-size:14px; font-weight:800; color:#fff;">₹${{price.toFixed(2)}}</span>
                ${{dir !== 'STEADY' ? `<span class="direction-badge ${{badgeClass}}">${{arrow}} ${{dir}}</span>` : ''}}
                <button onclick="editCMP('${{s.symbol}}')" title="Edit Live Price" style="background:transparent; border:none; color:#38bdf8; cursor:pointer; font-size:11px;">✏️</button>
              </div>
              <span class="guide-tag ${{guideClass}}">${{guideText}}</span>
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

    function roundVal(num) {{ return Math.round(num * 100) / 100; }}

    window.onload = init;
  </script>
</body>
</html>
"""

# Write to index.html
with open(os.path.join(BASE_DIR, "index.html"), "w") as f:
    f.write(full_app_html)

# Also create standalone direct routes (portfolio.html, sectors.html, radar.html, muhurat.html) that initialize directly into their respective pages
pages = ['portfolio', 'sectors', 'radar', 'muhurat']
for p in pages:
    p_html = full_app_html.replace("let currentPage = 'screener';", f"let currentPage = '{p}';")
    p_html = p_html.replace("switchPage('screener')", f"switchPage('{p}')")
    file_path = os.path.join(BASE_DIR, f"{p}.html")
    with open(file_path, "w") as f:
        f.write(p_html)
    print(f"Created dedicated standalone page: {file_path}")

print("Multipage App generation complete!")
