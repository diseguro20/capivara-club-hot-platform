const CACHE_NAME = 'capivara-laravel-v12';
const ASSETS = ['/manifest.json','/manifest-admin.json','/icons/icon-192.png','/icons/icon-512.png'];
self.addEventListener('install', e => e.waitUntil(caches.open(CACHE_NAME).then(c => c.addAll(ASSETS)).then(() => self.skipWaiting())));
self.addEventListener('activate', e => e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))).then(() => self.clients.claim())));
self.addEventListener('fetch', e => {
 const u = new URL(e.request.url);
 if (e.request.method !== 'GET' || u.origin !== location.origin || !ASSETS.includes(u.pathname)) return;
 e.respondWith(fetch(e.request).catch(() => caches.match(e.request)));
});
self.addEventListener('push', event => {
  let payload = {};
  try { payload = event.data ? event.data.json() : {}; } catch { payload = {body: event.data?.text() || ''}; }
  const notification = payload.notification || payload;
  const requestedUrl = notification.navigate || payload.url || '/admin';
  let target = new URL('/admin', self.location.origin);
  try {
    const candidate = new URL(requestedUrl, self.location.origin);
    if (candidate.origin === self.location.origin && candidate.pathname === '/admin') target = candidate;
  } catch {}
  const data = {...(payload.data || {}), ...(notification.data || {}), url: target.href};
  event.waitUntil(self.registration.showNotification(notification.title || payload.title || 'CAPIVARA CLUB HOT', {
    body: notification.body || payload.body || 'Você tem uma atualização no painel.',
    lang: notification.lang || 'pt-BR',
    dir: notification.dir || 'ltr',
    icon: notification.icon || payload.icon || '/icons/icon-192.png',
    badge: notification.badge || payload.badge || '/icons/icon-192.png',
    tag: notification.tag || payload.tag || `capivara-${Date.now()}`,
    renotify: notification.renotify ?? false,
    silent: notification.silent ?? false,
    data,
  }));
});
self.addEventListener('notificationclick', event => {
  event.notification.close();
  const target = new URL(event.notification.data?.url || '/admin', self.location.origin);
  const destination = target.origin === self.location.origin && target.pathname === '/admin' ? target.href : new URL('/admin', self.location.origin).href;
  event.waitUntil(self.clients.matchAll({type: 'window', includeUncontrolled: true}).then(async clients => {
    for (const client of clients) {
      if (new URL(client.url).origin !== self.location.origin) continue;
      const focused = client.navigate ? await client.navigate(destination) : client;
      return (focused || client).focus();
    }
    return self.clients.openWindow(destination);
  }));
});
