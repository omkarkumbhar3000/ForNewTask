// The one way pages talk to the server: same-origin session cookie, the CSRF token in a header (DD-03),
// JSON in and out, and problem+json errors turned into ApiError. Pages never build URLs outside /api/v1.

export class ApiError extends Error {
  constructor(status, problem) {
    super(problem.detail || 'Something went wrong. Please try again.');
    this.status = status;
    this.code = problem.code || 'server-error';
    this.fields = Array.isArray(problem.fields) ? problem.fields : [];
  }
}

let reauthHandler = null;

/** Called when the server answers reauth-required; it asks for the password and resolves true to retry. */
export function onReauthRequired(handler) {
  reauthHandler = handler;
}

function csrfToken() {
  const match = document.cookie.match(/(?:^|;\s*)XSRF-TOKEN=([^;]+)/);
  return match ? decodeURIComponent(match[1]) : null;
}

async function ensureCsrf() {
  let token = csrfToken();
  if (!token) {
    await fetch('/api/v1/public/health', { credentials: 'same-origin' });
    token = csrfToken();
  }
  return token;
}

export async function api(path, { method = 'GET', body, retry = true } = {}) {
  const headers = { Accept: 'application/json' };
  if (body !== undefined) headers['Content-Type'] = 'application/json';
  if (method !== 'GET') {
    const token = await ensureCsrf();
    if (token) headers['X-XSRF-TOKEN'] = token;
  }
  let response;
  try {
    response = await fetch('/api/v1' + path, {
      method,
      headers,
      credentials: 'same-origin',
      body: body === undefined ? undefined : JSON.stringify(body),
    });
  } catch {
    throw new ApiError(0, { code: 'offline', detail: 'We could not reach CleverCubs. Check the connection and try again.' });
  }
  if (response.status === 204) return null;
  const type = response.headers.get('content-type') || '';
  const data = type.includes('json') ? await response.json().catch(() => null) : null;
  if (response.ok) return data;

  const problem = data || { code: 'server-error' };
  if (response.status === 401 && problem.code === 'unauthenticated') {
    const next = location.pathname + location.search;
    location.assign('/login?next=' + encodeURIComponent(next));
    throw new ApiError(401, problem);
  }
  if (problem.code === 'reauth-required' && retry && reauthHandler) {
    if (await reauthHandler()) return api(path, { method, body, retry: false });
  }
  if (problem.code === 'password-change-required') {
    const target = location.pathname.startsWith('/admin') ? '/admin/#account' : '/parent/account.html';
    if (location.pathname + location.hash !== target) location.assign(target);
  }
  throw new ApiError(response.status, problem);
}

export const get = (path) => api(path);
export const post = (path, body) => api(path, { method: 'POST', body: body ?? {} });
export const put = (path, body) => api(path, { method: 'PUT', body: body ?? {} });
export const patch = (path, body) => api(path, { method: 'PATCH', body: body ?? {} });
export const del = (path) => api(path, { method: 'DELETE' });

/** The signed-in account, or null for a visitor. Never redirects and never answers 401. */
export async function whoAmI() {
  const response = await fetch('/api/v1/public/session', { credentials: 'same-origin', headers: { Accept: 'application/json' } });
  if (!response.ok) return null;
  const session = await response.json();
  return session.signedIn ? session : null;
}

/** Where an account belongs after signing in. */
export function homeFor(me) {
  if (!me) return '/';
  if (me.mode === 'CHILD') return '/learn/';
  if (me.role === 'SUPER_ADMIN') return '/admin/';
  return '/parent/';
}
