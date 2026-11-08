#!/usr/bin/env python3
import json
import os

STOCKS_JSON = "/Users/hariprasanth/Documents/stock_screener/stocks_data.json"
OUTPUT_HTML = "/Users/hariprasanth/Documents/stock_screener/index.html"

with open(STOCKS_JSON, "r") as f:
    stocks_data = json.load(f)

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>⚡ Stock Radar Pro - High-Conviction Swing Screener (&lt; ₹250)</title>
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
      max-width: 1400px;
      margin: 0 auto;
      padding: 24px 20px;
    }}

    /* Header Bar */
    header {{
      background: linear-gradient(180deg, #131c31 0%, rgba(19, 28, 49, 0.7) 100%);
      border-bottom: 1px solid var(--border-color);
      backdrop-filter: blur(12px);
      position: sticky;
      top: 0;
      z-index: 100;
      padding: 16px 0;
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
      width: 42px;
      height: 42px;
      background: linear-gradient(135deg, #10b981, #06b6d4);
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 22px;
      box-shadow: 0 0 20px rgba(16, 185, 129, 0.4);
    }}

    .logo-text h1 {{
      font-size: 20px;
      font-weight: 800;
      letter-spacing: -0.5px;
      background: linear-gradient(90deg, #ffffff, #cbd5e1);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}

    .logo-text p {{
      font-size: 12px;
      color: var(--text-muted);
    }}

    .status-badge {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: rgba(16, 185, 129, 0.12);
      border: 1px solid rgba(16, 185, 129, 0.3);
      padding: 6px 14px;
      border-radius: 999px;
      font-size: 13px;
      font-weight: 600;
      color: #34d399;
    }}

    .status-dot {{
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: #10b981;
      box-shadow: 0 0 10px #10b981;
      animation: pulse 2s infinite;
    }}

    @keyframes pulse {{
      0% {{ transform: scale(0.95); opacity: 0.8; }}
      50% {{ transform: scale(1.2); opacity: 1; }}
      100% {{ transform: scale(0.95); opacity: 0.8; }}
    }}

    /* Timing Strategy Guide Card */
    .timing-banner {{
      background: linear-gradient(135deg, #172554 0%, #1e1b4b 100%);
      border: 2px solid #3b82f6;
      border-radius: 18px;
      padding: 22px 26px;
      margin: 24px 0 28px 0;
      box-shadow: 0 10px 30px rgba(59, 130, 246, 0.2);
      display: grid;
      grid-template-columns: 1.1fr 2fr;
      gap: 24px;
      align-items: center;
    }}

    @media (max-width: 960px) {{
      .timing-banner {{
        grid-template-columns: 1fr;
      }}
    }}

    .timing-badge-title {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: rgba(59, 130, 246, 0.2);
      color: #60a5fa;
      border: 1px solid rgba(59, 130, 246, 0.4);
      padding: 4px 12px;
      border-radius: 8px;
      font-size: 12px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      margin-bottom: 10px;
    }}

    .timing-banner h3 {{
      font-size: 22px;
      font-weight: 800;
      color: #ffffff;
      line-height: 1.3;
    }}

    .timing-banner p {{
      font-size: 13px;
      color: #cbd5e1;
      margin-top: 6px;
    }}

    .timing-boxes-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
      gap: 14px;
    }}

    .time-slot-box {{
      background: rgba(15, 23, 42, 0.7);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 12px;
      padding: 14px 16px;
      transition: all 0.2s;
    }}

    .time-slot-box.recommended {{
      border-color: #10b981;
      background: rgba(16, 185, 129, 0.1);
    }}

    .time-slot-box h4 {{
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      font-weight: 700;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}

    .time-slot-box.recommended h4 {{ color: #34d399; }}
    .time-slot-box.secondary h4 {{ color: #60a5fa; }}
    .time-slot-box.danger h4 {{ color: #f87171; }}

    .time-slot-box .time-window {{
      font-size: 17px;
      font-weight: 800;
      font-family: 'JetBrains Mono', monospace;
      color: #ffffff;
      margin: 6px 0 4px 0;
    }}

    .time-slot-box .time-desc {{
      font-size: 11px;
      color: var(--text-muted);
      line-height: 1.4;
    }}

    /* Metrics Bar */
    .metrics-bar {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 16px;
      margin: 0 0 32px 0;
    }}

    .metric-card {{
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 14px;
      padding: 16px 20px;
      display: flex;
      align-items: center;
      gap: 16px;
      transition: all 0.2s;
    }}

    .metric-card:hover {{
      border-color: var(--border-highlight);
      transform: translateY(-2px);
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
      font-size: 12px;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.5px;
      font-weight: 600;
    }}

    .metric-data .value {{
      font-size: 22px;
      font-weight: 800;
      color: var(--text-main);
      font-family: 'JetBrains Mono', monospace;
    }}

    /* Section Title */
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

    /* Priority Hero Grid */
    .hero-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(360px, 1fr));
      gap: 20px;
      margin-bottom: 40px;
    }}

    .hero-card {{
      background: linear-gradient(145deg, #162238 0%, #111a2c 100%);
      border: 2px solid #1e3a5f;
      border-radius: 18px;
      padding: 24px;
      position: relative;
      overflow: hidden;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
      transition: all 0.25s ease;
      cursor: pointer;
    }}

    .hero-card:hover {{
      transform: translateY(-4px);
      border-color: #38bdf8;
      box-shadow: 0 15px 40px rgba(56, 189, 248, 0.2);
    }}

    .hero-card.rank-1 {{
      border-color: #10b981;
      background: linear-gradient(145deg, #0e2926 0%, #0d1e25 100%);
      box-shadow: 0 10px 35px rgba(16, 185, 129, 0.25);
    }}

    .hero-badge-top {{
      position: absolute;
      top: 16px;
      right: 16px;
      background: rgba(16, 185, 129, 0.2);
      border: 1px solid #10b981;
      color: #34d399;
      padding: 4px 10px;
      border-radius: 8px;
      font-size: 12px;
      font-weight: 700;
      letter-spacing: 0.5px;
      text-transform: uppercase;
    }}

    .stock-identity {{
      display: flex;
      align-items: center;
      gap: 12px;
      margin-bottom: 16px;
    }}

    .stock-rank-tag {{
      width: 34px;
      height: 34px;
      border-radius: 8px;
      background: #1e293b;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 800;
      font-size: 14px;
      color: #38bdf8;
      font-family: 'JetBrains Mono', monospace;
    }}

    .stock-symbol {{
      font-size: 24px;
      font-weight: 800;
      color: #ffffff;
      letter-spacing: -0.5px;
    }}

    .stock-company {{
      font-size: 13px;
      color: var(--text-muted);
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      max-width: 200px;
    }}

    .hero-price-row {{
      display: flex;
      align-items: baseline;
      justify-content: space-between;
      margin: 16px 0;
      padding: 12px 16px;
      background: rgba(0, 0, 0, 0.25);
      border-radius: 12px;
      border: 1px solid rgba(255, 255, 255, 0.05);
    }}

    .hero-price-current {{
      font-size: 28px;
      font-weight: 800;
      font-family: 'JetBrains Mono', monospace;
      color: #ffffff;
    }}

    .hero-score-pill {{
      display: flex;
      align-items: center;
      gap: 6px;
      font-weight: 700;
      font-size: 14px;
      padding: 4px 10px;
      border-radius: 8px;
      background: rgba(16, 185, 129, 0.15);
      color: #34d399;
      border: 1px solid rgba(16, 185, 129, 0.3);
    }}

    /* Card Timing Box */
    .card-timing-box {{
      background: rgba(59, 130, 246, 0.12);
      border: 1px solid rgba(59, 130, 246, 0.3);
      border-radius: 10px;
      padding: 10px 14px;
      margin: 12px 0;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}

    .card-timing-box .timing-tag {{
      font-size: 11px;
      color: #93c5fd;
      font-weight: 700;
      text-transform: uppercase;
    }}

    .card-timing-box .timing-val {{
      font-size: 13px;
      font-weight: 800;
      color: #ffffff;
      font-family: 'JetBrains Mono', monospace;
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

    .pattern-tag {{
      display: block;
      background: rgba(16, 185, 129, 0.08);
      border: 1px solid rgba(16, 185, 129, 0.25);
      color: #34d399;
      padding: 8px 12px;
      border-radius: 8px;
      font-size: 12px;
      font-weight: 600;
      margin: 10px 0;
      text-align: center;
    }}

    .hero-meta-row {{
      display: flex;
      justify-content: space-between;
      font-size: 12px;
      color: var(--text-muted);
      margin: 12px 0 18px 0;
      padding: 8px 0;
      border-top: 1px dashed rgba(255, 255, 255, 0.1);
      border-bottom: 1px dashed rgba(255, 255, 255, 0.1);
    }}

    .hero-actions {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
    }}

    .btn {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      padding: 10px 14px;
      border-radius: 10px;
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
      box-shadow: 0 4px 15px rgba(16, 185, 129, 0.35);
    }}

    .btn-buy:hover {{
      background: linear-gradient(135deg, #059669, #047857);
      transform: translateY(-2px);
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

    /* Position Calculator Box */
    .calc-card {{
      background: linear-gradient(135deg, #1e1e38 0%, #151b2e 100%);
      border: 1px solid #3730a3;
      border-radius: 16px;
      padding: 24px;
      margin-bottom: 40px;
      display: grid;
      grid-template-columns: 1fr 2fr;
      gap: 24px;
      align-items: center;
    }}

    @media (max-width: 900px) {{
      .calc-card {{
        grid-template-columns: 1fr;
      }}
    }}

    .calc-input-group label {{
      display: block;
      font-size: 13px;
      color: #c7d2fe;
      font-weight: 600;
      margin-bottom: 8px;
    }}

    .calc-input-group input {{
      width: 100%;
      background: #0f172a;
      border: 1px solid #4338ca;
      color: #ffffff;
      padding: 12px 16px;
      border-radius: 10px;
      font-size: 18px;
      font-family: 'JetBrains Mono', monospace;
      font-weight: 700;
      outline: none;
    }}

    .calc-chips {{
      display: flex;
      gap: 8px;
      margin-top: 10px;
      flex-wrap: wrap;
    }}

    .calc-chip {{
      background: #312e81;
      color: #c7d2fe;
      border: none;
      padding: 4px 10px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      transition: background 0.15s;
    }}

    .calc-chip:hover {{
      background: #4338ca;
      color: #ffffff;
    }}

    .calc-output-grid {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 16px;
      background: rgba(15, 23, 42, 0.7);
      padding: 20px;
      border-radius: 12px;
      border: 1px solid rgba(255, 255, 255, 0.05);
    }}

    @media (max-width: 600px) {{
      .calc-output-grid {{
        grid-template-columns: 1fr;
      }}
    }}

    .calc-res-item h5 {{
      font-size: 11px;
      color: var(--text-muted);
      text-transform: uppercase;
      font-weight: 600;
    }}

    .calc-res-item p {{
      font-size: 20px;
      font-weight: 800;
      font-family: 'JetBrains Mono', monospace;
      margin-top: 4px;
    }}

    /* Filter & Search Bar */
    .filter-section {{
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 16px;
      padding: 18px 24px;
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
      padding: 12px 16px 12px 42px;
      border-radius: 10px;
      font-size: 14px;
      outline: none;
      transition: border-color 0.2s;
    }}

    .search-box input:focus {{
      border-color: var(--accent-blue);
    }}

    .search-icon {{
      position: absolute;
      left: 14px;
      top: 50%;
      transform: translateY(-50%);
      color: var(--text-sub);
      font-size: 16px;
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
      padding: 8px 14px;
      border-radius: 999px;
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s;
    }}

    .pill:hover {{
      background: #1e293b;
      color: #ffffff;
    }}

    .pill.active {{
      background: var(--accent-blue);
      color: #ffffff;
      border-color: var(--accent-blue);
    }}

    /* Table Design */
    .table-container {{
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 16px;
      overflow-x: auto;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    }}

    table {{
      width: 100%;
      border-collapse: collapse;
      text-align: left;
      font-size: 13px;
    }}

    thead th {{
      background: #0f172a;
      color: var(--text-muted);
      font-weight: 700;
      text-transform: uppercase;
      font-size: 11px;
      letter-spacing: 0.5px;
      padding: 14px 16px;
      border-bottom: 1px solid var(--border-color);
      position: sticky;
      top: 0;
      cursor: pointer;
      user-select: none;
    }}

    thead th:hover {{
      color: #ffffff;
    }}

    tbody tr {{
      border-bottom: 1px solid rgba(255, 255, 255, 0.04);
      transition: background 0.15s;
    }}

    tbody tr:hover {{
      background: var(--bg-card-hover);
    }}

    td {{
      padding: 14px 16px;
      vertical-align: middle;
    }}

    .rank-cell {{
      font-family: 'JetBrains Mono', monospace;
      font-weight: 700;
      color: var(--text-sub);
    }}

    .symbol-cell {{
      font-weight: 700;
      font-size: 14px;
      color: #ffffff;
    }}

    .symbol-cell span {{
      display: block;
      font-size: 11px;
      color: var(--text-muted);
      font-weight: 400;
    }}

    .price-cell {{
      font-family: 'JetBrains Mono', monospace;
      font-weight: 700;
      font-size: 14px;
      color: #ffffff;
    }}

    .score-badge {{
      display: inline-flex;
      align-items: center;
      gap: 4px;
      font-family: 'JetBrains Mono', monospace;
      font-weight: 700;
      font-size: 13px;
      padding: 3px 8px;
      border-radius: 6px;
    }}

    .score-high {{
      background: rgba(16, 185, 129, 0.15);
      color: #34d399;
      border: 1px solid rgba(16, 185, 129, 0.3);
    }}

    .score-mid {{
      background: rgba(59, 130, 246, 0.15);
      color: #60a5fa;
      border: 1px solid rgba(59, 130, 246, 0.3);
    }}

    .score-low {{
      background: rgba(245, 158, 11, 0.15);
      color: #fbbf24;
      border: 1px solid rgba(245, 158, 11, 0.3);
    }}

    .table-btn {{
      padding: 6px 10px;
      font-size: 11px;
      font-weight: 600;
      border-radius: 6px;
      background: #1e293b;
      color: #93c5fd;
      border: 1px solid #334155;
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      gap: 4px;
    }}

    .table-btn:hover {{
      background: #334155;
      color: #ffffff;
    }}

    /* Footer info */
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

  <!-- Top Navigation -->
  <header>
    <div class="container header-content">
      <div class="logo-area">
        <div class="logo-icon">📈</div>
        <div class="logo-text">
          <h1>⚡ NSE High-Conviction Stock Screener</h1>
          <p>Filtered for &lt; ₹250 | 1-Week Swing Trading (+15% Target, -8% Stop Loss)</p>
        </div>
      </div>
      <div style="display: flex; gap: 12px; align-items: center; flex-wrap: wrap;">
        <div class="status-badge">
          <div class="status-dot"></div>
          <span>Cloud Monitor Active (9:15 AM - 3:30 PM IST)</span>
        </div>
        <a href="https://github.com/hariprasanth-jcode/stock-screener/actions" target="_blank" class="btn btn-chart" style="padding: 6px 12px; font-size: 12px;">
          ⚙️ GitHub Actions
        </a>
      </div>
    </div>
  </header>

  <main class="container">

    <!-- Timing & Execution Strategy Banner -->
    <div class="timing-banner">
      <div>
        <div class="timing-badge-title">⏰ PRECISION EXECUTION TIMING</div>
        <h3>When Exactly To Buy For Maximum Profit</h3>
        <p>Follow the institutional 15-minute rule to filter false opening spikes and lock in high-probability 1-week gains.</p>
        <div style="margin-top: 14px; font-size: 13px; color: #93c5fd; font-weight: 600;">
          📅 Target Entry Date: <span style="color: #ffffff; background: rgba(59,130,246,0.3); padding: 3px 8px; border-radius: 6px;">Monday, Nov 9, 2026</span>
          <br>⏳ Target Exit Date: <span style="color: #34d399;">Friday, Nov 13, 2026</span> (or when +15% target is hit)
        </div>
      </div>

      <div class="timing-boxes-grid">
        <div class="time-slot-box recommended">
          <h4>
            <span>🏆 Best Entry Window</span>
            <span>⭐ HIGH WIN-RATE</span>
          </h4>
          <div class="time-window">09:30 AM – 10:00 AM</div>
          <div class="time-desc">Wait 15 mins after 9:15 open. If price holds above breakout level with sustained volume, execute BUY.</div>
        </div>

        <div class="time-slot-box secondary">
          <h4>
            <span>🕒 Secondary Window</span>
            <span>EOD MOMENTUM</span>
          </h4>
          <div class="time-window">02:30 PM – 03:15 PM</div>
          <div class="time-desc">Confirm daily closing candle strength. Perfect for high-volume breakouts closing near day highs.</div>
        </div>

        <div class="time-slot-box danger">
          <h4>
            <span>⚠️ Danger Zone</span>
            <span>DO NOT BUY</span>
          </h4>
          <div class="time-window">09:15 AM – 09:25 AM</div>
          <div class="time-desc">Initial 10-minute noise, gap-up traps & quick profit booking. Wait for the 15-min candle confirmation.</div>
        </div>
      </div>
    </div>

    <!-- Top Key Metrics -->
    <div class="metrics-bar">
      <div class="metric-card">
        <div class="metric-icon" style="background: rgba(59, 130, 246, 0.15); color: #60a5fa;">🏢</div>
        <div class="metric-data">
          <h4>Total Scanned</h4>
          <div class="value">2,630+</div>
        </div>
      </div>
      <div class="metric-card">
        <div class="metric-icon" style="background: rgba(16, 185, 129, 0.15); color: #34d399;">🎯</div>
        <div class="metric-data">
          <h4>Filtered (&lt; ₹250)</h4>
          <div class="value" id="filteredCount">517</div>
        </div>
      </div>
      <div class="metric-card">
        <div class="metric-icon" style="background: rgba(245, 158, 11, 0.15); color: #fbbf24;">⭐</div>
        <div class="metric-data">
          <h4>Conviction (≥ 80)</h4>
          <div class="value" id="highConvictionCount">0</div>
        </div>
      </div>
      <div class="metric-card">
        <div class="metric-icon" style="background: rgba(139, 92, 246, 0.15); color: #a78bfa;">📩</div>
        <div class="metric-data">
          <h4>Alerts Target</h4>
          <div class="value" style="font-size: 14px; line-height: 28px;">hari.mba000@gmail.com</div>
        </div>
      </div>
    </div>

    <!-- Section 1: Hero Top Priority Stocks (Immediate Buy Conviction) -->
    <div class="section-header">
      <div>
        <h2 class="section-title">🔥 INVEST NOW: Top Priority High-Conviction Picks</h2>
        <p class="section-subtitle">Ranked #1 to #6 based on Technical Breakouts, Candlestick Patterns, and QoQ Growth</p>
      </div>
    </div>

    <div class="hero-grid" id="heroGrid">
      <!-- Generated via JS -->
    </div>

    <!-- Section 2: Interactive Position Sizer / Profit Calculator -->
    <div class="calc-card">
      <div class="calc-input-group">
        <label for="investInput">💰 1-Week Trade Profit Calculator</label>
        <input type="number" id="investInput" value="25000" step="1000" />
        <div class="calc-chips">
          <button class="calc-chip" onclick="setCalcAmount(10000)">₹10,000</button>
          <button class="calc-chip" onclick="setCalcAmount(25000)">₹25,000</button>
          <button class="calc-chip" onclick="setCalcAmount(50000)">₹50,000</button>
          <button class="calc-chip" onclick="setCalcAmount(100000)">₹1,00,000</button>
        </div>
        <div style="margin-top: 10px; font-size: 12px; color: var(--text-muted);">
          Selected Stock: <strong id="calcSelectedStock" style="color: #38bdf8;">ESAFSFB (₹42.21)</strong>
        </div>
      </div>
      <div class="calc-output-grid">
        <div class="calc-res-item">
          <h5>Shares You Can Buy</h5>
          <p id="calcShares" style="color: #38bdf8;">592</p>
        </div>
        <div class="calc-res-item">
          <h5>Projected Gain (+15%)</h5>
          <p id="calcProfit" style="color: #10b981;">+₹3,750</p>
        </div>
        <div class="calc-res-item">
          <h5>Max Loss at Stop (-8%)</h5>
          <p id="calcLoss" style="color: #ef4444;">-₹2,000</p>
        </div>
      </div>
    </div>

    <!-- Section 3: Full Filterable Radar Table -->
    <div class="section-header">
      <div>
        <h2 class="section-title">📊 Complete Stock Radar Table</h2>
        <p class="section-subtitle">Real-time indicators, Volume surge, RSI, and Candlestick patterns</p>
      </div>
    </div>

    <div class="filter-section">
      <div class="search-row">
        <div class="search-box">
          <span class="search-icon">🔍</span>
          <input type="text" id="searchInput" placeholder="Search by Symbol (e.g. ESAFSFB, RBA, JAIBALAJI, ONGC)..." oninput="applyFilters()" />
        </div>
      </div>
      <div class="filter-pills">
        <button class="pill active" onclick="setFilter('ALL', this)">All Stocks (517)</button>
        <button class="pill" onclick="setFilter('SCORE_85', this)">🔥 Score ≥ 85 (Top Conviction)</button>
        <button class="pill" onclick="setFilter('SCORE_80', this)">⭐ Score ≥ 80</button>
        <button class="pill" onclick="setFilter('PRICE_50', this)">Under ₹50</button>
        <button class="pill" onclick="setFilter('PRICE_100', this)">Under ₹100</button>
        <button class="pill" onclick="setFilter('PATTERN_BREAKOUT', this)">🔥 20-Day Breakout</button>
        <button class="pill" onclick="setFilter('PATTERN_ENGULFING', this)">🟢 Bullish Engulfing</button>
      </div>
    </div>

    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th onclick="sortTable('rank')">Rank ↕</th>
            <th onclick="sortTable('symbol')">Stock Symbol ↕</th>
            <th onclick="sortTable('price')">Price ↕</th>
            <th onclick="sortTable('score')">Score ↕</th>
            <th>Buy Timing</th>
            <th>1-Wk Target (+15%)</th>
            <th>Stop Loss (-8%)</th>
            <th onclick="sortTable('rsi')">RSI ↕</th>
            <th>Vol Surge</th>
            <th>Profit QoQ</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody id="stocksTableBody">
          <!-- Filled by JS -->
        </tbody>
      </table>
    </div>

  </main>

  <footer>
    <div class="container">
      <p>⚡ Automated Stock Screener & Real-Time Alert Engine | Built for Hariprasanth</p>
      <p style="margin-top: 6px; font-size: 11px;">Target Holding: 1-Week (Nov 9 – Nov 13, 2026) | Active Cloud Monitor: 9:15 AM - 3:30 PM IST</p>
    </div>
  </footer>

  <script>
    // Embedded 517 Stock Records
    const STOCKS_DATA = {json.dumps(stocks_data)};

    let currentFilter = 'ALL';
    let searchQuery = '';
    let sortColumn = 'rank';
    let sortAsc = true;
    let selectedCalcStock = STOCKS_DATA[0];

    function init() {{
      const highConviction = STOCKS_DATA.filter(s => (s.score || 0) >= 80).length;
      document.getElementById('highConvictionCount').innerText = highConviction;
      document.getElementById('filteredCount').innerText = STOCKS_DATA.length;

      renderHeroGrid();
      applyFilters();
      updateCalculator();
    }}

    function renderHeroGrid() {{
      const heroContainer = document.getElementById('heroGrid');
      const topPicks = STOCKS_DATA.slice(0, 6);

      heroContainer.innerHTML = topPicks.map((s, idx) => `
        <div class="hero-card ${{idx === 0 ? 'rank-1' : ''}}" onclick="selectStockForCalc('${{s.symbol}}')">
          <div class="hero-badge-top">${{idx === 0 ? '🏆 #1 TOP PICK' : 'RANK #' + (idx + 1)}}</div>
          <div class="stock-identity">
            <div class="stock-rank-tag">#${{idx + 1}}</div>
            <div>
              <div class="stock-symbol">${{s.symbol}}</div>
              <div class="stock-company">${{s.name || s.symbol}}</div>
            </div>
          </div>

          <div class="hero-price-row">
            <div>
              <span style="font-size: 11px; color: var(--text-muted); display: block; text-transform: uppercase;">Current Price</span>
              <span class="hero-price-current">₹${{s.price}}</span>
            </div>
            <div class="hero-score-pill">
              ⭐ ${{s.score}}/100
            </div>
          </div>

          <!-- Explicit Date & Time Window -->
          <div class="card-timing-box">
            <div>
              <div class="timing-tag">📅 Buy Date</div>
              <div class="timing-val" style="color: #38bdf8;">Mon, Nov 9, 2026</div>
            </div>
            <div style="text-align: right;">
              <div class="timing-tag">⏰ Optimal Entry</div>
              <div class="timing-val" style="color: #34d399;">09:30 – 10:00 AM</div>
            </div>
          </div>

          <div class="pattern-tag">
            ${{s.pattern || '🟢 Strong Bullish Trend'}}
          </div>

          <div class="trade-plan-grid">
            <div class="plan-box target">
              <div class="plan-label">
                <span>🎯 Target (+15%)</span>
                <span>Exit: Nov 13</span>
              </div>
              <div class="plan-val green">₹${{s.target}}</div>
            </div>
            <div class="plan-box stoploss">
              <div class="plan-label">
                <span>🛡️ Stop Loss (-8%)</span>
                <span>Strict</span>
              </div>
              <div class="plan-val red">₹${{s.stop_loss}}</div>
            </div>
          </div>

          <div class="hero-meta-row">
            <div>Vol Surge: <strong style="color: #38bdf8;">${{s.vol_surge}}</strong></div>
            <div>RSI: <strong>${{s.rsi}}</strong></div>
            <div>Profit QoQ: <strong style="color: #10b981;">+${{s.profit_qoq}}%</strong></div>
          </div>

          <div class="hero-actions">
            <a href="https://www.tradingview.com/chart/?symbol=NSE:${{s.symbol}}" target="_blank" class="btn btn-chart" onclick="event.stopPropagation()">
              📈 Chart
            </a>
            <a href="https://www.google.com/finance/quote/${{s.symbol}}:NSE" target="_blank" class="btn btn-buy" onclick="event.stopPropagation()">
              ⚡ Inspect & Buy
            </a>
          </div>
        </div>
      `).join('');
    }}

    function applyFilters() {{
      searchQuery = document.getElementById('searchInput').value.toLowerCase().trim();

      let filtered = STOCKS_DATA.filter(s => {{
        // Filter pills
        if (currentFilter === 'SCORE_85' && (s.score || 0) < 85) return false;
        if (currentFilter === 'SCORE_80' && (s.score || 0) < 80) return false;
        if (currentFilter === 'PRICE_50' && (s.price || 0) >= 50) return false;
        if (currentFilter === 'PRICE_100' && (s.price || 0) >= 100) return false;
        if (currentFilter === 'PATTERN_BREAKOUT' && !((s.pattern || '').includes('Breakout'))) return false;
        if (currentFilter === 'PATTERN_ENGULFING' && !((s.pattern || '').includes('Engulfing'))) return false;

        // Search query
        if (searchQuery) {{
          const matchSym = s.symbol.toLowerCase().includes(searchQuery);
          const matchName = (s.name || '').toLowerCase().includes(searchQuery);
          if (!matchSym && !matchName) return false;
        }}

        return true;
      }});

      // Sort
      filtered.sort((a, b) => {{
        let vA = a[sortColumn];
        let vB = b[sortColumn];
        if (vA === undefined) vA = 0;
        if (vB === undefined) vB = 0;

        if (typeof vA === 'string') {{
          return sortAsc ? vA.localeCompare(vB) : vB.localeCompare(vA);
        }}
        return sortAsc ? vA - vB : vB - vA;
      }});

      renderTable(filtered);
    }}

    function renderTable(stocks) {{
      const tbody = document.getElementById('stocksTableBody');
      if (stocks.length === 0) {{
        tbody.innerHTML = `<tr><td colspan="11" style="text-align: center; padding: 40px; color: var(--text-muted);">No stocks matched your criteria.</td></tr>`;
        return;
      }}

      tbody.innerHTML = stocks.map(s => {{
        const scoreClass = s.score >= 85 ? 'score-high' : (s.score >= 80 ? 'score-mid' : 'score-low');
        return `
          <tr onclick="selectStockForCalc('${{s.symbol}}')" style="cursor: pointer;">
            <td class="rank-cell">#${{s.rank}}</td>
            <td class="symbol-cell">
              ${{s.symbol}}
              <span>${{s.name ? s.name.substring(0, 24) : ''}}</span>
            </td>
            <td class="price-cell">₹${{s.price}}</td>
            <td>
              <span class="score-badge ${{scoreClass}}">⭐ ${{s.score}}</span>
            </td>
            <td>
              <span style="font-size: 11px; color: #34d399; font-weight: 600;">Mon 9:30-10:00 AM</span>
            </td>
            <td style="color: #10b981; font-weight: 700; font-family: 'JetBrains Mono', monospace;">₹${{s.target}}</td>
            <td style="color: #ef4444; font-weight: 700; font-family: 'JetBrains Mono', monospace;">₹${{s.stop_loss}}</td>
            <td style="font-family: 'JetBrains Mono', monospace;">${{s.rsi}}</td>
            <td style="color: #38bdf8; font-weight: 600;">${{s.vol_surge}}</td>
            <td style="color: #10b981; font-weight: 600;">+${{s.profit_qoq}}%</td>
            <td>
              <div style="display: flex; gap: 6px;">
                <a href="https://www.tradingview.com/chart/?symbol=NSE:${{s.symbol}}" target="_blank" class="table-btn" onclick="event.stopPropagation()">📈</a>
                <a href="https://www.google.com/finance/quote/${{s.symbol}}:NSE" target="_blank" class="table-btn" onclick="event.stopPropagation()">🔍</a>
              </div>
            </td>
          </tr>
        `;
      }}).join('');
    }}

    function setFilter(filterType, btnElement) {{
      currentFilter = filterType;
      document.querySelectorAll('.filter-pills .pill').forEach(p => p.classList.remove('active'));
      btnElement.classList.add('active');
      applyFilters();
    }}

    function sortTable(column) {{
      if (sortColumn === column) {{
        sortAsc = !sortAsc;
      }} else {{
        sortColumn = column;
        sortAsc = (column === 'rank') ? true : false;
      }}
      applyFilters();
    }}

    function selectStockForCalc(symbol) {{
      const stock = STOCKS_DATA.find(s => s.symbol === symbol);
      if (stock) {{
        selectedCalcStock = stock;
        document.getElementById('calcSelectedStock').innerText = `${{stock.symbol}} (₹${{stock.price}})`;
        updateCalculator();
        window.scrollTo({{ top: document.querySelector('.calc-card').offsetTop - 100, behavior: 'smooth' }});
      }}
    }}

    function setCalcAmount(amount) {{
      document.getElementById('investInput').value = amount;
      updateCalculator();
    }}

    function updateCalculator() {{
      const investInput = parseFloat(document.getElementById('investInput').value) || 0;
      if (!selectedCalcStock || selectedCalcStock.price <= 0) return;

      const shares = Math.floor(investInput / selectedCalcStock.price);
      const actualInvest = shares * selectedCalcStock.price;
      const targetVal = shares * selectedCalcStock.target;
      const stopVal = shares * selectedCalcStock.stop_loss;

      const profit = Math.round(targetVal - actualInvest);
      const loss = Math.round(actualInvest - stopVal);

      document.getElementById('calcShares').innerText = shares.toLocaleString('en-IN');
      document.getElementById('calcProfit').innerText = `+₹${{profit.toLocaleString('en-IN')}}`;
      document.getElementById('calcLoss').innerText = `-₹${{loss.toLocaleString('en-IN')}}`;
    }}

    document.getElementById('investInput').addEventListener('input', updateCalculator);

    window.onload = init;
  </script>
</body>
</html>
"""

with open(OUTPUT_HTML, "w") as f:
    f.write(html_content)

print(f"Successfully generated {OUTPUT_HTML} (size: {os.path.getsize(OUTPUT_HTML)} bytes)")
