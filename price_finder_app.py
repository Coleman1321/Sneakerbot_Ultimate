"""
Sneaker Price Finder – Flask web app
=====================================
Run:
    python price_finder_app.py

Then open http://localhost:5001 in your browser.
"""

import logging
from flask import Flask, jsonify, request, render_template_string
from src.price_finder import find_prices

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
app = Flask(__name__)

# ---------------------------------------------------------------------------
# HTML template (self-contained – no external CDN required for core layout)
# ---------------------------------------------------------------------------

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Sneaker Price Finder</title>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    :root {
      --bg:       #0f0f12;
      --surface:  #1a1a22;
      --card:     #22222e;
      --accent:   #6c63ff;
      --accent2:  #ff6584;
      --text:     #e8e8f0;
      --muted:    #888899;
      --border:   #2e2e3e;
      --green:    #22c55e;
      --radius:   12px;
    }

    body {
      background: var(--bg);
      color: var(--text);
      font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 2rem 1rem 4rem;
    }

    /* ── Header ── */
    header {
      text-align: center;
      margin-bottom: 2.5rem;
    }
    header .logo {
      font-size: 2.8rem;
      margin-bottom: .4rem;
    }
    header h1 {
      font-size: 1.9rem;
      font-weight: 700;
      background: linear-gradient(135deg, var(--accent), var(--accent2));
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }
    header p {
      color: var(--muted);
      margin-top: .4rem;
      font-size: .95rem;
    }

    /* ── Search form ── */
    .search-card {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 1.8rem 2rem;
      width: 100%;
      max-width: 720px;
      display: flex;
      gap: 1rem;
      flex-wrap: wrap;
      align-items: flex-end;
    }

    .field {
      display: flex;
      flex-direction: column;
      gap: .4rem;
      flex: 1;
      min-width: 160px;
    }
    .field label {
      font-size: .8rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: .06em;
      color: var(--muted);
    }
    .field input, .field select {
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 8px;
      color: var(--text);
      font-size: 1rem;
      padding: .65rem .9rem;
      outline: none;
      transition: border-color .2s;
      width: 100%;
    }
    .field input::placeholder { color: var(--muted); }
    .field input:focus, .field select:focus {
      border-color: var(--accent);
    }
    .field select option { background: var(--card); }

    .btn-search {
      background: linear-gradient(135deg, var(--accent), var(--accent2));
      border: none;
      border-radius: 8px;
      color: #fff;
      cursor: pointer;
      font-size: 1rem;
      font-weight: 600;
      padding: .68rem 1.8rem;
      transition: opacity .2s, transform .1s;
      white-space: nowrap;
      flex-shrink: 0;
    }
    .btn-search:hover  { opacity: .88; }
    .btn-search:active { transform: scale(.97); }
    .btn-search:disabled { opacity: .5; cursor: not-allowed; }

    /* ── Status / spinner ── */
    #status {
      width: 100%;
      max-width: 720px;
      margin-top: 1.2rem;
      text-align: center;
      color: var(--muted);
      font-size: .9rem;
      min-height: 1.4rem;
    }

    .spinner {
      display: inline-block;
      width: 18px; height: 18px;
      border: 3px solid var(--border);
      border-top-color: var(--accent);
      border-radius: 50%;
      animation: spin .7s linear infinite;
      vertical-align: middle;
      margin-right: .4rem;
    }
    @keyframes spin { to { transform: rotate(360deg); } }

    /* ── Summary bar ── */
    #summary {
      width: 100%;
      max-width: 960px;
      margin-top: 1.8rem;
      display: none;
    }
    .summary-bar {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 1rem 1.4rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: .6rem;
    }
    .summary-stat { display: flex; flex-direction: column; align-items: center; gap: .1rem; }
    .summary-stat .val {
      font-size: 1.5rem; font-weight: 700;
      background: linear-gradient(135deg, var(--accent), var(--accent2));
      -webkit-background-clip: text; -webkit-text-fill-color: transparent;
      background-clip: text;
    }
    .summary-stat .lbl { font-size: .75rem; color: var(--muted); text-transform: uppercase; letter-spacing: .05em; }

    /* ── Platform badges ── */
    .badge {
      display: inline-block;
      border-radius: 999px;
      font-size: .7rem;
      font-weight: 700;
      padding: .2rem .65rem;
      text-transform: uppercase;
      letter-spacing: .05em;
    }
    .badge-StockX  { background: #0c7f3f22; color: #22c55e; border: 1px solid #22c55e44; }
    .badge-GOAT    { background: #3b82f622; color: #60a5fa; border: 1px solid #3b82f644; }
    .badge-eBay    { background: #f59e0b22; color: #fbbf24; border: 1px solid #f59e0b44; }
    .badge-Grailed { background: #ec489922; color: #f472b6; border: 1px solid #ec489944; }

    /* ── Results grid ── */
    #results {
      width: 100%;
      max-width: 960px;
      margin-top: 1.4rem;
      display: none;
      flex-direction: column;
      gap: .8rem;
    }

    .result-row {
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      display: flex;
      align-items: center;
      gap: 1rem;
      padding: 1rem 1.2rem;
      transition: border-color .2s, transform .15s;
      position: relative;
    }
    .result-row:hover {
      border-color: var(--accent);
      transform: translateY(-1px);
    }
    .result-row.lowest {
      border-color: var(--green);
      box-shadow: 0 0 0 1px var(--green);
    }
    .lowest-tag {
      position: absolute;
      top: -10px; left: 12px;
      background: var(--green);
      color: #000;
      font-size: .65rem;
      font-weight: 800;
      padding: .15rem .55rem;
      border-radius: 999px;
      text-transform: uppercase;
      letter-spacing: .07em;
    }

    .result-img {
      width: 64px; height: 64px;
      object-fit: contain;
      border-radius: 8px;
      background: var(--surface);
      flex-shrink: 0;
    }
    .result-img-placeholder {
      width: 64px; height: 64px;
      background: var(--surface);
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1.6rem;
      flex-shrink: 0;
    }

    .result-info { flex: 1; min-width: 0; }
    .result-name {
      font-weight: 600;
      font-size: .95rem;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .result-meta {
      display: flex;
      gap: .5rem;
      align-items: center;
      margin-top: .35rem;
      flex-wrap: wrap;
    }
    .result-condition { font-size: .8rem; color: var(--muted); }
    .result-size {
      font-size: .8rem;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 4px;
      padding: .1rem .45rem;
    }

    .result-price {
      font-size: 1.5rem;
      font-weight: 800;
      color: var(--text);
      flex-shrink: 0;
      margin: 0 .5rem;
    }

    .btn-buy {
      background: linear-gradient(135deg, var(--accent), var(--accent2));
      border: none;
      border-radius: 8px;
      color: #fff;
      cursor: pointer;
      font-size: .9rem;
      font-weight: 700;
      padding: .6rem 1.4rem;
      text-decoration: none;
      transition: opacity .2s, transform .1s;
      white-space: nowrap;
      flex-shrink: 0;
    }
    .btn-buy:hover  { opacity: .85; }
    .btn-buy:active { transform: scale(.96); }

    /* ── Empty / error states ── */
    .empty-state {
      text-align: center;
      padding: 3rem 1rem;
      color: var(--muted);
    }
    .empty-state .icon { font-size: 3rem; margin-bottom: .8rem; }
    .empty-state p { font-size: .95rem; }

    /* ── Responsive ── */
    @media (max-width: 540px) {
      .result-price { font-size: 1.1rem; }
      .result-img, .result-img-placeholder { width: 48px; height: 48px; }
      .btn-buy { padding: .5rem .9rem; font-size: .8rem; }
    }
  </style>
</head>
<body>

  <header>
    <div class="logo">👟</div>
    <h1>Sneaker Price Finder</h1>
    <p>Enter a SKU or name to see the lowest prices across StockX, GOAT, eBay &amp; Grailed</p>
  </header>

  <div class="search-card">
    <div class="field" style="flex:2; min-width:200px;">
      <label for="sku">SKU / Sneaker Name</label>
      <input id="sku" type="text" placeholder="e.g. DZ5485-612 or Air Jordan 1 Chicago" />
    </div>
    <div class="field" style="max-width:130px;">
      <label for="size">US Size</label>
      <select id="size">
        <option value="">Any Size</option>
        <option value="4">4</option>
        <option value="4.5">4.5</option>
        <option value="5">5</option>
        <option value="5.5">5.5</option>
        <option value="6">6</option>
        <option value="6.5">6.5</option>
        <option value="7">7</option>
        <option value="7.5">7.5</option>
        <option value="8">8</option>
        <option value="8.5">8.5</option>
        <option value="9">9</option>
        <option value="9.5">9.5</option>
        <option value="10">10</option>
        <option value="10.5">10.5</option>
        <option value="11">11</option>
        <option value="11.5">11.5</option>
        <option value="12">12</option>
        <option value="12.5">12.5</option>
        <option value="13">13</option>
        <option value="14">14</option>
        <option value="15">15</option>
      </select>
    </div>
    <button class="btn-search" id="searchBtn" onclick="runSearch()">Search</button>
  </div>

  <div id="status"></div>

  <div id="summary">
    <div class="summary-bar">
      <div class="summary-stat">
        <span class="val" id="sumCount">—</span>
        <span class="lbl">Listings found</span>
      </div>
      <div class="summary-stat">
        <span class="val" id="sumLowest">—</span>
        <span class="lbl">Lowest price</span>
      </div>
      <div class="summary-stat">
        <span class="val" id="sumHighest">—</span>
        <span class="lbl">Highest price</span>
      </div>
      <div class="summary-stat">
        <span class="val" id="sumPlatforms">—</span>
        <span class="lbl">Platforms</span>
      </div>
    </div>
  </div>

  <div id="results"></div>

  <script>
    const skuInput   = document.getElementById('sku');
    const sizeSelect = document.getElementById('size');
    const searchBtn  = document.getElementById('searchBtn');
    const statusEl   = document.getElementById('status');
    const summaryEl  = document.getElementById('summary');
    const resultsEl  = document.getElementById('results');

    skuInput.addEventListener('keydown', e => { if (e.key === 'Enter') runSearch(); });

    function setStatus(html) { statusEl.innerHTML = html; }

    function fmt(price) {
      return '$' + price.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    }

    function platformIcon(name) {
      const icons = { StockX: '📈', GOAT: '🐐', eBay: '🛒', Grailed: '👕' };
      return icons[name] || '🏪';
    }

    async function runSearch() {
      const sku  = skuInput.value.trim();
      const size = sizeSelect.value;

      if (!sku) {
        setStatus('<span style="color:#ff6584">⚠ Please enter a SKU or sneaker name.</span>');
        return;
      }

      searchBtn.disabled = true;
      summaryEl.style.display = 'none';
      resultsEl.style.display  = 'none';
      resultsEl.innerHTML = '';
      setStatus('<span class="spinner"></span>Searching StockX, GOAT, eBay &amp; Grailed…');

      try {
        const params = new URLSearchParams({ sku, size });
        const resp   = await fetch('/api/search?' + params);
        const data   = await resp.json();

        if (!resp.ok) {
          setStatus('<span style="color:#ff6584">Error: ' + (data.error || 'Search failed') + '</span>');
          return;
        }

        const results = data.results || [];

        if (results.length === 0) {
          setStatus('');
          resultsEl.style.display = 'flex';
          resultsEl.innerHTML = `
            <div class="empty-state">
              <div class="icon">🔍</div>
              <p>No listings found for <strong>${escHtml(sku)}</strong>${size ? ' in size <strong>' + size + '</strong>' : ''}.<br>
              Try a different SKU or remove the size filter.</p>
            </div>`;
          return;
        }

        // Summary bar
        const prices    = results.map(r => r.price);
        const platforms = [...new Set(results.map(r => r.platform))];
        document.getElementById('sumCount').textContent     = results.length;
        document.getElementById('sumLowest').textContent    = fmt(Math.min(...prices));
        document.getElementById('sumHighest').textContent   = fmt(Math.max(...prices));
        document.getElementById('sumPlatforms').textContent = platforms.length;
        summaryEl.style.display = 'block';

        // Result rows
        const rows = results.map((r, idx) => {
          const isLowest = idx === 0;
          const imgHtml  = r.img
            ? `<img class="result-img" src="${escHtml(r.img)}" alt="" loading="lazy"
                    onerror="this.style.display='none';this.nextElementSibling.style.display='flex'">`
            : '';
          const placeholderHtml = `<div class="result-img-placeholder" ${r.img ? 'style="display:none"' : ''}>${platformIcon(r.platform)}</div>`;

          return `
            <div class="result-row ${isLowest ? 'lowest' : ''}">
              ${isLowest ? '<span class="lowest-tag">Lowest Price</span>' : ''}
              ${imgHtml}${placeholderHtml}
              <div class="result-info">
                <div class="result-name" title="${escHtml(r.name)}">${escHtml(r.name)}</div>
                <div class="result-meta">
                  <span class="badge badge-${escHtml(r.platform)}">${platformIcon(r.platform)} ${escHtml(r.platform)}</span>
                  <span class="result-condition">${escHtml(r.condition)}</span>
                  ${r.size && r.size !== 'Any' ? `<span class="result-size">US ${escHtml(r.size)}</span>` : ''}
                </div>
              </div>
              <div class="result-price">${fmt(r.price)}</div>
              <a class="btn-buy" href="${escHtml(r.url)}" target="_blank" rel="noopener noreferrer">
                Buy →
              </a>
            </div>`;
        }).join('');

        setStatus(`Found <strong>${results.length}</strong> listing${results.length !== 1 ? 's' : ''} for <strong>${escHtml(sku)}</strong>${size ? ' · Size ' + size : ''}`);
        resultsEl.innerHTML      = rows;
        resultsEl.style.display  = 'flex';

      } catch (err) {
        setStatus('<span style="color:#ff6584">Network error — is the server running?</span>');
        console.error(err);
      } finally {
        searchBtn.disabled = false;
      }
    }

    function escHtml(str) {
      return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;');
    }
  </script>
</body>
</html>
"""


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------


@app.route("/")
def index():
    return render_template_string(HTML)


@app.route("/api/search")
def search():
    sku = request.args.get("sku", "").strip()
    size = request.args.get("size", "").strip()

    if not sku:
        return jsonify({"error": "SKU is required"}), 400

    results = find_prices(sku, size)
    return jsonify({"results": results, "sku": sku, "size": size})


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


if __name__ == "__main__":
    print("\n🔍  Sneaker Price Finder")
    print("   Open http://localhost:5001 in your browser\n")
    app.run(host="0.0.0.0", port=5001, debug=False)
