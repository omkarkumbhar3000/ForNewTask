// Measures what each key page downloads before any tap (requirement section 25), so performance claims are
// measured, not assumed. Registers a throw-away family, measures, then deletes it.
//   node measure.mjs            (the application must be running; CLEVERCUBS_URL overrides the address)
import { chromium } from '@playwright/test';

const base = process.env.CLEVERCUBS_URL || 'http://127.0.0.1:8080';
const password = 'Measure the pages 2026';
const browser = await chromium.launch({ channel: 'chrome' });
const context = await browser.newContext({ viewport: { width: 1440, height: 900 } });
const page = await context.newPage();

async function weigh(path, label, settle = 1500) {
  const sizes = [];
  const onResponse = async (response) => {
    try {
      const body = await response.body();
      sizes.push({ url: response.url(), bytes: body.length, type: response.request().resourceType() });
    } catch { /* redirects and aborted media have no body */ }
  };
  page.on('response', onResponse);
  const started = Date.now();
  await page.goto(base + path, { waitUntil: 'load' });
  const loadMs = Date.now() - started;
  await page.waitForTimeout(settle);
  page.off('response', onResponse);
  const total = sizes.reduce((sum, s) => sum + s.bytes, 0);
  const media = sizes.filter((s) => s.url.includes('/media/')).reduce((sum, s) => sum + s.bytes, 0);
  console.log(`${label.padEnd(28)} ${(total / 1024).toFixed(0).padStart(7)} KB   requests ${String(sizes.length).padStart(3)}   media ${(media / 1024).toFixed(0).padStart(6)} KB   load ${loadMs} ms`);
}

const api = async (method, path, body) => page.evaluate(async ([m, p, b]) => {
  const token = decodeURIComponent((document.cookie.match(/XSRF-TOKEN=([^;]+)/) || [])[1] || '');
  const r = await fetch('/api/v1' + p, { method: m, headers: { 'Content-Type': 'application/json', 'X-XSRF-TOKEN': token }, body: b ? JSON.stringify(b) : undefined });
  return { status: r.status, body: r.status === 204 ? null : await r.json().catch(() => null) };
}, [method, path, body]);

await weigh('/', 'Welcome (visitor)');
await weigh('/login', 'Sign in (visitor)');
const email = `measure-${Date.now()}@example.test`;
const dob = new Date(Date.now() - 5.2 * 365.25 * 864e5).toISOString().slice(0, 10);
const reg = await api('POST', '/auth/register', {
  parent: { fullName: 'Measure Parent', email, password, mobile: '', city: '' },
  child: { firstName: 'Ada', displayName: '', dateOfBirth: dob, username: null, avatarCode: 'owl' },
  acceptTerms: true, acceptPrivacy: true, consentChildData: true,
});
if (reg.status !== 201) throw new Error('registration failed: ' + JSON.stringify(reg.body));
await weigh('/parent/', 'Parent dashboard');
const children = await api('GET', '/parent/children');
await api('POST', '/session/child', { childId: children.body[0].id });
await weigh('/learn/', 'Child home (11 courses)');
const birds = await api('GET', '/learn/courses/birds');
await weigh(`/learn/lesson.html?id=${birds.body.lessons[0].id}`, 'Birds lesson 1 (was 56.85 MB)');
const rhymes = await api('GET', '/learn/courses/rhymes');
await weigh(`/learn/lesson.html?id=${rhymes.body.lessons[0].id}`, 'Rhyme video lesson');
await weigh('/learn/course.html?slug=alphabets', 'Course page');
await api('POST', '/session/parent', { password });
await api('DELETE', '/parent/account');
console.log('(throw-away account deleted)');
await browser.close();
