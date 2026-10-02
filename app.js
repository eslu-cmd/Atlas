// Minimal M1 proof wiring. No framework. Zero visual polish by design — the
// Claude Design brief governs the real interface.

const $ = (sel) => document.querySelector(sel);
const outputs = {
  health: $('[data-output="health"]'),
  'known-answers-summary': $('[data-output="known-answers-summary"]'),
  'known-answers-detail': $('[data-output="known-answers-detail"]'),
  encode: $('[data-output="encode"]'),
  alloc: $('[data-output="alloc"]'),
  'alloc-list': $('[data-output="alloc-list"]'),
  txn: $('[data-output="txn"]'),
  unauthorized: $('[data-output="unauthorized"]'),
};

function set(target, data) {
  const el = outputs[target];
  if (!el) return;
  if (typeof data === 'string') el.textContent = data;
  else el.textContent = JSON.stringify(data, null, 2);
}

function setSummary(target, html) {
  const el = outputs[target];
  if (!el) return;
  el.innerHTML = html;
}

async function callJson(method, url, body) {
  const init = { method, headers: { 'Content-Type': 'application/json' } };
  if (body !== undefined) init.body = JSON.stringify(body);
  const res = await fetch(url, init);
  const text = await res.text();
  let parsed;
  try { parsed = JSON.parse(text); } catch { parsed = text; }
  return { status: res.status, body: parsed };
}

function val(name) { return $(`[data-input="${name}"]`).value; }

async function doHealth() {
  set('health', await callJson('GET', '/api/health'));
}

async function doKnownAnswers() {
  const { status, body } = await callJson('GET', '/api/known_answers');
  const pass = body?.all_pass;
  const cls = pass ? 'ok' : 'fail';
  const ex = body?.canonical_examples;
  const suite = body?.engine_suite;
  setSummary('known-answers-summary',
    `<div class="summary">status <code>${status}</code> · ` +
    `<span class="${cls}">${pass ? 'PASS' : 'FAIL'}</span> · ` +
    `canonical examples ${ex?.passed}/${ex?.total} · ` +
    `engine suite ${suite?.passed}/${suite?.run} · ` +
    `engine ${ex?.versions?.engine} · dict ${ex?.versions?.dictionary}</div>`);
  set('known-answers-detail', body);
}

async function doEncode() {
  let facts;
  try { facts = JSON.parse(val('encode')); }
  catch (e) { set('encode', `invalid JSON: ${e.message}`); return; }
  set('encode', await callJson('POST', '/api/encode', { facts }));
}

async function doAllocate() {
  const body = {
    namespace: val('alloc-namespace'),
    scope: val('alloc-scope'),
    token: val('alloc-token'),
    meaning: val('alloc-meaning'),
    actor: val('alloc-actor'),
    reason: val('alloc-reason'),
  };
  set('alloc', await callJson('POST', '/api/dictionary_allocate', body));
}

async function doAllocateList() {
  set('alloc-list', await callJson('GET', '/api/dictionary_allocate'));
}

async function doTxn(mode) {
  const body = {
    idempotency_key: val('txn-key'),
    payload: safeParse(val('txn-payload'), {}),
    actor: val('txn-actor'),
    reason: val('txn-reason'),
    mode,
  };
  set('txn', await callJson('POST', '/api/txn_proof', body));
}

async function doTxnGet() {
  const key = encodeURIComponent(val('txn-key'));
  set('txn', await callJson('GET', `/api/txn_proof?key=${key}`));
}

function safeParse(s, fallback) {
  try { return JSON.parse(s); } catch { return fallback; }
}

async function doUnauthorized() {
  // Attempt a direct write to Supabase REST API with the public anon key.
  // RLS must reject the insert (no insert policy for anon). This proves the
  // trusted-service boundary: only the server-side service role can write.
  const url = window.ATLAS_PUBLIC?.SUPABASE_URL;
  const key = window.ATLAS_PUBLIC?.SUPABASE_ANON_KEY;
  if (!url || !key) {
    set('unauthorized', { error: 'public config missing — ensure /api/public-config returned Supabase URL + anon key' });
    return;
  }
  const res = await fetch(`${url}/rest/v1/atlas_m1_proof`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'apikey': key,
      'Authorization': `Bearer ${key}`,
      'Prefer': 'return=representation',
    },
    body: JSON.stringify({
      idempotency_key: 'unauthorized-attempt-' + Date.now(),
      payload: { attempt: 'anon direct write — should be rejected' },
      actor: 'anon-browser',
      reason: 'unauthorized rejection test',
    }),
  });
  const text = await res.text();
  let parsed; try { parsed = JSON.parse(text); } catch { parsed = text; }
  const rejected = res.status === 401 || res.status === 403 || /row-level security/i.test(JSON.stringify(parsed));
  setSummary('unauthorized',
    `<div class="summary"><span class="${rejected ? 'ok' : 'fail'}">${rejected ? 'REJECTED (good)' : 'ACCEPTED (bad — RLS leak)'}</span> · HTTP ${res.status}</div>`);
  outputs.unauthorized.textContent += '\n' + JSON.stringify(parsed, null, 2);
}

// Fetch public config so the frontend knows the Supabase URL + anon key
async function loadPublicConfig() {
  try {
    const { body } = await callJson('GET', '/api/public_config');
    window.ATLAS_PUBLIC = body;
  } catch { /* unauthorized test will show the error */ }
}

document.addEventListener('click', (ev) => {
  const btn = ev.target.closest('[data-action]');
  if (!btn) return;
  const action = btn.dataset.action;
  const handlers = {
    'health': doHealth,
    'known-answers': doKnownAnswers,
    'encode': doEncode,
    'alloc': doAllocate,
    'alloc-list': doAllocateList,
    'txn-write': () => doTxn('write'),
    'txn-rollback': () => doTxn('rollback'),
    'txn-retry': () => doTxn('retry'),
    'txn-get': doTxnGet,
    'unauthorized': doUnauthorized,
  };
  const fn = handlers[action];
  if (fn) fn().catch(err => console.error(action, err));
});

loadPublicConfig();
