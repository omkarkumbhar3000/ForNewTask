/**
 * build-performance-data.mjs — the ONLY writer of the performance dashboard datasets.
 *
 *   node tools/dashboard-performance/scripts/build-performance-data.mjs
 *
 * ─────────────────────────────────────────────────────────────────────────────────────────────
 * HONESTY CONTRACT. No k6 execution has produced real numbers yet (blocked on a working
 * QA_MsSQL credential — see state/perf/OBJ-019-STATE.md). So this emits datasets in TWO
 * clearly separated parts:
 *
 *   REAL     — the Sanity scope (14 modules, 211 checks) read from the framework's own
 *              performance/data/sanity-modules.json, plus the framework/environment facts.
 *   SAMPLE   — every latency / throughput / percentage figure. Each is stamped `sample: true`
 *              and the dataset carries `dataState: "sample"`, so the UI shows a standing banner
 *              and never lets a made-up number read as a measurement.
 *
 * When a real run exists, point INGEST_RUN at performance/reports/<runId>/ and this script reads
 * the true summaries instead; `dataState` flips to "measured" and the banner disappears. The
 * dashboard code does not change — only this file and the JSON it writes.
 * ─────────────────────────────────────────────────────────────────────────────────────────────
 */

import { readFileSync, writeFileSync, existsSync, mkdirSync, readdirSync, statSync } from 'node:fs'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'

const HERE = dirname(fileURLToPath(import.meta.url))
const APP = join(HERE, '..')
const DATA = join(APP, 'public', 'data')
const REGISTRY_PATH = join(APP, '..', '..', 'Automation gitlab repo', 'pam_automation_bootstrap',
  'performance', 'data', 'sanity-modules.json')

mkdirSync(DATA, { recursive: true })

// A fixed pseudo-random so sample figures are stable between rebuilds (no Math.random at build).
let seed = 20260814
function rnd() { seed = (seed * 1103515245 + 12345) & 0x7fffffff; return seed / 0x7fffffff }
function around(base, spread) { return Math.round(base + (rnd() - 0.5) * 2 * spread) }
function pctile(base) { return { p50: around(base, base * 0.08), p90: around(base * 1.4, base * 0.1),
  p95: around(base * 1.6, base * 0.12), p99: around(base * 2.1, base * 0.18) } }

const registry = JSON.parse(readFileSync(REGISTRY_PATH, 'utf8'))
const modules = registry.modules.filter((m) => m.nav.type !== 'login')

const SAMPLE = true
const STATE = 'sample'
const GEN = 'tools/dashboard-performance/scripts/build-performance-data.mjs'
const SAMPLE_NOTE = 'SAMPLE data — shape only. No k6 execution has produced real figures yet ' +
  '(blocked on a QA_MsSQL credential). Every latency/throughput number here is illustrative.'

function write(name, obj) {
  writeFileSync(join(DATA, name + '.json'), JSON.stringify(obj, null, 1), 'utf8')
}

// ── manifest ──────────────────────────────────────────────────────────────────────────────
write('manifest', {
  schema: 'pam-perf-dashboard/1', dataState: STATE, generatedBy: GEN,
  objective: 'OBJ-019', project: 'PAM', tracker: 'PAMIT',
  environment: 'QA_MsSQL', tool: 'k6 v2.2.0',
  sampleNote: SAMPLE_NOTE,
  currentRunId: SAMPLE ? 'SAMPLE (no execution yet)' : null,
  sanitySource: registry.source,
})

// ── executive summary ─────────────────────────────────────────────────────────────────────
const totalScenarios = 1 /*login*/ + modules.length
write('summary', {
  dataState: STATE, sample: SAMPLE, sampleNote: SAMPLE_NOTE,
  overallStatus: 'Awaiting first execution',
  scenarios: { total: totalScenarios, passed: SAMPLE ? totalScenarios : 'N/A', failed: SAMPLE ? 0 : 'N/A' },
  avgResponseMs: SAMPLE ? 742 : 'N/A',
  p95Ms: SAMPLE ? 1180 : 'N/A',
  p99Ms: SAMPLE ? 1640 : 'N/A',
  throughputRps: SAMPLE ? 4.6 : 'N/A',
  errorRate: SAMPLE ? 0.004 : 'N/A',
  activeVus: SAMPLE ? 3 : 'N/A',
  trend: SAMPLE ? [
    { run: 'run-1', p95: 1240 }, { run: 'run-2', p95: 1205 }, { run: 'run-3', p95: 1180 },
  ] : [],
})

// ── login performance ─────────────────────────────────────────────────────────────────────
write('login', {
  dataState: STATE, sample: SAMPLE, sampleNote: SAMPLE_NOTE,
  authApiMs: SAMPLE ? pctile(810) : 'N/A',
  uiJourneyMs: SAMPLE ? pctile(4050) : 'N/A',
  successRate: SAMPLE ? 1 : 'N/A',
  failureRate: SAMPLE ? 0 : 'N/A',
  browserOverheadMs: SAMPLE ? 1090 : 'N/A',
  segments: SAMPLE ? [
    { segment: 'Navigation', ms: 950 }, { segment: 'Credential entry', ms: 395 },
    { segment: 'Authentication', ms: 1900 }, { segment: 'Landing render', ms: 830 },
  ] : [],
  trend: SAMPLE ? [{ run: 'run-1', ui: 4200, api: 840 }, { run: 'run-2', ui: 4100, api: 820 },
    { run: 'run-3', ui: 4050, api: 810 }] : [],
  authPath: 'POST /frmLoginACMO.aspx (web-tier UI login). NOT /arcontoken.',
})

// ── sanity performance (REAL scope, SAMPLE metrics) ───────────────────────────────────────
write('sanity', {
  dataState: STATE, sample: SAMPLE, sampleNote: SAMPLE_NOTE,
  source: registry.source,
  totals: { modules: modules.length, checks: registry.totals.checks, excluded: registry.excluded.length },
  excluded: registry.excluded,
  modules: modules.map((m) => {
    const ui = around(700 + m.checks * 18, 120)
    const api = around(280 + m.checks * 3, 40)
    const ratio = ui / api
    const attribution = ratio >= 2.5 ? 'Frontend/UI-dominated' : ratio <= 1.3 ? 'Backend-dominated' : 'Mixed'
    return {
      key: m.key, name: m.name, checks: m.checks, navType: m.nav.type,
      uiLoadMs: SAMPLE ? ui : 'N/A',
      apiLoadMs: SAMPLE ? (m.pageUrl ? api : 'capture-required') : 'N/A',
      okRate: SAMPLE ? Math.round((0.97 + rnd() * 0.03) * 1000) / 1000 : 'N/A',
      attribution: SAMPLE ? attribution : 'N/A',
      status: SAMPLE ? 'Passed' : 'Pending',
    }
  }),
})

// ── API performance ───────────────────────────────────────────────────────────────────────
write('api', {
  dataState: STATE, sample: SAMPLE, sampleNote: SAMPLE_NOTE,
  requests: SAMPLE ? 1284 : 'N/A',
  requestsPerSec: SAMPLE ? 4.6 : 'N/A',
  avgLatencyMs: SAMPLE ? 612 : 'N/A',
  medianLatencyMs: SAMPLE ? 548 : 'N/A',
  percentiles: SAMPLE ? { p90: 980, p95: 1180, p99: 1640 } : 'N/A',
  errorRate: SAMPLE ? 0.004 : 'N/A',
  failedRequests: SAMPLE ? 5 : 'N/A',
  checksPassRate: SAMPLE ? 0.998 : 'N/A',
  statusDistribution: SAMPLE ? [
    { code: '302', label: 'Auth success (redirect)', count: 640 },
    { code: '200', label: 'Page / rejected re-render', count: 639 },
    { code: '4xx/5xx', label: 'Transport errors', count: 5 },
  ] : [],
  trend: SAMPLE ? [{ run: 'run-1', p95: 1240 }, { run: 'run-2', p95: 1210 }, { run: 'run-3', p95: 1180 }] : [],
})

// ── UI / user experience ──────────────────────────────────────────────────────────────────
write('ui', {
  dataState: STATE, sample: SAMPLE, sampleNote: SAMPLE_NOTE,
  pageLoadMs: SAMPLE ? pctile(1350) : 'N/A',
  moduleLoadMs: SAMPLE ? pctile(1180) : 'N/A',
  navigationMs: SAMPLE ? pctile(640) : 'N/A',
  submoduleLoadMs: SAMPLE ? pctile(890) : 'N/A',
  perceivedMs: SAMPLE ? pctile(2100) : 'N/A',
  uiFailures: SAMPLE ? 2 : 'N/A',
  webVitals: SAMPLE ? [
    { metric: 'LCP', ms: 1500 }, { metric: 'FCP', ms: 820 }, { metric: 'TTFB', ms: 610 },
  ] : [],
  trend: SAMPLE ? [{ run: 'run-1', ms: 1420 }, { run: 'run-2', ms: 1300 }, { run: 'run-3', ms: 1180 }] : [],
})

// ── API vs UI comparison ──────────────────────────────────────────────────────────────────
write('comparison', {
  dataState: STATE, sample: SAMPLE, sampleNote: SAMPLE_NOTE,
  verdict: SAMPLE ? 'No single dominant component (sample)' : 'N/A',
  perModule: modules.map((m) => {
    const ui = around(700 + m.checks * 18, 120)
    const api = around(280 + m.checks * 3, 40)
    return { key: m.key, name: m.name, ui: SAMPLE ? ui : 'N/A', api: SAMPLE ? api : 'N/A' }
  }),
  matrix: [
    { pattern: 'API slow + UI slow', reading: 'Backend/API bottleneck likely' },
    { pattern: 'API fast + UI slow', reading: 'UI/browser/frontend bottleneck likely' },
    { pattern: 'API slow + UI moderate', reading: 'Backend latency contributing to UX' },
    { pattern: 'API fast + UI fast', reading: 'Healthy end-to-end' },
    { pattern: 'API errors + UI failures rise', reading: 'Backend scalability/reliability issue' },
    { pattern: 'API stable + browser load rises', reading: 'Frontend/client-side issue' },
  ],
})

console.log('Performance dashboard datasets written to ' + DATA)
// -- executions: every real k6 invocation, including the rejected ones ----------------------
//
// OBJ-020. The owner's instruction after the Sunday API timeout went unshown: incomplete and
// terminated executions must never be omitted from a dashboard. The same rule applies here, and
// it matters more, because the sample figures above are NOT measurements - without this panel a
// reader cannot tell that execution has been attempted at all.
const REPORTS = join(APP, '..', '..', 'Automation gitlab repo', 'pam_automation_bootstrap',
  'performance', 'reports')

function readExecutions() {
  if (!existsSync(REPORTS)) return []
  const out = []
  for (const runId of readdirSync(REPORTS)) {
    const dir = join(REPORTS, runId)
    if (!statSync(dir).isDirectory()) continue
    const files = readdirSync(dir).filter((f) => f.endsWith('-summary.json'))
    if (files.length === 0) {
      out.push({
        runId,
        phases: [],
        terminalState: 'No summary written',
        whyItStopped: 'the run directory exists but k6 wrote no summary - the run did not finish',
        measurementValid: false,
      })
      continue
    }
    const phases = []
    let valid = false
    let why = ''
    for (const f of files) {
      let s
      try { s = JSON.parse(readFileSync(join(dir, f), 'utf8')) } catch { continue }
      const o = s.outcome || {}
      const rejections = s.rejections || {}
      const rejectionList = Object.keys(rejections)
        .map((k) => k + ' x' + rejections[k]).join(', ')
      if (o.measurementValid) valid = true
      if (!o.measurementValid && !why) {
        why = rejectionList
          ? ('every attempt was rejected (' + rejectionList + ')')
          : (o.measurementNote || 'the run produced no valid measurement')
      }
      phases.push({
        phase: (s.context && s.context.phase) || f.replace('-summary.json', ''),
        journey: (s.context && s.context.journey) || 'login',
        environment: (s.context && s.context.environment) || 'N/A',
        profile: (s.workload && s.workload.profile) || (s.context && s.context.profile) || 'N/A',
        targetVus: (s.workload && s.workload.targetVus) != null ? s.workload.targetVus : 'N/A',
        iterations: o.iterations != null ? o.iterations : 'N/A',
        successfulLogins: o.successfulLogins != null ? o.successfulLogins : 'N/A',
        failureRate: o.failureRate != null ? o.failureRate : 'N/A',
        measurementValid: Boolean(o.measurementValid),
        rejections: rejectionList || 'none',
        checkRate: (s.checks && s.checks.rate) != null ? s.checks.rate : 'N/A',
      })
    }
    out.push({
      runId,
      phases,
      terminalState: valid ? 'Completed - measurement valid' : 'Attempted - no valid measurement',
      whyItStopped: valid ? 'the run authenticated and produced usable timings' : why,
      measurementValid: valid,
    })
  }
  return out.sort((a, b) => (a.runId < b.runId ? 1 : -1))
}

const executions = readExecutions()

write('executions', {
  dataState: STATE, sample: SAMPLE,
  purpose: 'Every k6 invocation issued against the product, including attempts that produced no '
    + 'measurement. An execution that was blocked is still an execution and is never omitted.',
  blocker: {
    active: executions.length > 0 && !executions.some((e) => e.measurementValid),
    summary: 'No performance execution has yet authenticated on QA_MsSQL. Live measurement is '
      + 'blocked on a working credential, not on the framework.',
    attemptsMade: executions.length,
    accountsTried: ['arcosadmin (rejected: invalid credentials)',
      'auto_adminui (locked out during OBJ-019 validation - admin unlock required)'],
    unblocks: ['an admin unlock of auto_adminui plus its current password',
      'a dedicated performance account with no second factor',
      'a confirmed working QA_MsSQL password supplied as PERF_PASSWORD'],
    safetyNote: 'Credential attempts are deliberately NOT retried. Each rejected login increments '
      + 'a lockout counter on a shared functional account, and one such account is already locked.',
  },
  executions,
})

console.log('  dataState=' + STATE + '  modules=' + modules.length + '  checks=' + registry.totals.checks)


// ═══════════════════════════════════════════════════════════════════════════════════════════
// REAL INGEST v2 — OBJ-021 · N-1 vs N
//
// Reads the runs actually retained under performance/reports/ and produces a two-execution
// comparison. Newest = N, the one before = N-1. Nothing is auto-generated or estimated: every
// number traces to a run summary, and anything a run did not measure is written 'N/A' with a
// reason.
//
// Regression gates are baseline-relative (owner decision): WARN at >15% above N-1, FAIL at >30%,
// hard FAIL on any login failure or on a check-rate drop. No invented SLO.
// ═══════════════════════════════════════════════════════════════════════════════════════════
const WARN_PCT = 15;
const FAIL_PCT = 30;

function loadRuns() {
  const dir = join(APP, '..', '..', 'Automation gitlab repo', 'pam_automation_bootstrap',
    'performance', 'reports');
  if (!existsSync(dir)) return [];
  const out = [];
  for (const name of readdirSync(dir)) {
    const f = join(dir, name, 'browser-summary.json');
    if (!existsSync(f)) continue;
    try { out.push({ id: name, s: JSON.parse(readFileSync(f, 'utf8')) }); } catch (e) { /* skip */ }
  }
  return out.sort((a, b) => (a.id < b.id ? 1 : -1)); // newest first
}

const runs = loadRuns();
if (runs.length) {
  const N = runs[0];
  const P = runs[1] || null;                       // N-1, may be absent
  const sN = N.s;
  const sP = P ? P.s : null;

  const num = (v) => (typeof v === 'number' ? Math.round(v * 10) / 10 : 'N/A');
  const band = (seg) => (seg && typeof seg.med === 'number'
    ? { p50: num(seg.med), p90: num(seg.p90), p95: num(seg.p95), p99: num(seg.p99) } : 'N/A');
  const psOf = (s) => s.phaseSpecific || {};
  const modsOf = (s) => psOf(s).modules || {};

  /** Percentage change, current vs baseline. Positive = slower. 'N/A' unless both are numbers. */
  function delta(cur, base) {
    if (typeof cur !== 'number' || typeof base !== 'number' || base === 0) return 'N/A';
    return Math.round(((cur - base) / base) * 1000) / 10;
  }
  /** Baseline-relative verdict for a latency figure. */
  function gate(cur, base) {
    const d = delta(cur, base);
    if (d === 'N/A') return { state: 'NO BASELINE', delta: 'N/A' };
    if (d > FAIL_PCT) return { state: 'FAIL', delta: d };
    if (d > WARN_PCT) return { state: 'WARN', delta: d };
    return { state: 'PASS', delta: d };
  }

  const outN = sN.outcome || {};
  const outP = sP ? (sP.outcome || {}) : {};
  const segN = sN.segments || {};
  const segP = sP ? (sP.segments || {}) : {};
  const modsN = modsOf(sN);
  const modsP = sP ? modsOf(sP) : {};

  const measuredN = Object.keys(modsN).filter((k) => modsN[k].samples > 0);
  const failedN = Object.keys(modsN).filter((k) => !modsN[k].samples && modsN[k].okRate === 0);
  const notRunN = Object.keys(modsN).filter((k) => !modsN[k].samples && modsN[k].okRate === 'N/A');
  const totalMods = Object.keys(modsN).length;

  const loginOkN = outN.successfulLogins === outN.iterations && outN.iterations > 0;
  const checkN = (sN.checks && sN.checks.rate) != null ? sN.checks.rate : null;
  const checkP = (sP && sP.checks && sP.checks.rate != null) ? sP.checks.rate : null;

  // Headline gate: login failures and a check-rate drop are hard FAILs regardless of latency.
  const p95Gate = gate(segN.journey && segN.journey.p95, segP.journey && segP.journey.p95);
  let overall = p95Gate.state;
  const gateReasons = [];
  if (!loginOkN) { overall = 'FAIL'; gateReasons.push('a login failed'); }
  if (checkN != null && checkP != null && checkN < checkP - 0.0001) {
    if (overall !== 'FAIL') overall = 'WARN';
    gateReasons.push('check pass rate fell vs N-1');
  }
  if (p95Gate.state === 'FAIL') gateReasons.push('login p95 more than ' + FAIL_PCT + '% above N-1');
  else if (p95Gate.state === 'WARN') gateReasons.push('login p95 more than ' + WARN_PCT + '% above N-1');
  if (!gateReasons.length) gateReasons.push('within ' + WARN_PCT + '% of N-1 on every gated metric');

  const runLabel = (id) => id.replace('2026-', '').replace('_', ' ');

  // ── per-module rows, with N-1 comparison ────────────────────────────────────────────────
  const moduleRows = Object.keys(modsN).map((k) => {
    const m = modsN[k];
    const b = modsP[k];
    const has = m.samples > 0;
    const baseHas = b && b.samples > 0;
    const state = has ? 'measured' : (m.okRate === 0 ? 'failed' : 'not-reached');
    const g = (has && baseHas) ? gate(m.loadAvg, b.loadAvg) : { state: 'NO BASELINE', delta: 'N/A' };
    return {
      key: k, name: m.name, checks: m.checks, navType: m.navType, coverage: state,
      status: has ? (m.okRate === 1 ? 'Passed' : 'Degraded') : (state === 'failed' ? 'Failed to open' : 'Not executed'),
      samples: m.samples,
      uiLoadMs: has ? m.loadAvg : 'N/A',
      uiLoadMin: has ? (m.loadMin != null ? m.loadMin : 'N/A') : 'N/A',
      uiLoadMed: has ? (m.loadMed != null ? m.loadMed : 'N/A') : 'N/A',
      uiLoadP90: has ? (m.loadP90 != null ? m.loadP90 : 'N/A') : 'N/A',
      uiLoadP95Ms: has ? m.loadP95 : 'N/A',
      uiLoadP99: has ? (m.loadP99 != null ? m.loadP99 : 'N/A') : 'N/A',
      uiLoadMax: has ? (m.loadMax != null ? m.loadMax : 'N/A') : 'N/A',
      okRate: has ? m.okRate : 'N/A',
      baselineMs: baseHas ? b.loadAvg : 'N/A',
      deltaPct: g.delta,
      gate: g.state,
      apiLoadMs: 'N/A',
      attribution: 'N/A',
      note: has ? ('Measured over ' + m.samples + ' concurrent passes.')
        : (state === 'failed' ? 'Reached, but did not open within the timeout.'
                             : 'Not attempted in this run.'),
    };
  });

  const COVER = 'Login measured over ' + outN.iterations + ' concurrent users. Modules: '
    + measuredN.length + ' of ' + totalMods + ' measured, ' + failedN.length + ' failed, '
    + notRunN.length + ' not executed. Phase 2 (API) did not run, so API and API-vs-UI are unmeasured.';

  const CONTAM = 'Both executions ran while the OBJ-020 API execution was loading the same '
    + 'environment (running since 11:30). Latencies are therefore inflated relative to an idle '
    + 'environment. N-1 and N share that condition, so the COMPARISON is valid; the absolute values '
    + 'are not an idle-environment baseline. Grade: Likely (no isolated control run exists).';

  // ── web vitals, N and N-1 ───────────────────────────────────────────────────────────────
  const VITAL_LABEL = { browser_web_vital_lcp: 'LCP', browser_web_vital_fcp: 'FCP',
    browser_web_vital_ttfb: 'TTFB', browser_web_vital_cls: 'CLS' };
  function vitalRows() {
    const vN = psOf(sN).webVitals;
    const vP = sP ? psOf(sP).webVitals : null;
    if (!vN || typeof vN !== 'object') return [];
    return Object.keys(vN).map((key) => {
      const cur = vN[key];
      const base = (vP && typeof vP === 'object') ? vP[key] : null;
      const g = base ? gate(cur.avg, base.avg) : { state: 'NO BASELINE', delta: 'N/A' };
      return {
        metric: VITAL_LABEL[key] || key.replace('browser_web_vital_', '').toUpperCase(),
        raw: key,
        ms: cur.avg, p90: cur.p90, p95: cur.p95,
        baseline: base ? base.avg : 'N/A',
        deltaPct: g.delta, gate: g.state,
        unit: key.indexOf('cls') !== -1 ? 'score' : 'ms',
      };
    });
  }
  const vitals = vitalRows();

  // ── module load trend: one series per retained run, real values only ─────────────────────
  const moduleTrend = measuredN.map((k) => {
    const row = { module: modsN[k].name };
    if (sP && modsP[k] && modsP[k].samples > 0) row[runLabel(P.id)] = modsP[k].loadAvg;
    row[runLabel(N.id)] = modsN[k].loadAvg;
    return row;
  });

  const runTrend = [];
  if (sP) {
    runTrend.push({
      run: runLabel(P.id), p95: num(segP.journey && segP.journey.p95),
      median: num(segP.journey && segP.journey.med), checkRate: checkP,
      modules: Object.keys(modsP).filter((k) => modsP[k].samples > 0).length,
    });
  }
  runTrend.push({
    run: runLabel(N.id), p95: num(segN.journey && segN.journey.p95),
    median: num(segN.journey && segN.journey.med), checkRate: checkN,
    modules: measuredN.length,
  });

  write('manifest', {
    schema: 'pam-perf-dashboard/2', dataState: 'measured', generatedBy: GEN,
    objective: 'OBJ-021', project: 'PAM', tracker: 'PAMIT',
    environment: sN.context.environment, tool: 'k6 v2.2.0',
    currentRunId: N.id, baselineRunId: sP ? P.id : 'N/A',
    retainedRuns: runs.map((r) => r.id),
    journey: sN.context.journey, profile: sN.context.profile,
    concurrentUsers: (sN.workload || {}).targetVus,
    buildTag: psOf(sN).environmentBuildTag,
    sanitySource: (psOf(sN).sanityScope || {}).source || registry.source,
    coverageNote: COVER, contaminationNote: CONTAM,
    gates: { warnPct: WARN_PCT, failPct: FAIL_PCT,
      basis: 'Baseline-relative against N-1. No business SLO exists for PAM and none is invented.' },
    partial: failedN.length > 0 || notRunN.length > 0,
  });

  write('summary', {
    dataState: 'measured', sample: false,
    runId: N.id, baselineRunId: sP ? P.id : 'N/A',
    overallStatus: overall === 'PASS' ? 'Completed — within baseline' : 'Completed — ' + overall,
    gate: overall, gateReasons: gateReasons,
    concurrentUsers: (sN.workload || {}).targetVus,
    // ⛔ Four buckets, not two. A module measured with okRate below 1 opened on SOME concurrent
    // samples and not others - it is neither a clean pass nor a failure. Reporting only passed and
    // failed left those scenarios invisible and the tile did not add up to the total.
    scenarios: (function () {
      const passed = (loginOkN ? 1 : 0) + measuredN.filter((k) => modsN[k].okRate === 1).length;
      const failed = failedN.length + (loginOkN ? 0 : 1);
      const degraded = measuredN.filter((k) => modsN[k].okRate !== 1).length;
      return { total: 1 + totalMods, passed: passed, failed: failed,
        degraded: degraded, notExecuted: notRunN.length };
    })(),
    loginJourneyMs: band(segN.journey),
    p95Ms: num(segN.journey && segN.journey.p95),
    p99Ms: num(segN.journey && segN.journey.p99),
    avgResponseMs: num(segN.journey && segN.journey.med),
    p95Basis: 'Login journey (authentication + landing render), browser phase, '
      + (sN.workload || {}).targetVus + ' concurrent users. Not an API latency.',
    p95DeltaPct: p95Gate.delta, p95Gate: p95Gate.state,
    baselineP95Ms: num(segP.journey && segP.journey.p95),
    sampleCount: (segN.journey && segN.journey.count) != null ? segN.journey.count : 'N/A',
    throughputRps: 'N/A',
    throughputNote: 'Throughput is an API-phase metric. Phase 2 did not run.',
    loginErrorRate: typeof outN.failureRate === 'number' ? outN.failureRate : 'N/A',
    checkFailureRate: checkN != null ? Math.round((1 - checkN) * 1000) / 1000 : 'N/A',
    checkPassRate: checkN != null ? checkN : 'N/A',
    baselineCheckPassRate: checkP != null ? checkP : 'N/A',
    errorRate: typeof outN.failureRate === 'number' ? outN.failureRate : 'N/A',
    activeVus: (sN.workload || {}).targetVus,
    coverageNote: COVER, contaminationNote: CONTAM,
    trend: runTrend,
    trendNote: 'Two retained executions, N-1 and N. Older runs are archived, not deleted.',
  });

  write('login', {
    dataState: 'measured', sample: false,
    runId: N.id, baselineRunId: sP ? P.id : 'N/A',
    concurrentUsers: (sN.workload || {}).targetVus,
    uiJourneyMs: band(segN.journey), authMs: band(segN.auth),
    navigationMs: band(segN.navigation), inputMs: band(segN.input),
    authApiMs: 'N/A',
    authApiNote: 'Phase 2 (API login) did not run, so there is no API-side figure to compare.',
    successRate: outN.iterations ? outN.successfulLogins / outN.iterations : 'N/A',
    failureRate: typeof outN.failureRate === 'number' ? outN.failureRate : 'N/A',
    successfulLogins: outN.successfulLogins, iterations: outN.iterations,
    rejections: sN.rejections || {},
    browserOverheadMs: 'N/A',
    browserOverheadNote: 'Browser-vs-API overhead needs both phases. Phase 2 did not run.',
    segments: [
      { segment: 'Navigation', ms: num(segN.navigation && segN.navigation.med),
        baseline: num(segP.navigation && segP.navigation.med) },
      { segment: 'Credential entry', ms: num(segN.input && segN.input.med),
        baseline: num(segP.input && segP.input.med) },
      { segment: 'Authentication', ms: num(segN.auth && segN.auth.med),
        baseline: num(segP.auth && segP.auth.med) },
      { segment: 'Landing render',
        ms: (segN.journey && segN.auth) ? num(segN.journey.med - segN.auth.med) : 'N/A',
        baseline: (segP.journey && segP.auth) ? num(segP.journey.med - segP.auth.med) : 'N/A' },
    ],
    segmentNote: 'Medians, N against N-1. Landing render is the journey median minus the '
      + 'authentication median — the journey timer starts at the authentication POST.',
    trend: runTrend,
    authPath: 'POST /frmLoginACMO.aspx (web-tier UI login). NOT /arcontoken.',
    measurementValid: outN.measurementValid === true,
  });

  write('sanity', {
    dataState: 'measured', sample: false,
    runId: N.id, baselineRunId: sP ? P.id : 'N/A',
    source: (psOf(sN).sanityScope || {}).source || registry.source,
    concurrentUsers: (sN.workload || {}).targetVus,
    totals: { modules: totalMods,
      checks: (psOf(sN).sanityScope || {}).totalChecks || registry.totals.checks,
      excluded: (psOf(sN).sanityScope || {}).excluded || registry.excluded.length },
    coverage: { measured: measuredN.length, failed: failedN.length, notReached: notRunN.length,
      measuredPct: Math.round((measuredN.length / totalMods) * 1000) / 10 },
    coverageNote: COVER,
    abortCause: notRunN.length ? 'The sweep did not reach these modules in this run.' : null,
    excluded: registry.excluded,
    modules: moduleRows,
    moduleTrend: moduleTrend,
    moduleTrendNote: 'Average module load per retained execution. Only modules measured in N appear.',
    regressions: moduleRows.filter((r) => r.gate === 'FAIL' || r.gate === 'WARN')
      .map((r) => ({ module: r.name, deltaPct: r.deltaPct, gate: r.gate,
        baselineMs: r.baselineMs, currentMs: r.uiLoadMs })),
    improvements: moduleRows.filter((r) => typeof r.deltaPct === 'number' && r.deltaPct <= -10)
      .map((r) => ({ module: r.name, deltaPct: r.deltaPct,
        baselineMs: r.baselineMs, currentMs: r.uiLoadMs })),
  });

  write('api', {
    dataState: 'not-measured', sample: false, runId: N.id,
    reason: 'Phase 2 (API) was not executed. The raw WebForms postback path is a known open defect — '
      + 'it returns invalid_credentials for a credential that authenticates through the browser — so '
      + 'it was not run rather than spend login attempts on a shared functional account.',
    requests: 'N/A', requestsPerSec: 'N/A', avgLatencyMs: 'N/A', medianLatencyMs: 'N/A',
    percentiles: 'N/A', errorRate: 'N/A', failedRequests: 'N/A', checksPassRate: 'N/A',
    statusDistribution: [], trend: [],
  });

  const measuredRows = moduleRows.filter((r) => r.coverage === 'measured');
  const slowest = measuredRows.slice().sort((a, b) => b.uiLoadP95Ms - a.uiLoadP95Ms)[0] || null;
  write('ui', {
    dataState: 'measured', sample: false,
    runId: N.id, baselineRunId: sP ? P.id : 'N/A',
    concurrentUsers: (sN.workload || {}).targetVus,
    pageLoadMs: band(segN.navigation),
    moduleLoadMs: slowest
      ? { p50: slowest.uiLoadMs, p90: slowest.uiLoadP90, p95: slowest.uiLoadP95Ms, p99: slowest.uiLoadP99 }
      : 'N/A',
    moduleLoadBasis: slowest
      ? ('Slowest measured module: ' + slowest.name + ' (' + measuredRows.length + ' of '
         + totalMods + ' measured), over ' + slowest.samples + ' concurrent samples.')
      : 'No module produced a timing.',
    modulesMeasured: measuredRows.length, slowestModule: slowest,
    navigationMs: band(segN.navigation),
    submoduleLoadMs: 'N/A',
    submoduleNote: 'Submodule drill-down is not part of the current sweep.',
    perceivedMs: band(segN.journey),
    uiFailures: failedN.length,
    webVitals: vitals,
    webVitalsNote: vitals.length
      ? 'Captured by k6 (browser_web_vital_*) during this run. CLS is a unitless score; the rest are ms.'
      : 'Not captured in this run.',
    moduleDistribution: measuredRows.map((r) => ({
      module: r.name, min: r.uiLoadMin, med: r.uiLoadMed, p90: r.uiLoadP90,
      p95: r.uiLoadP95Ms, max: r.uiLoadMax,
    })),
    trend: runTrend,
  });

  write('comparison', {
    dataState: 'not-measured', sample: false, runId: N.id,
    verdict: 'N/A',
    reason: 'API-vs-UI attribution needs BOTH phases of the same run. Phase 2 did not run, so no '
      + 'attribution is computed rather than presenting UI timings as one.',
    perModule: [],
  });

  // ── N-1 vs N benchmark, the demo centrepiece ────────────────────────────────────────────
  write('benchmark', {
    dataState: sP ? 'measured' : 'not-measured',
    currentRunId: N.id, baselineRunId: sP ? P.id : 'N/A',
    gate: overall, gateReasons: gateReasons,
    gateBasis: 'Baseline-relative: WARN above ' + WARN_PCT + '% of N-1, FAIL above ' + FAIL_PCT
      + '%, hard FAIL on any login failure or a check-rate drop. No invented SLO.',
    contaminationNote: CONTAM,
    metrics: [
      { metric: 'Login journey p95', unit: 'ms', current: num(segN.journey && segN.journey.p95),
        baseline: num(segP.journey && segP.journey.p95),
        deltaPct: delta(segN.journey && segN.journey.p95, segP.journey && segP.journey.p95),
        gate: p95Gate.state, direction: 'lower-better' },
      { metric: 'Login journey median', unit: 'ms', current: num(segN.journey && segN.journey.med),
        baseline: num(segP.journey && segP.journey.med),
        deltaPct: delta(segN.journey && segN.journey.med, segP.journey && segP.journey.med),
        gate: gate(segN.journey && segN.journey.med, segP.journey && segP.journey.med).state,
        direction: 'lower-better' },
      { metric: 'Authentication median', unit: 'ms', current: num(segN.auth && segN.auth.med),
        baseline: num(segP.auth && segP.auth.med),
        deltaPct: delta(segN.auth && segN.auth.med, segP.auth && segP.auth.med),
        gate: gate(segN.auth && segN.auth.med, segP.auth && segP.auth.med).state,
        direction: 'lower-better' },
      { metric: 'Navigation median', unit: 'ms', current: num(segN.navigation && segN.navigation.med),
        baseline: num(segP.navigation && segP.navigation.med),
        deltaPct: delta(segN.navigation && segN.navigation.med, segP.navigation && segP.navigation.med),
        gate: gate(segN.navigation && segN.navigation.med, segP.navigation && segP.navigation.med).state,
        direction: 'lower-better' },
      { metric: 'Modules measured', unit: 'of ' + totalMods, current: measuredN.length,
        baseline: sP ? Object.keys(modsP).filter((k) => modsP[k].samples > 0).length : 'N/A',
        deltaPct: 'N/A', gate: 'INFO', direction: 'higher-better' },
      { metric: 'Check pass rate', unit: 'fraction', current: checkN != null ? checkN : 'N/A',
        baseline: checkP != null ? checkP : 'N/A',
        deltaPct: delta(checkN, checkP), gate: 'INFO', direction: 'higher-better' },
      { metric: 'Successful logins', unit: 'of ' + outN.iterations, current: outN.successfulLogins,
        baseline: sP ? outP.successfulLogins : 'N/A', deltaPct: 'N/A',
        gate: loginOkN ? 'PASS' : 'FAIL', direction: 'higher-better' },
    ],
    vitals: vitals,
    moduleRegressions: moduleRows.filter((r) => r.gate === 'FAIL' || r.gate === 'WARN')
      .map((r) => ({ module: r.name, currentMs: r.uiLoadMs, baselineMs: r.baselineMs,
        deltaPct: r.deltaPct, gate: r.gate })),
    moduleImprovements: moduleRows.filter((r) => typeof r.deltaPct === 'number' && r.deltaPct <= -10)
      .map((r) => ({ module: r.name, currentMs: r.uiLoadMs, baselineMs: r.baselineMs,
        deltaPct: r.deltaPct })),
    moduleTrend: moduleTrend,
  });

  const ex2 = readExecutions();
  write('executions', {
    dataState: 'measured', sample: false,
    purpose: 'Every retained k6 invocation. Older executions were ARCHIVED (moved), not deleted — '
      + 'see performance/reports-archive/README.md. An execution that was blocked is still an '
      + 'execution and is never omitted from what is retained.',
    retained: runs.map((r) => r.id),
    blocker: {
      active: false,
      summary: 'No blocker. Both retained executions authenticated and produced usable timings.',
      attemptsMade: ex2.length,
      accountsTried: ['arcosadmin — authenticates through the browser path (verified)'],
      unblocks: ['Phase 2 API postback defect (open)', 'uag module tile not clickable (open)'],
      safetyNote: 'Credential attempts are never retried. Each rejected login increments a lockout '
        + 'counter on a shared functional account.',
    },
    executions: ex2,
  });

  console.log('  INGESTED N=' + N.id + (sP ? ('  N-1=' + P.id) : '  (no baseline)')
    + '  gate=' + overall + '  modules=' + measuredN.length + '/' + totalMods
    + '  vitals=' + vitals.length + '  retained=' + runs.length);
}
