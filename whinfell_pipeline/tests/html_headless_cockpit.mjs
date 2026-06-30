#!/usr/bin/env node
/** Headless Phase 2 cockpit: RV chart, focus, compare, rail navigation. */
import fs from 'fs';
import path from 'path';
import vm from 'vm';
import { fileURLToPath } from 'url';

const REPO = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const HTML_PATH = path.join(REPO, '08_Deliverables/Whinfell_Transmission_Control.html');
const CHINA_MODELS_JS = path.join(REPO, '08_Deliverables/desk_china_ladder_models.js');
const META_JSON = path.join(REPO, '08_Deliverables/data_dictionary_meta.json');
const COCKPIT_BUNDLE = path.join(REPO, 'whinfell_pipeline/examples/cockpit_hydration_snippet.json');

const REQUIRED_FNS = [
  'drawRvBasisChart', 'toggleFocusMode', 'toggleCompareMode', 'setActiveNode',
  'renderNodeCockpitShell', 'flipNode', 'hydrateFromBundle', 'mergeNodeCockpit',
];

function extractBadgeDefault(html) {
  const m = html.match(/window\.DICTIONARY_BADGE_DEFAULT\s*=\s*(\{[\s\S]*?\});/);
  if (!m) throw new Error('DICTIONARY_BADGE_DEFAULT not found in HTML');
  return JSON.parse(m[1]);
}

function extractScript(html) {
  const chinaModels = fs.readFileSync(CHINA_MODELS_JS, 'utf8');
  const badgeDefault = extractBadgeDefault(html);
  const metaPayload = JSON.parse(fs.readFileSync(META_JSON, 'utf8'));
  const m = html.match(/<script>\s*\/\*\* Whinfell Transmission Control[\s\S]*?<\/script>/);
  if (!m) throw new Error('main script block not found');
  const ddStub = `
window.DICTIONARY_BADGE_DEFAULT = ${JSON.stringify(badgeDefault)};
globalThis.fetch = () => Promise.resolve({
  ok: true,
  json: async () => JSON.parse(JSON.stringify(${JSON.stringify(metaPayload)})),
});
`;
  let body = ddStub + chinaModels + '\n' + m[0].replace(/^<script>\s*/, '').replace(/\s*<\/script>$/, '');
  const cut = body.indexOf("el('btnSave').onclick");
  if (cut >= 0) body = body.slice(0, cut);
  body += `
appState = createEmptyState();
this.__test = {
  LADDER, RV_HORIZONS, appState, hydrateFromBundle, mergeNodeCockpit,
  drawRvBasisChart, toggleFocusMode, toggleCompareMode, setActiveNode,
  renderNodeCockpitShell, flipNode, jumpToNode, activeNodeId, applyWorkspaceView,
  applyCompareSelection, buildStateFromDOM, createEmptyState, createEmptyNavigation, document,
};
`;
  return body;
}

function makeSandbox() {
  class CList {
    constructor() { this._set = new Set(); }
    add(...c) { c.forEach(x => this._set.add(x)); }
    remove(...c) { c.forEach(x => this._set.delete(x)); }
    toggle(c, force) {
      if (force === true) { this._set.add(c); return true; }
      if (force === false) { this._set.delete(c); return false; }
      if (this._set.has(c)) { this._set.delete(c); return false; }
      this._set.add(c); return true;
    }
    contains(c) { return this._set.has(c); }
  }

  class El {
    constructor(id) {
      this.id = id;
      this.value = '';
      this.textContent = '';
      this.className = '';
      this.innerHTML = '';
      this.disabled = false;
      this.dataset = {};
      this.style = {};
      this.classList = new CList();
      this.scrollTop = 0;
      this._listeners = {};
      if (id === 'cockpitRvCanvas') {
        this.parentElement = {
          getBoundingClientRect: () => ({ width: 400, height: 240 }),
        };
      }
    }
    addEventListener() {}
    get onclick() { return this._onclk; }
    set onclick(fn) { this._onclk = fn; }
    get onchange() { return this._onchg; }
    set onchange(fn) { this._onchg = fn; }
    querySelectorAll(sel) {
      if (sel === '[data-node-id]') {
        return Object.values(els).filter(e => e.dataset?.nodeId);
      }
      if (sel === '[data-horizon]') return [];
      return [];
    }
    querySelector() { return null; }
  }

  const els = {};
  const ctx2d = {
    setTransform() {},
    clearRect() {},
    beginPath() {},
    moveTo() {},
    lineTo() {},
    stroke() {},
    fillRect() {},
    fillText() {},
    arc() {},
    fill() {},
  };

  return {
    document: {
      getElementById(id) {
        if (!els[id]) els[id] = new El(id);
        const el = els[id];
        if (id === 'cockpitRvCanvas') {
          el.getContext = (type) => (type === '2d' ? ctx2d : null);
        }
        return el;
      },
      querySelectorAll(sel) {
        if (sel === '[data-node-id]') {
          return Object.values(els).filter(e => e.dataset?.nodeId);
        }
        return [];
      },
      querySelector(sel) {
        if (sel === '#cockpitShell .cockpit-main') {
          if (!els._cockpitMain) els._cockpitMain = new El('cockpitMain');
          return els._cockpitMain;
        }
        return null;
      },
    },
    localStorage: { _data: {}, getItem(k) { return this._data[k] ?? null; }, setItem(k, v) { this._data[k] = v; } },
    window: { open() {}, devicePixelRatio: 1 },
    navigator: { clipboard: { writeText: async () => {}, readText: async () => '' } },
    console, setTimeout, clearTimeout, Date, JSON, Math, Number, parseInt, parseFloat, Array, Object, Error,
    _els: els,
  };
}

function seedCockpitDom(t) {
  const ids = [
    'nodeRail', 'cockpitShell', 'cockpitChartTitle', 'cockpitChartSubtitle',
    'cockpitHorizonPills', 'cockpitRvCanvas', 'cockpitChartPlaceholder',
    'cockpitChartValue', 'cockpitChartRichness', 'cockpitChartPct',
    'cockpitDecisionRail', 'cockpitDetailBand', 'cockpitFocusLayer',
    'cockpitCompareLayer', 'btnHeresWhy', 'btnCompareMode', 'nodeCockpitZone',
    'legacyConsoleZone', 'btnWorkspaceToggle',
    'whinfellScore', 'transmissionState', 'regimeTag', 'grossA', 'grossB',
  ];
  ids.forEach(id => t.document.getElementById(id));
}

function boot(script) {
  const ctx = makeSandbox();
  vm.createContext(ctx);
  vm.runInContext(script, ctx);
  const t = ctx.__test;
  if (!t) throw new Error('__test missing');
  for (const fn of REQUIRED_FNS) {
    if (typeof t[fn] !== 'function') throw new Error(`missing function: ${fn}`);
  }
  return t;
}

function hydrateCockpit(t, bundle) {
  seedCockpitDom(t);
  t.appState.ui = t.appState.ui || {};
  t.appState.ui.workspaceView = 'cockpit';
  t.hydrateFromBundle(bundle);
}

function testDrawRvBasisChart(t, bundle) {
  hydrateCockpit(t, bundle);
  const cockpit = t.mergeNodeCockpit('basis', t.buildStateFromDOM());
  const canvas = t.document.getElementById('cockpitRvCanvas');
  const result = t.drawRvBasisChart(cockpit, canvas);
  if (!result.drew) throw new Error('drawRvBasisChart did not draw');
  if (result.pointCount !== 5) throw new Error(`expected 5 horizon points, got ${result.pointCount}`);
  t.renderNodeCockpitShell(t.buildStateFromDOM());
  const title = t.document.getElementById('cockpitChartTitle').textContent;
  if (!title || title === '—') throw new Error(`chart title not set: ${title}`);
  return { drew: true, pointCount: result.pointCount, title };
}

function testFocusMode(t, bundle) {
  hydrateCockpit(t, bundle);
  t.toggleFocusMode(true);
  if (!t.appState.navigation.focus_mode) throw new Error('focus_mode not set');
  const layer = t.document.getElementById('cockpitFocusLayer');
  if (layer.classList.contains('zone-hidden')) throw new Error('focus layer hidden when active');
  if (!layer.innerHTML.includes('Thesis')) throw new Error('focus layer missing thesis block');
  t.toggleFocusMode(false);
  if (t.appState.navigation.focus_mode) throw new Error('focus_mode not cleared');
  return { focusToggle: true, thesisRendered: true };
}

function testCompareMode(t, bundle) {
  hydrateCockpit(t, bundle);
  t.setActiveNode('credit');
  t.toggleCompareMode(true);
  if (t.appState.navigation.view_mode !== 'compare') throw new Error('view_mode not compare');
  t.applyCompareSelection('liquidity');
  const ids = t.appState.navigation.compare_node_ids || [];
  if (!ids.includes('credit') || !ids.includes('liquidity')) {
    throw new Error(`compare ids unexpected: ${JSON.stringify(ids)}`);
  }
  const layer = t.document.getElementById('cockpitCompareLayer');
  if (layer.classList.contains('zone-hidden')) throw new Error('compare layer hidden when active');
  if (!layer.innerHTML.includes('compare-card')) throw new Error('compare cards not rendered');
  t.toggleCompareMode(false);
  if (t.appState.navigation.view_mode !== 'flip') throw new Error('view_mode not restored to flip');
  return { compareToggle: true, cardCount: (layer.innerHTML.match(/compare-card/g) || []).length };
}

function testRailNavigation(t, bundle) {
  hydrateCockpit(t, bundle);
  t.setActiveNode('highbeta');
  if (t.activeNodeId() !== 'highbeta') throw new Error(`setActiveNode failed: ${t.activeNodeId()}`);
  t.flipNode(1);
  if (t.activeNodeId() !== 'basis') throw new Error(`flipNode forward failed: ${t.activeNodeId()}`);
  t.jumpToNode('liquidity');
  if (t.activeNodeId() !== 'liquidity') throw new Error(`jumpToNode failed: ${t.activeNodeId()}`);
  t.renderNodeCockpitShell(t.buildStateFromDOM());
  const rail = t.document.getElementById('nodeRail');
  if (!rail.innerHTML.includes('node-rail-tab')) throw new Error('node rail not rendered');
  return { activeNode: t.activeNodeId(), railRendered: true };
}

function runSuite(script, bundle, label) {
  return {
    label,
    chart: testDrawRvBasisChart(boot(script), bundle),
    focus: testFocusMode(boot(script), bundle),
    compare: testCompareMode(boot(script), bundle),
    navigation: testRailNavigation(boot(script), bundle),
  };
}

const html = fs.readFileSync(HTML_PATH, 'utf8');
const bundle = JSON.parse(fs.readFileSync(COCKPIT_BUNDLE, 'utf8'));
const script = extractScript(html);

const run1 = runSuite(script, bundle, 'run1');
const run2 = runSuite(script, bundle, 'run2');

const snap = (run) => {
  const { label: _l, ...rest } = run;
  return rest;
};
if (JSON.stringify(snap(run1)) !== JSON.stringify(snap(run2))) {
  throw new Error(`run1/run2 mismatch: ${JSON.stringify({ run1: snap(run1), run2: snap(run2) })}`);
}

const out = [
  'html_headless_cockpit_ok',
  `Required functions: ${REQUIRED_FNS.join(', ')}.`,
  'Blocks: drawRvBasisChart (5 horizons), toggleFocusMode, toggleCompareMode, setActiveNode/flipNode.',
  'Executed twice (run1, run2) with identical snapshots.',
  JSON.stringify(run1, null, 2),
].join('\n');
console.log(out);