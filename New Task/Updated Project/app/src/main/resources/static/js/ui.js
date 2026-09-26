// Small DOM helpers. Everything the server sends is written with textContent or attributes, never innerHTML,
// so a stored script is shown as text (SEC-E18). The CSP forbids inline styles, so dynamic values go through
// CSS custom properties set with style.setProperty.

export function h(tag, attrs = {}, ...children) {
  const el = document.createElement(tag);
  for (const [key, value] of Object.entries(attrs || {})) {
    if (value === undefined || value === null || value === false) continue;
    if (key === 'class') el.className = value;
    else if (key === 'text') el.textContent = value;
    else if (key.startsWith('on') && typeof value === 'function') el.addEventListener(key.slice(2).toLowerCase(), value);
    else if (key === 'vars') for (const [name, v] of Object.entries(value)) el.style.setProperty(name, v);
    else if (key === 'dataset') Object.assign(el.dataset, value);
    else if (value === true) el.setAttribute(key, '');
    else el.setAttribute(key, String(value));
  }
  append(el, children);
  return el;
}

function append(el, children) {
  for (const child of children.flat(Infinity)) {
    if (child === null || child === undefined || child === false) continue;
    el.append(child instanceof Node ? child : document.createTextNode(String(child)));
  }
}

export const $ = (selector, root = document) => root.querySelector(selector);
export const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];

export function mount(target, ...children) {
  const el = typeof target === 'string' ? $(target) : target;
  el.replaceChildren();
  append(el, children);
  return el;
}

export function param(name) {
  return new URLSearchParams(location.search).get(name);
}

export const ACCENTS = ['sun', 'sky', 'berry', 'lilac', 'leaf', 'honey'];
export const accentFor = (index) => 'accent-' + ACCENTS[index % ACCENTS.length];

/** The crayon progress bar, with an accessible progressbar role. */
export function crayon(value, label) {
  const v = Math.max(0, Math.min(100, Number(value) || 0));
  const bar = h('div', {
    class: 'crayon' + (v >= 100 ? ' is-done' : '') + (v === 0 ? ' is-empty' : ''),
    role: 'progressbar', 'aria-valuemin': 0, 'aria-valuemax': 100, 'aria-valuenow': v,
    'aria-label': label || 'Progress', vars: { '--value': v + '%' },
  }, h('i'));
  return bar;
}

export function ring(value, label) {
  const v = Math.max(0, Math.min(100, Number(value) || 0));
  return h('div', { class: 'ring', role: 'img', 'aria-label': (label || 'Progress') + ': ' + v + '%', vars: { '--value': v } },
    h('b', { text: v + '%' }));
}

/** Five stars for the youngest children, who get pictures instead of numbers (docs/04 section 6.3). */
export function stars(value) {
  const filled = Math.round((Math.max(0, Math.min(100, value)) / 100) * 5);
  const wrap = h('span', { class: 'stars', role: 'img', 'aria-label': filled + ' of 5 stars' });
  for (let i = 0; i < 5; i++) wrap.append(h('span', { class: i < filled ? '' : 'off', 'aria-hidden': 'true', text: '⭐' }));
  return wrap;
}

export function toast(message, kind = '') {
  let box = $('.toasts');
  if (!box) {
    box = h('div', { class: 'toasts', role: 'status', 'aria-live': 'polite' });
    document.body.append(box);
  }
  const item = h('div', { class: 'toast ' + kind, text: message });
  box.append(item);
  setTimeout(() => item.remove(), 4200);
}

/** One small celebration, never on page load, and skipped when reduced motion is preferred. */
export function celebrate(symbols = ['⭐', '🌟', '🎉', '✨', '💛']) {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const layer = h('div', { class: 'celebrate', 'aria-hidden': 'true' });
  for (let i = 0; i < 18; i++) {
    const angle = (Math.PI * 2 * i) / 18;
    const distance = 140 + Math.random() * 120;
    layer.append(h('span', {
      text: symbols[i % symbols.length],
      vars: {
        '--dx': Math.round(Math.cos(angle) * distance) + 'px',
        '--dy': Math.round(Math.sin(angle) * distance) + 'px',
        '--rot': Math.round(Math.random() * 360) + 'deg',
      },
    }));
  }
  document.body.append(layer);
  setTimeout(() => layer.remove(), 1300);
}

let readAloud = true;
export function setReadAloud(on) { readAloud = on !== false; }

/** The browser's own speech: no service, no network (docs/04 section 6.3). */
export function speak(text, force = false) {
  if ((!readAloud && !force) || !text || !('speechSynthesis' in window)) return;
  window.speechSynthesis.cancel();
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.rate = 0.9;
  utterance.pitch = 1.1;
  window.speechSynthesis.speak(utterance);
}

export function speakButton(textFn, label = 'Read to me') {
  return h('button', { class: 'speak', type: 'button', onclick: () => speak(typeof textFn === 'function' ? textFn() : textFn, true) },
    h('span', { 'aria-hidden': 'true', text: '🔊' }), label);
}

export function fmtDate(value) {
  if (!value) return '';
  let v = value;
  if (typeof v === 'string' && /T\d{2}:\d{2}/.test(v) && !/[zZ]|[+-]\d{2}:?\d{2}$/.test(v)) v += 'Z';
  const date = new Date(v);
  if (Number.isNaN(date.getTime())) return String(value);
  return date.toLocaleDateString(undefined, { day: 'numeric', month: 'short', year: 'numeric' });
}

export function fmtDateTime(value) {
  if (!value) return '';
  let v = value;
  if (typeof v === 'string' && !/[zZ]|[+-]\d{2}:?\d{2}$/.test(v)) v += 'Z';
  const date = new Date(v);
  return Number.isNaN(date.getTime()) ? String(value)
    : date.toLocaleString(undefined, { day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' });
}

/** Shows an ApiError on a form: field messages beside their inputs, the rest in the alert box. */
export function showErrors(form, error) {
  clearErrors(form);
  let placed = false;
  for (const f of error.fields || []) {
    const name = String(f.field).split('.').pop();
    const input = form.querySelector(`[name="${CSS.escape(f.field)}"], [name="${CSS.escape(name)}"], [name$=".${CSS.escape(name)}"]`);
    if (input) {
      const field = input.closest('.field') || input.parentElement;
      field.classList.add('invalid');
      input.setAttribute('aria-invalid', 'true');
      const note = h('p', { class: 'field-error', text: f.message === error.message ? f.message : capitalise(f.message) });
      field.append(note);
      if (!placed) input.focus();
      placed = true;
    }
  }
  const alert = form.querySelector('.form-alert');
  if (alert && (!placed || error.fields.length === 0)) {
    alert.textContent = error.message;
    alert.hidden = false;
    alert.focus?.();
  }
}

export function clearErrors(form) {
  form.querySelectorAll('.field-error').forEach((n) => n.remove());
  form.querySelectorAll('.invalid').forEach((n) => n.classList.remove('invalid'));
  form.querySelectorAll('[aria-invalid]').forEach((n) => n.removeAttribute('aria-invalid'));
  const alert = form.querySelector('.form-alert');
  if (alert) alert.hidden = true;
}

function capitalise(s) {
  const text = String(s || '');
  return text.charAt(0).toUpperCase() + text.slice(1) + (/[.!?]$/.test(text) ? '' : '.');
}

/** A native dialog; resolves with the button value, or null when dismissed. */
export function dialog({ title, body = [], actions = [], onOpen }) {
  return new Promise((resolve) => {
    let d;
    // Cancel is a plain button, so Enter in a field confirms instead of cancelling.
    const form = h('form', { method: 'dialog' },
      h('h2', { text: title }),
      ...[].concat(body),
      h('div', { class: 'dialog-actions' },
        actions.map((a) => a.value === 'cancel'
          ? h('button', { class: 'btn ' + (a.class || 'btn-quiet'), type: 'button', text: a.label, onclick: () => d.close('cancel') })
          : h('button', { class: 'btn ' + (a.class || 'btn-quiet'), value: a.value, type: 'submit', text: a.label }))));
    d = h('dialog', { 'aria-label': title }, form);
    document.body.append(d);
    d.addEventListener('close', () => {
      const value = d.returnValue && d.returnValue !== 'cancel' ? d.returnValue : null;
      resolve({ value, form });
      d.remove();
    });
    d.showModal();
    onOpen?.(form);
  });
}

export async function confirmDialog(title, message, okLabel, danger = false) {
  const { value } = await dialog({
    title,
    body: [h('p', { text: message })],
    actions: [{ label: 'Cancel', value: 'cancel' }, { label: okLabel, value: 'ok', class: danger ? 'btn-danger' : 'btn-primary' }],
  });
  return value === 'ok';
}

/** Asks for the grown-up's password; resolves with it, or null. */
export async function askPassword(title, message, okLabel = 'Continue') {
  const input = h('input', { type: 'password', name: 'password', autocomplete: 'current-password', required: true, id: 'dialog-password' });
  const { value, form } = await dialog({
    title,
    body: [h('p', { text: message }), h('div', { class: 'field' }, h('label', { for: 'dialog-password', text: 'Password' }), input)],
    actions: [{ label: 'Cancel', value: 'cancel' }, { label: okLabel, value: 'ok', class: 'btn-primary' }],
    onOpen: () => input.focus(),
  });
  return value === 'ok' ? form.querySelector('input').value : null;
}

export function empty(icon, text, ...extra) {
  return h('div', { class: 'empty' }, h('span', { class: 'icon', 'aria-hidden': 'true', text: icon }), h('p', { text }), ...extra);
}

export function download(filename, data) {
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = h('a', { href: url, download: filename });
  document.body.append(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}
