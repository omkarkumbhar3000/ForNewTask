import { get } from '../api.js';
import { layout } from '../layout.js';
import { h, mount, param, fmtDate, empty } from '../ui.js';

const ctx = await layout({ area: 'parent', current: '/parent/' });
if (!ctx.blocked) await render();

async function render() {
  const childId = Number(param('id'));
  const certId = Number(param('cert'));
  try {
    const report = await get(`/parent/children/${childId}`);
    const cert = report.certificates.find((c) => c.id === certId);
    if (!cert) throw new Error('This certificate was not found.');
    mount('#main', h('div', { class: 'stack' },
      h('p', { class: 'no-print draft-note', text: 'Certificate wording is a draft awaiting review (INF-07).' }),
      h('div', { class: 'certificate' },
        h('img', { src: '/img/logo-192.png', alt: 'CleverCubs', width: 120, height: 120 }),
        h('h1', { text: 'Certificate of completion' }),
        h('p', { text: 'This is to celebrate that' }),
        h('p', { class: 'name', text: report.child.displayName }),
        h('p', { text: `completed every course of ${cert.programTitle} on CleverCubs.` }),
        h('p', { class: 'muted', text: `Issued ${fmtDate(cert.issuedAt)}. Certificate code ${cert.verificationCode}.` })),
      h('div', { class: 'row no-print' },
        h('button', { class: 'btn btn-primary', type: 'button', onclick: () => window.print(), text: 'Print' }),
        h('a', { class: 'btn btn-quiet', href: `/parent/summary.html?id=${childId}`, text: 'Back to the year summary' }))));
  } catch (e) {
    mount('#main', empty('🔍', e.message));
  }
}
