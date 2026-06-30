#!/usr/bin/env node
/** Headless: fetch data_dictionary_meta.json → renderDataDictionaryBadge (load + refresh). */
import fs from 'fs';
import path from 'path';
import vm from 'vm';
import { fileURLToPath } from 'url';

const REPO = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const HTML_PATH = path.join(REPO, '08_Deliverables/Whinfell_Transmission_Control.html');
const META_JSON = path.join(REPO, '08_Deliverables/data_dictionary_meta.json');

function extractScript(html) {
  const m = html.match(/<script>\s*\/\*\* Whinfell Transmission Control[\s\S]*?<\/script>/);
  if (!m) throw new Error('main script block not found');
  let body = m[0].replace(/^<script>\s*/, '').replace(/\s*<\/script>$/, '');
  const cut = body.indexOf("el('btnSave').onclick");
  if (cut >= 0) body = body.slice(0, cut);
  const metaPayload = fs.readFileSync(META_JSON, 'utf8');
  body += `
const __metaPayload = ${metaPayload};
let __fetchCount = 0;
globalThis.fetch = () => {
  __fetchCount += 1;
  return Promise.resolve({ ok: true, json: async () => JSON.parse(JSON.stringify(__metaPayload)) });
};
(async () => {
  await fetchDataDictionaryMeta(true);
  applyDataDictionaryBadge(ddMetaCache, validateDataDictionaryMeta(ddMetaCache));
  await fetchDataDictionaryMeta(true);
  renderDataDictionaryBadge(true);
  await new Promise(r => setTimeout(r, 5));
  globalThis.__ddOut = {
    fetchCount: __fetchCount,
    badgeText: document.getElementById('ddVersionBadge').textContent,
    meta: ddMetaCache,
    validated: validateDataDictionaryMeta(ddMetaCache),
  };
})();
`;
  return body;
}

function makeSandbox() {
  class El {
    constructor(id) {
      this.id = id; this.textContent = 'Loading dictionary…'; this.title = ''; this.className = '';
      this.classList = { _s: new Set(), toggle(c, f) { if (f === true) this._s.add(c); else if (f === false) this._s.delete(c); else this._s.has(c) ? this._s.delete(c) : this._s.add(c); } };
      this.value = ''; this.innerHTML = ''; this.dataset = {}; this.style = {}; this.disabled = false;
    }
    addEventListener() {}
  }
  const els = { ddVersionBadge: new El('ddVersionBadge') };
  return {
    document: {
      getElementById(id) { if (!els[id]) els[id] = new El(id); return els[id]; },
      querySelectorAll: () => [],
      querySelector: () => ({ value: 'full' }),
    },
    window: {}, localStorage: { getItem: () => null, setItem: () => {} },
    console, setTimeout, clearTimeout, Date, JSON, Math, Number, parseInt, parseFloat, Array, Object, Error, Promise,
    navigator: { clipboard: { writeText: async () => {} } },
  };
}

const sandbox = makeSandbox();
vm.createContext(sandbox);
vm.runInContext(extractScript(fs.readFileSync(HTML_PATH, 'utf8')), sandbox, { filename: 'tc-dd-badge.mjs' });

setTimeout(() => {
  const out = sandbox.__ddOut;
  if (!out) { console.error('FAIL no output'); process.exit(1); }
  if (out.fetchCount < 2) { console.error('FAIL fetchCount', out.fetchCount); process.exit(1); }
  if (!out.badgeText?.includes('Master Data Dictionary v1.0')) { console.error('FAIL badge', out.badgeText); process.exit(1); }
  if (!out.validated) { console.error('FAIL validation', out.meta); process.exit(1); }
  console.log('PASS dd_badge_headless fetch x' + out.fetchCount + ':', out.badgeText);
  process.exit(0);
}, 200);