/**
 * WTM BasisWatch + Implied Rate
 * Embedded panel (Transmission Control) · Standalone page (Whinfell_BasisWatch.html)
 */
(function basisWatchPanel(global) {
  'use strict';

  const BW_BUILD = '2.5-BASISWATCH-STANDALONE-2026-07-01';
  const THEME_COLORS = { dark: '#090d12', light: '#eef1f5' };
  const PREFS_KEY = 'whinfell_basiswatch_prefs';
  const THEME_KEY = 'whinfell_tc_theme';
  const HYDRATION_URL = 'data/hydration/latest.json';
  const CURVE_URL = 'data/barchart/barchart_curve_history.json';

  const CME_MONTH = { F: 0, G: 1, H: 2, J: 3, K: 4, M: 5, N: 6, Q: 7, U: 8, V: 9, X: 10, Z: 11 };
  const MONTH_LABEL = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

  const ASSETS = {
    BTC: { root: 'BT', spotKey: 'btc_spot_usd', label: 'Bitcoin', barchartSpread: 'https://www.barchart.com/futures/quotes/BTM26/spreads', koyfin: 'https://app.koyfin.com/crypto/BTCUSD' },
    ETH: { root: 'ETH', spotKey: 'eth_spot_usd', label: 'Ethereum', barchartSpread: 'https://www.barchart.com/futures/quotes/ETHM26/spreads', koyfin: 'https://app.koyfin.com/crypto/ETHUSD' },
  };

  const CROSS_ASSET_ROOTS = [
    { root: 'DX', label: 'US Dollar (DX)', role: 'FX bridge' },
    { root: 'HG', label: 'Copper (HG)', role: 'Industrial' },
    { root: 'ZM', label: 'Soybean Meal (ZM)', role: 'Ag complex' },
    { root: 'TA', label: 'Iron Ore (TA)', role: 'China industrial' },
  ];

  let curveCache = null;
  let curveFetchPromise = null;
  let standaloneState = null;
  const isStandalone = () => document.body?.dataset?.bwLayout === 'standalone';

  function el(id) { return document.getElementById(id); }

  function fmtNum(n, d = 2) {
    if (n == null || !Number.isFinite(n)) return '—';
    return n.toLocaleString('en-US', { minimumFractionDigits: d, maximumFractionDigits: d });
  }

  function fmtPct(n, d = 2) {
    if (n == null || !Number.isFinite(n)) return '—';
    return `${fmtNum(n, d)}%`;
  }

  function parseCmeSymbol(sym) {
    const m = String(sym || '').match(/^([A-Z0-9!]+)([FGHJKMNQUVXZ])(\d{2})$/);
    if (!m) return null;
    const month = CME_MONTH[m[2]];
    if (month == null) return null;
    const year = 2000 + parseInt(m[3], 10);
    return { root: m[1], monthCode: m[2], month, year, expiry: lastFridayOfMonth(year, month), label: `${MONTH_LABEL[month]} ${year}` };
  }

  function lastFridayOfMonth(year, month) {
    const d = new Date(Date.UTC(year, month + 1, 0));
    while (d.getUTCDay() !== 5) d.setUTCDate(d.getUTCDate() - 1);
    return d;
  }

  function daysBetween(a, b) { return Math.max(1, Math.round((b - a) / 86400000)); }
  function daysToExpiry(expiry, asOf = new Date()) { return daysBetween(asOf, expiry); }

  function heatClass(ann) {
    if (!Number.isFinite(ann)) return 'bw-heat--na';
    if (ann >= 12) return 'bw-heat--hot';
    if (ann >= 6) return 'bw-heat--warm';
    if (ann >= 0) return 'bw-heat--flat';
    return 'bw-heat--cold';
  }

  function shapeBadgeClass(shape) {
    if (shape === 'Contango') return 'bw-shape-badge--contango';
    if (shape === 'Backwardation') return 'bw-shape-badge--backwardation';
    return 'bw-shape-badge--flat';
  }

  function curveShapeLabel(contracts) {
    if (!contracts.length) return '—';
    const front = contracts.slice(0, Math.min(3, contracts.length));
    const avg = front.reduce((s, c) => s + (c.annBasis || 0), 0) / front.length;
    if (avg >= 4) return 'Contango';
    if (avg <= -2) return 'Backwardation';
    return 'Flat';
  }

  function getChartTheme() {
    const s = getComputedStyle(document.documentElement);
    const v = name => s.getPropertyValue(name).trim() || undefined;
    return {
      grid: v('--bw-chart-grid') || 'rgba(255,255,255,0.07)',
      axis: v('--bw-chart-axis') || '#8b9aab',
      spotLine: v('--bw-chart-spot-line') || 'rgba(94,179,255,0.55)',
      spotLabel: v('--bw-chart-spot-label') || '#9ec5f0',
      curve: v('--bw-chart-curve') || '#e07b39',
      front: v('--bw-chart-front') || '#3d8bfd',
      node: v('--bw-chart-node') || '#c5d0dc',
      muted: v('--bw-muted') || '#8b9aab',
      empty: v('--bw-muted') || '#8b9aab',
    };
  }

  function loadPrefs() {
    try {
      const raw = localStorage.getItem(PREFS_KEY);
      return raw ? JSON.parse(raw) : {};
    } catch { return {}; }
  }

  function savePrefs(prefs) {
    try { localStorage.setItem(PREFS_KEY, JSON.stringify(prefs)); } catch { /* ignore */ }
  }

  function applyTheme(theme) {
    const next = theme === 'light' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    const btn = el('btnBwTheme');
    if (btn) {
      const label = btn.querySelector('.bw-theme-label');
      if (label) label.textContent = next === 'dark' ? 'Light mode' : 'Dark mode';
      else btn.textContent = next === 'dark' ? 'Light mode' : 'Dark mode';
      btn.setAttribute('aria-pressed', next === 'light' ? 'true' : 'false');
      btn.title = next === 'dark' ? 'Switch to light mode' : 'Switch to dark mode';
    }
    const themeColor = el('bwThemeColor');
    if (themeColor) themeColor.setAttribute('content', THEME_COLORS[next] || THEME_COLORS.dark);
    try { localStorage.setItem(THEME_KEY, next); } catch { /* ignore */ }
  }

  function initTheme() {
    const params = new URLSearchParams(location.search);
    let theme = params.get('theme');
    if (!theme) {
      try { theme = localStorage.getItem(THEME_KEY) || 'dark'; } catch { theme = 'dark'; }
    }
    applyTheme(theme);
  }

  function popOutUrl(state) {
    const bw = state?.basisWatch || loadPrefs();
    const theme = document.documentElement.getAttribute('data-theme') || 'dark';
    const base = isStandalone()
      ? location.href.split('?')[0]
      : (location.protocol === 'file:'
        ? new URL('Whinfell_BasisWatch.html', location.href).href
        : new URL('Whinfell_BasisWatch.html', location.origin + location.pathname.replace(/\/[^/]*$/, '/')).href);
    const q = new URLSearchParams({
      asset: bw.asset || 'BTC',
      view: bw.view || 'basis',
      theme,
    });
    return `${base}?${q.toString()}`;
  }

  async function ensureCurveHistory() {
    if (curveCache) return curveCache;
    if (curveFetchPromise) return curveFetchPromise;
    if (location.protocol === 'file:') {
      curveCache = { records: [] };
      return curveCache;
    }
    curveFetchPromise = fetch(`${CURVE_URL}?_=${Date.now()}`)
      .then(r => (r.ok ? r.json() : { records: [] }))
      .then(data => { curveCache = data || { records: [] }; return curveCache; })
      .catch(() => { curveCache = { records: [] }; return curveCache; });
    return curveFetchPromise;
  }

  async function loadHydrationBundle() {
    if (location.protocol === 'file:') return null;
    try {
      const res = await fetch(`${HYDRATION_URL}?_=${Date.now()}`);
      if (!res.ok) return null;
      return await res.json();
    } catch { return null; }
  }

  function recordsForRoot(records, root) {
    return (records || []).filter(r => {
      const meta = r.contract_meta || {};
      return meta.contract_root === root || String(r.raw_symbol || '').startsWith(root);
    });
  }

  function buildContracts(records, spot, asOfDate) {
    const asOf = asOfDate ? new Date(asOfDate) : new Date();
    return records.map(r => {
      const parsed = parseCmeSymbol(r.raw_symbol);
      if (!parsed) return null;
      const price = Number(r.latest?.close ?? r.points?.[r.points.length - 1]?.close);
      if (!Number.isFinite(price) || price <= 0) return null;
      const dte = daysToExpiry(parsed.expiry, asOf);
      if (dte < 0) return null;
      const absBasis = price - spot;
      const pctBasis = spot > 0 ? (absBasis / spot) * 100 : null;
      const annBasis = spot > 0 && dte > 0 ? ((price / spot) - 1) * (365 / dte) * 100 : null;
      return {
        symbol: r.raw_symbol, label: parsed.label, expiry: parsed.expiry, dte, price,
        absBasis, pctBasis, annBasis,
        chg: Number(r.latest?.change), pctChg: Number(r.latest?.pct_change),
      };
    }).filter(Boolean).sort((a, b) => a.expiry - b.expiry);
  }

  function synthesizeEthCurve(btcContracts, ethSpot, btcSpot) {
    if (!btcContracts.length || !ethSpot || !btcSpot) return [];
    const ratio = ethSpot / btcSpot;
    return btcContracts.map(c => ({
      ...c, symbol: c.symbol.replace(/^BT/, 'ETH'), price: c.price * ratio,
      absBasis: c.price * ratio - ethSpot, pctBasis: ((c.price * ratio - ethSpot) / ethSpot) * 100, annBasis: c.annBasis, synthetic: true,
    }));
  }

  function pickFrontContract(contracts, rollLogic, manualNear) {
    if (!contracts.length) return null;
    if (rollLogic === 'manual' && manualNear) {
      const hit = contracts.find(c => c.symbol.toUpperCase().includes(String(manualNear).toUpperCase().slice(0, 3)));
      if (hit) return hit;
    }
    if (rollLogic === 'constant') {
      let best = contracts[0], bestDist = Math.abs(best.dte - 30);
      contracts.forEach(c => {
        const d = Math.abs(c.dte - 30);
        if (d < bestDist) { best = c; bestDist = d; }
      });
      return best;
    }
    return contracts.find(c => c.dte >= 7) || contracts[0];
  }

  function forwardRates(contracts) {
    const out = [];
    for (let i = 1; i < contracts.length; i++) {
      const a = contracts[i - 1], b = contracts[i];
      const days = daysBetween(a.expiry, b.expiry);
      out.push({ from: a.symbol, to: b.symbol, days, fwd: a.price > 0 ? ((b.price / a.price) - 1) * (365 / days) * 100 : null, calendar: b.price - a.price });
    }
    return out;
  }

  function richestTenor(contracts) {
    return contracts.length ? contracts.reduce((b, c) => (!b || (c.annBasis || -999) > (b.annBasis || -999) ? c : b), null) : null;
  }

  function steepestCalendar(forwards) {
    return forwards.length ? forwards.reduce((b, f) => (!b || Math.abs(f.fwd || 0) > Math.abs(b.fwd || 0) ? f : b), null) : null;
  }

  function crossAssetStrip(records) {
    return CROSS_ASSET_ROOTS.map(spec => {
      const recs = recordsForRoot(records, spec.root);
      const latest = recs.map(r => r.latest).filter(Boolean).sort((a, b) => String(b.date).localeCompare(String(a.date)))[0];
      return { ...spec, symbol: recs[0]?.raw_symbol || spec.root, price: latest?.close, change: latest?.pct_change };
    });
  }

  function rollStateLabel(contracts, front) {
    if (!front || contracts.length < 2) return '—';
    const idx = contracts.findIndex(c => c.symbol === front.symbol);
    const next = contracts[idx + 1];
    if (!next) return 'Back of curve';
    if (front.dte <= 14) return `Roll window · ${front.symbol} → ${next.symbol}`;
    return `Hold ${front.symbol}`;
  }

  function buildModel(state, curveData) {
    const prefs = { ...loadPrefs(), ...(state.basisWatch || {}) };
    const assetKey = prefs.asset || 'BTC';
    const asset = ASSETS[assetKey] || ASSETS.BTC;
    const records = curveData?.records || [];
    const sleeve = state.hydration?.crypto_sleeve?.assets || {};
    const spotRec = sleeve[asset.spotKey];
    const spot = Number(spotRec?.last_price);
    const spotChg = Number(spotRec?.chg_1d ?? spotRec?.['1_day']) * 100;
    const asOf = state.hydration?.as_of || state.provenance?.dataAsOf || new Date().toISOString();

    let contracts = buildContracts(recordsForRoot(records, asset.root), spot, asOf);
    let dataNote = '';
    if (!contracts.length && assetKey === 'ETH' && spot > 0) {
      const btcSpot = Number(sleeve.btc_spot_usd?.last_price);
      contracts = synthesizeEthCurve(buildContracts(recordsForRoot(records, 'BT'), btcSpot, asOf), spot, btcSpot);
      dataNote = 'ETH curve synthesized from BTC term structure · wire CME ETH futures for live curve';
    } else if (!contracts.length) {
      dataNote = isStandalone() ? 'Loading hydration bundle…' : 'Import hydration + publish desk preview for Barchart curve JSON';
    }

    const rollLogic = prefs.rollLogic || 'nearest';
    const front = pickFrontContract(contracts, rollLogic, state.btcL3?.nearMonth || '');
    const forwards = forwardRates(contracts);
    const richest = richestTenor(contracts);
    const steepest = steepestCalendar(forwards);
    const shape = curveShapeLabel(contracts);

    return {
      assetKey, asset, spot, spotChg: Number.isFinite(spotChg) ? spotChg : null, asOf,
      contracts, front, forwards, cross: crossAssetStrip(records), richest, steepest, shape,
      rollLabel: rollStateLabel(contracts, front), dataNote,
      refMid: Number(state.hydration?.global?.basis_spread || state.hydration?.execution?.basis_spread || state.hydration?.execution?.ref_mid) || null,
      mode: prefs.mode || 'live', view: prefs.view || 'basis',
    };
  }

  function renderSummaryCards(model, standalone) {
    const front = model.front, spot = model.spot;
    const hi = standalone ? ' bw-card--highlight' : '';
    return `
      <div class="bw-card${hi}"><span class="bw-card-label">Spot · CF proxy</span><strong class="bw-card-value">${spot > 0 ? '$' + fmtNum(spot, 0) : '—'}</strong><span class="bw-card-meta">${Number.isFinite(model.spotChg) ? fmtPct(model.spotChg) + ' 1d' : '—'}</span></div>
      <div class="bw-card"><span class="bw-card-label">Front futures</span><strong class="bw-card-value">${front ? '$' + fmtNum(front.price, 0) : '—'}</strong><span class="bw-card-meta">${front ? front.symbol + ' · ' + front.dte + 'd' : '—'}</span></div>
      <div class="bw-card${hi}"><span class="bw-card-label">Ann. basis</span><strong class="bw-card-value">${front ? fmtPct(front.annBasis) : '—'}</strong><span class="bw-card-meta">${front ? fmtPct(front.pctBasis) + ' vs spot' : '—'}</span></div>
      <div class="bw-card"><span class="bw-card-label">Abs basis</span><strong class="bw-card-value">${front ? '$' + fmtNum(front.absBasis, 0) : '—'}</strong><span class="bw-card-meta">${model.refMid ? 'Ref mid ' + fmtPct(model.refMid) : '—'}</span></div>
      <div class="bw-card"><span class="bw-card-label">Curve shape</span><strong class="bw-card-value">${model.shape}</strong><span class="bw-card-meta">${model.rollLabel}</span></div>
      <div class="bw-card"><span class="bw-card-label">Contracts</span><strong class="bw-card-value">${model.contracts.length || '—'}</strong><span class="bw-card-meta">${String(model.asOf).slice(0, 19)}</span></div>`;
  }

  function renderCallouts(model) {
    return `<div class="bw-callout-strip">
      <div class="bw-callout"><span class="bw-callout-label">Richest tenor</span><div class="bw-callout-value">${model.richest?.symbol || '—'}</div><div class="bw-callout-meta">${model.richest ? fmtPct(model.richest.annBasis) + ' ann.' : '—'}</div></div>
      <div class="bw-callout"><span class="bw-callout-label">Steepest calendar</span><div class="bw-callout-value">${model.steepest ? model.steepest.from + '→' + model.steepest.to : '—'}</div><div class="bw-callout-meta">${model.steepest ? fmtPct(model.steepest.fwd) + ' fwd' : '—'}</div></div>
    </div>`;
  }

  function renderBasisTable(model) {
    if (!model.contracts.length) return '<p class="bw-empty">No futures curve — run daily chain and publish desk preview.</p>';
    const rows = model.contracts.map(c => `
      <tr class="${model.front && c.symbol === model.front.symbol ? 'bw-row-front' : ''}">
        <td>${c.symbol}${c.synthetic ? ' <span title="Synthesized">*</span>' : ''}</td>
        <td>${c.label}</td><td>${c.dte}d</td>
        <td>$${fmtNum(c.price, 0)}</td><td>${fmtNum(c.absBasis, 0)}</td>
        <td>${fmtPct(c.pctBasis)}</td>
        <td class="${heatClass(c.annBasis)}">${fmtPct(c.annBasis)}</td>
        <td>${Number.isFinite(c.pctChg) ? fmtPct(c.pctChg) : '—'}</td>
      </tr>`).join('');
    return `<div class="bw-table-wrap"><table class="bw-table"><thead><tr><th>Contract</th><th>Expiry</th><th>DTE</th><th>Futures</th><th>Abs</th><th>%</th><th>Ann.</th><th>Chg</th></tr></thead><tbody>${rows}</tbody></table></div>`;
  }

  function renderImpliedTable(model) {
    if (!model.contracts.length) return '<p class="bw-empty">No curve data.</p>';
    const spotRows = model.contracts.map(c => `<tr><td>${c.symbol}</td><td>${fmtPct(c.annBasis)}</td><td>${c.dte}d</td></tr>`).join('');
    const fwdRows = model.forwards.map(f => `<tr><td>${f.from} → ${f.to}</td><td>${fmtPct(f.fwd)}</td><td>${fmtNum(f.calendar, 0)}</td><td>${f.days}d</td></tr>`).join('');
    return `<div class="bw-implied-grid">
      <div class="bw-panel" style="border:none;box-shadow:none"><h4 class="bw-subhead">Spot-implied annualized</h4><div class="bw-table-wrap"><table class="bw-table bw-table--compact"><thead><tr><th>Tenor</th><th>Rate</th><th>DTE</th></tr></thead><tbody>${spotRows}</tbody></table></div></div>
      <div class="bw-panel" style="border:none;box-shadow:none"><h4 class="bw-subhead">Forward calendar rates</h4><div class="bw-table-wrap"><table class="bw-table bw-table--compact"><thead><tr><th>Leg</th><th>Fwd</th><th>Spread $</th><th>Days</th></tr></thead><tbody>${fwdRows || '<tr><td colspan="4">—</td></tr>'}</tbody></table></div></div>
    </div>`;
  }

  function renderHeatmap(model) {
    if (!model.contracts.length) return '';
    return `<div class="bw-heatmap">${model.contracts.map(c => `
      <div class="bw-heat-cell ${heatClass(c.annBasis)}" title="${c.symbol}: ${fmtPct(c.annBasis)} ann.">
        <span class="bw-heat-sym">${c.symbol.replace(/\d{2}$/, '')}</span>
        <span class="bw-heat-val">${fmtPct(c.annBasis, 1)}</span>
        <span class="bw-heat-dte">${c.dte}d</span>
      </div>`).join('')}</div>`;
  }

  function renderCrossAsset(model) {
    return model.cross.map(x => `
      <div class="bw-cross-pill">
        <span class="bw-cross-label">${x.label}</span>
        <span class="bw-cross-role">${x.role}</span>
        <span class="bw-cross-val">${Number.isFinite(x.price) ? fmtNum(x.price, x.price < 10 ? 4 : 2) : '—'}<span class="bw-cross-chg">${Number.isFinite(x.change) ? fmtPct(x.change) : ''}</span></span>
      </div>`).join('');
  }

  function drawBasisChart(model) {
    const canvas = el('bwCurveCanvas');
    if (!canvas) return;
    const theme = getChartTheme();
    const ctx = canvas.getContext('2d');
    const dpr = window.devicePixelRatio || 1;
    const rect = canvas.getBoundingClientRect();
    const h = isStandalone() ? 280 : Math.max(110, rect.height);
    canvas.width = Math.max(280, rect.width) * dpr;
    canvas.height = h * dpr;
    ctx.scale(dpr, dpr);
    const w = rect.width;
    ctx.clearRect(0, 0, w, h);
    const contracts = model.contracts;
    if (!contracts.length || !(model.spot > 0)) {
      ctx.fillStyle = theme.empty;
      ctx.font = '12px system-ui,sans-serif';
      ctx.fillText('Curve populates after hydration + Barchart curve JSON', 16, h / 2);
      return;
    }
    const prices = [model.spot, ...contracts.map(c => c.price)];
    const minP = Math.min(...prices) * 0.998, maxP = Math.max(...prices) * 1.002;
    const pad = { l: 52, r: 16, t: 18, b: 32 };
    const plotW = w - pad.l - pad.r, plotH = h - pad.t - pad.b;
    const xAt = i => pad.l + (i / Math.max(1, contracts.length)) * plotW;
    const yAt = p => pad.t + plotH - ((p - minP) / (maxP - minP || 1)) * plotH;

    ctx.strokeStyle = theme.grid;
    for (let i = 0; i <= 4; i++) {
      const y = pad.t + (plotH * i) / 4;
      ctx.beginPath(); ctx.moveTo(pad.l, y); ctx.lineTo(w - pad.r, y); ctx.stroke();
    }
    ctx.beginPath(); ctx.moveTo(pad.l, pad.t); ctx.lineTo(pad.l, h - pad.b); ctx.lineTo(w - pad.r, h - pad.b); ctx.stroke();

    ctx.setLineDash([5, 4]);
    ctx.strokeStyle = theme.spotLine;
    ctx.beginPath(); ctx.moveTo(pad.l, yAt(model.spot)); ctx.lineTo(w - pad.r, yAt(model.spot)); ctx.stroke();
    ctx.setLineDash([]);
    ctx.fillStyle = theme.spotLabel;
    ctx.font = '10px system-ui,sans-serif';
    ctx.fillText(`Spot $${fmtNum(model.spot, 0)}`, pad.l + 6, yAt(model.spot) - 6);

    const grad = ctx.createLinearGradient(pad.l, 0, w - pad.r, 0);
    grad.addColorStop(0, theme.curve);
    grad.addColorStop(1, theme.front);
    ctx.strokeStyle = grad;
    ctx.lineWidth = 2.5;
    ctx.beginPath();
    contracts.forEach((c, i) => { const x = xAt(i + 1), y = yAt(c.price); if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y); });
    ctx.stroke();
    ctx.lineWidth = 1;

    contracts.forEach((c, i) => {
      const x = xAt(i + 1), y = yAt(c.price);
      const isFront = model.front && c.symbol === model.front.symbol;
      ctx.fillStyle = isFront ? theme.front : theme.node;
      ctx.beginPath(); ctx.arc(x, y, isFront ? 5 : 3.5, 0, Math.PI * 2); ctx.fill();
      ctx.fillStyle = theme.axis;
      ctx.font = '9px system-ui';
      ctx.fillText(c.symbol.replace(/\d{2}$/, ''), x - 10, h - 10);
    });
  }

  function syncControls(model) {
    document.querySelectorAll('.bw-view-tab').forEach(btn => btn.classList.toggle('bw-view-tab--active', btn.dataset.bwView === model.view));
    document.querySelectorAll('.bw-asset-btn').forEach(btn => btn.classList.toggle('bw-asset-btn--active', btn.dataset.bwAsset === model.assetKey));
    const roll = el('bwRollLogic'); if (roll) roll.value = (standaloneState || {}).basisWatch?.rollLogic || loadPrefs().rollLogic || 'nearest';
    const mode = el('bwModeToggle'); if (mode) mode.value = model.mode;
  }

  function renderPanel(state) {
    const panel = el('basisWatchPanel');
    if (!panel && !isStandalone()) return;
    if (panel) {
      panel.classList.toggle('basis-watch-panel--collapsed', !!state.basisWatch?.collapsed);
    }
    const model = state._basisWatchModel || buildModel(state, curveCache || { records: [] });
    const standalone = isStandalone();

    const status = el('bwStatusChip');
    if (status) { status.textContent = model.mode === 'snapshot' ? 'Snapshot' : 'Live'; status.className = `bw-status-chip bw-status-chip--${model.mode}`; }

    const note = el('bwDataNote');
    if (note) note.textContent = model.dataNote || (model.contracts.length ? `As of ${String(model.asOf).slice(0, 19)}` : '');

    const shapeBadge = el('bwShapeBadge');
    if (shapeBadge && standalone) {
      shapeBadge.className = `bw-shape-badge ${shapeBadgeClass(model.shape)}`;
      shapeBadge.textContent = `${model.shape} · ${model.rollLabel}`;
    }

    const curveMeta = el('bwCurveMeta');
    if (curveMeta) {
      const front = model.front;
      curveMeta.textContent = front
        ? `${model.asset.label} · ${front.symbol} · ${model.contracts.length} nodes`
        : `${model.asset.label} · awaiting curve`;
    }

    const summary = el('bwSummaryCards');
    if (summary) summary.innerHTML = renderSummaryCards(model, standalone);

    const callouts = el('bwCallouts');
    if (callouts) callouts.innerHTML = renderCallouts(model);

    const main = el('bwMainView');
    if (main) {
      main.innerHTML = model.view === 'implied'
        ? renderImpliedTable(model)
        : `${renderHeatmap(model)}${renderBasisTable(model)}`;
    }

    const cross = el('bwCrossAsset');
    if (cross) cross.innerHTML = renderCrossAsset(model);

    syncControls(model);
    drawBasisChart(model);
    state._basisWatchModel = model;

    const buildBadge = el('bwBuildBadge');
    if (buildBadge) buildBadge.textContent = BW_BUILD;

    const footerStamp = el('bwFooterStamp');
    if (footerStamp) footerStamp.textContent = BW_BUILD;
  }

  function persistBasisWatchPrefs(state) {
    const p = {
      asset: state.basisWatch?.asset || 'BTC',
      view: state.basisWatch?.view || 'basis',
      rollLogic: state.basisWatch?.rollLogic || 'nearest',
      mode: state.basisWatch?.mode || 'live',
    };
    savePrefs(p);
  }

  async function refresh(state, hooks) {
    await ensureCurveHistory();
    if (state.basisWatch?.mode === 'snapshot' && state.basisWatch.snapshot) {
      curveCache = state.basisWatch.snapshot.curve || curveCache;
    }
    state._basisWatchModel = buildModel(state, curveCache);
    persistBasisWatchPrefs(state);
    renderPanel(state);
    if (hooks?.renderAll) hooks.renderAll();
  }

  function exportCsv(state) {
    const model = state._basisWatchModel || buildModel(state, curveCache || { records: [] });
    const lines = ['contract,expiry,dte,futures,spot,abs_basis,pct_basis,ann_basis'];
    model.contracts.forEach(c => lines.push([c.symbol, c.label, c.dte, c.price, model.spot, c.absBasis, c.pctBasis, c.annBasis].join(',')));
    const a = document.createElement('a');
    a.href = URL.createObjectURL(new Blob([lines.join('\n')], { type: 'text/csv' }));
    a.download = `wtm_basiswatch_${model.assetKey}_${new Date().toISOString().slice(0, 10)}.csv`;
    a.click();
    URL.revokeObjectURL(a.href);
  }

  function exportPng(state) {
    const canvas = el('bwCurveCanvas');
    if (!canvas) return;
    const a = document.createElement('a');
    a.href = canvas.toDataURL('image/png');
    a.download = `wtm_basiswatch_curve_${new Date().toISOString().slice(0, 10)}.png`;
    a.click();
  }

  function captureSnapshot(state) {
    state.basisWatch = state.basisWatch || {};
    state.basisWatch.snapshot = { capturedAt: new Date().toISOString(), curve: curveCache ? JSON.parse(JSON.stringify(curveCache)) : null };
    state.basisWatch.mode = 'snapshot';
  }

  function wireControls(getState, hooks) {
    const markDirty = hooks?.markDirty || (() => {});

    el('btnBwCollapse')?.addEventListener('click', () => {
      const s = getState();
      s.basisWatch = s.basisWatch || {};
      s.basisWatch.collapsed = !s.basisWatch.collapsed;
      renderPanel(s);
      markDirty();
    });

    el('btnBwPopOut')?.addEventListener('click', () => {
      window.open(popOutUrl(getState()), '_blank', 'noopener,noreferrer');
    });

    el('btnBwTheme')?.addEventListener('click', () => {
      const cur = document.documentElement.getAttribute('data-theme') || 'dark';
      const next = cur === 'dark' ? 'light' : 'dark';
      applyTheme(next);
      renderPanel(getState());
      if (typeof global.dispatchEvent === 'function') {
        try { global.dispatchEvent(new CustomEvent('whinfell-theme-change', { detail: { theme: next } })); } catch { /* ignore */ }
      }
    });

    document.querySelectorAll('.bw-view-tab').forEach(btn => {
      btn.addEventListener('click', () => {
        const s = getState();
        s.basisWatch = s.basisWatch || {};
        s.basisWatch.view = btn.dataset.bwView || 'basis';
        refresh(s, hooks);
        markDirty();
      });
    });

    document.querySelectorAll('.bw-asset-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const s = getState();
        s.basisWatch = s.basisWatch || {};
        s.basisWatch.asset = btn.dataset.bwAsset || 'BTC';
        refresh(s, hooks);
        markDirty();
      });
    });

    el('bwRollLogic')?.addEventListener('change', e => {
      const s = getState();
      s.basisWatch = s.basisWatch || {};
      s.basisWatch.rollLogic = e.target.value;
      refresh(s, hooks);
      markDirty();
    });

    el('bwModeToggle')?.addEventListener('change', e => {
      const s = getState();
      s.basisWatch = s.basisWatch || {};
      if (e.target.value === 'snapshot') captureSnapshot(s);
      else s.basisWatch.mode = 'live';
      renderPanel(s);
      persistBasisWatchPrefs(s);
      markDirty();
    });

    el('btnBwRefresh')?.addEventListener('click', async () => {
      curveCache = null; curveFetchPromise = null;
      const s = getState();
      if (isStandalone() && s.hydration) {
        const bundle = await loadHydrationBundle();
        if (bundle) s.hydration = { ...s.hydration, ...bundle, crypto_sleeve: bundle.crypto_sleeve, global: bundle.global, execution: bundle.execution, as_of: bundle.as_of };
      }
      if (s.basisWatch) s.basisWatch.mode = 'live';
      refresh(s, hooks);
    });

    el('btnBwExportCsv')?.addEventListener('click', () => exportCsv(getState()));
    el('btnBwExportPng')?.addEventListener('click', () => exportPng(getState()));
    el('btnBwBarchart')?.addEventListener('click', () => {
      const m = getState()._basisWatchModel || buildModel(getState(), curveCache || { records: [] });
      window.open(m.asset.barchartSpread, '_blank', 'noopener');
    });
    el('btnBwKoyfin')?.addEventListener('click', () => {
      const m = getState()._basisWatchModel || buildModel(getState(), curveCache || { records: [] });
      window.open(m.asset.koyfin, '_blank', 'noopener');
    });
  }

  function init(hooks) {
    initTheme();
    wireControls(hooks.getState, hooks);
    ensureCurveHistory().then(() => refresh(hooks.getState(), hooks));
    window.addEventListener('resize', () => renderPanel(hooks.getState()));
  }

  async function initStandalone() {
    initTheme();
    const params = new URLSearchParams(location.search);
    const prefs = loadPrefs();
    standaloneState = {
      basisWatch: {
        asset: params.get('asset') || prefs.asset || 'BTC',
        view: params.get('view') || prefs.view || 'basis',
        rollLogic: prefs.rollLogic || 'nearest',
        mode: 'live',
        collapsed: false,
      },
      hydration: {},
      btcL3: {},
      provenance: {},
    };

    const bundle = await loadHydrationBundle();
    if (bundle) {
      standaloneState.hydration = {
        crypto_sleeve: bundle.crypto_sleeve,
        global: bundle.global,
        execution: bundle.execution,
        as_of: bundle.as_of,
        node_cockpits: bundle.node_cockpits,
      };
      standaloneState.provenance = { dataAsOf: bundle.as_of, hydratedAt: new Date().toISOString() };
    }

    wireControls(() => standaloneState, {});
    await ensureCurveHistory();
    await refresh(standaloneState, {});
    window.addEventListener('resize', () => renderPanel(standaloneState));

    window.addEventListener('storage', e => {
      if (e.key === PREFS_KEY || e.key === THEME_KEY) {
        if (e.key === THEME_KEY && e.newValue) applyTheme(e.newValue);
        const p = loadPrefs();
        standaloneState.basisWatch = { ...standaloneState.basisWatch, ...p };
        refresh(standaloneState, {});
      }
    });
  }

  global.WTM_BasisWatch = {
    init, initStandalone, render: renderPanel, refresh, exportCsv, exportPng,
    buildModel, ensureCurveHistory, popOutUrl, applyTheme, BW_BUILD,
  };

  if (document.body?.dataset?.bwLayout === 'standalone') {
    document.addEventListener('DOMContentLoaded', () => initStandalone());
  }
})(typeof window !== 'undefined' ? window : globalThis);