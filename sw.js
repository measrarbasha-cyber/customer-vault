// CustomerVault Resilient Service Worker v2
const CACHE_NAME = 'customervault-v2';

self.addEventListener('install', (event) => {
  // Activate immediately without waiting
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

  // Handle same-origin requests with Network-First, Cache-Fallback
  event.respondWith(
    fetch(event.request)
      .then((response) => {
        // Cache successful GET responses for static files
        if (response && response.status === 200 && !url.pathname.startsWith('/api/')) {
          const responseClone = response.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(event.request, responseClone);
          });
        }
        return response;
      })
      .catch(async () => {
        // Fallback to cache if network fails
        const cached = await caches.match(event.request);
        if (cached) return cached;

        // If it's a page navigation request, fallback to cached root
        if (event.request.mode === 'navigate') {
          const cachedRoot = await caches.match('/');
          if (cachedRoot) return cachedRoot;
        }

        // Return a valid offline JSON if API was requested
        if (url.pathname.startsWith('/api/')) {
          return new Response(JSON.stringify([]), {
            headers: { 'Content-Type': 'application/json' }
          });
        }

        return new Response('Network error - please refresh', { status: 503 });
      })
  );
});
