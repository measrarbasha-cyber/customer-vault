// CustomerVault Resilient Service Worker v3
const CACHE_NAME = 'customervault-v3';

self.addEventListener('install', (event) => {
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME) {
            return caches.delete(key);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  // Only intercept GET requests
  if (event.request.method !== 'GET') return;

  const url = new URL(event.request.url);

  // Let all cross-origin requests (CDNs, fonts, Google scripts) pass through directly to browser network
  if (url.origin !== self.location.origin) {
    return;
  }

  // Never cache HTML page navigation, root, or API requests - always get fresh from network
  if (event.request.mode === 'navigate' || url.pathname === '/' || url.pathname === '/index.html' || url.pathname.startsWith('/api/')) {
    event.respondWith(
      fetch(event.request, { cache: 'no-store' }).catch(async () => {
        const cachedRoot = await caches.match('/');
        if (cachedRoot) return cachedRoot;
        return new Response('Network error - please refresh', { status: 503 });
      })
    );
    return;
  }

  // Handle same-origin static assets with Network-First, Cache-Fallback
  event.respondWith(
    fetch(event.request)
      .then((response) => {
        if (response && response.status === 200) {
          const responseClone = response.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(event.request, responseClone);
          });
        }
        return response;
      })
      .catch(async () => {
        const cached = await caches.match(event.request);
        if (cached) return cached;
        return new Response('Network error - please refresh', { status: 503 });
      })
  );
});
