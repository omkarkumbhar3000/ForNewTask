import { get } from '../api.js';
import { layout } from '../layout.js';
import { h, mount } from '../ui.js';

await layout({ area: 'public', current: '/contact' });

try {
  const contact = await get('/public/contact');
  // D80: one or more addresses (CC_CONTACT_EMAIL); older servers sent only "email".
  const emails = Array.isArray(contact.emails) ? contact.emails : (contact.email ? [contact.email] : []);
  if (contact.configured && emails.length) {
    const links = [];
    emails.forEach((email, i) => {
      if (i > 0) links.push(' · ');
      links.push(h('a', { href: 'mailto:' + email, text: email }));
    });
    mount('#contact-line', emails.length > 1 ? 'Email us: ' : 'Email: ', ...links);
    document.getElementById('contact-line').classList.remove('muted');
  } else {
    // INF-02: the owner has not supplied the address yet; nothing personal is invented.
    mount('#contact-line', 'The contact address is being set up. Until then, signed-in parents can use the Feedback page.');
  }
} catch {
  mount('#contact-line', 'The contact address could not be loaded. Please try again later.');
}
