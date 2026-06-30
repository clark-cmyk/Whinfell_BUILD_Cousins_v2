#!/usr/bin/env node
/** Headless: renderDataDictionaryBadge after DICTIONARY_META load (simulated refresh). */
import fs from 'fs';
import path from 'path';
import vm from 'vm';
import { fileURLToPath } from 'url';

const REPO = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const HTML_PATH = path.join(REPO, '08_Deliverables/Whinfell_Transmission_Control.html');
const META_JS = path.join(REPO, '08_Deliverables/data_dictionary_meta.js');

function extractScript(html) {
  const m = html.match(/<script>\s*\/\*\* Whinfell Transmission Control[\s\S]*?<\/script>/);
  if (!m) throw new Error('main script block not found');
  let body = m[0].replace(/^<script>\s*/, '').replace(/\s*<\/script>$/, '');
  const cut = body.indexOf("el('btnSave').onclick");
  if (cut >= 0) body = body.slice(0, cut);
  const metaJs = fs.readFileSync(META_JS, 'utf8');
  body = metaJs + '\n' + body + `
renderDataDictionaryBadge();
const loadText = document.getElementById('ddVersionBadge').textContent;
validateDataDictionaryMeta();
renderDataDictionaryBadge();
const refreshText = document.getElementById('ddVersionBadge').textContent;
this.__out = { loadText, refreshText, meta: window.DICTIONARY_META, validated: validateDataDictionaryMeta() };
`;
  return body;
}

function makeSandbox() {
  class El {
    constructor(id) {
      this.id = id; this.textContent = ''; this.title = ''; this.className = '';
      this.classList = { _s: new Set(), toggle(c, f) { if (f) { f ? this._s.add(c) : this._s.delete(c); } else { this._s.has(c) ? this._s.delete(c) : this._s.add(c); } } };
      this.value = ''; this.innerHTML = ''; this.dataset = {}; this.style = {}; this.disabled = false;
    }
    addEventListener() {}
  }
  const els = { ddVersionBadge: new El('ddVersionBadge') };
  const document = {
    getElementById(id) {
      if (!els[id]) els[id] = new El(id);
      return els[id];
    },
    querySelectorAll: () => [],
    querySelector: () => ({ value: 'full' }),
  };
  const sandbox = {
    document, window: { DICTIONARY_META: null }, localStorage: { getItem: () => null, setItem: () => {} },
    console, setTimeout, clearTimeout, Date, JSON, Math, Number, parseInt, parseFloat, Array, Object, Error,
    navigator: { clipboard: { writeText: async () => {} } },
  };
  sandbox.window = sandbox.window;
  return sandbox;
}

const html = fs.readFileSync(HTML_PATH, 'utf8');
const sandbox = makeSandbox();
vm.createContext(sandbox);
vm.runInContext(extractScript(html), sandbox, { filename: 'tc-dd-badge.mjs' });

const out = sandbox.__out;
for (const label of ['loadText', 'refreshText']) {
  const t = out?.[label] || '';
  if (!t.includes('Master Data Dictionary v1.0') || !t.includes('Locked') || !t.includes('Aligned')) {
    console.error(`FAIL ${label}:`, t);
    process.exit(1);
  }
}
if (!out?.validated) {
  console.error('FAIL meta validation');
  process.exit(1);
}
console.log('PASS dd_badge_headless load:', out.loadText);
console.log('PASS dd_badge_headless refresh:', out.refreshText);