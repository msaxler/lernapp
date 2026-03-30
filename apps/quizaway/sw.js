// QuizAway Service Worker — AP11 PWA Shell
// Cache-Strategie: Cache-First für App-Shell, Network-First für geo.sqlite

const CACHE_NAME = 'quizaway-v5.0';
const CACHE_VERSION = '5.0.0';

// App-Shell: wird beim Install gecacht
const APP_SHELL = [
  '/apps/quizaway/quizaway_v5.html',
  '/apps/quizaway/manifest.json',
];

// ─── Install: App-Shell cachen ───────────────────────────────
self.addEventListener('install', event => {
  console.log('[SW] Install');
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      console.log('[SW] Caching App-Shell');
      return cache.addAll(APP_SHELL);
    }).then(() => self.skipWaiting())
  );
});

// ─── Activate: alte Caches aufräumen ─────────────────────────
self.addEventListener('activate', event => {
  console.log('[SW] Activate');
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(
        keys
          .filter(key => key !== CACHE_NAME)
          .map(key => {
            console.log('[SW] Alter Cache gelöscht:', key);
            return caches.delete(key);
          })
      )
    ).then(() => self.clients.claim())
  );
});

// ─── Fetch: Anfragen abfangen ────────────────────────────────
self.addEventListener('fetch', event => {
  const url = new URL(event.request.url);

  // Nur http/https cachen — chrome-extension etc. ignorieren
  if (!url.protocol.startsWith('http')) return;

  // API-Endpunkte: nie cachen — dynamische Daten, immer live vom Server
  if (url.pathname.startsWith('/warteraum/') ||
      url.pathname.startsWith('/lobby/') ||
      url.pathname.startsWith('/relay/') ||
      url.pathname.startsWith('/offer/') ||
      url.pathname.startsWith('/answer/') ||
      url.pathname === '/new' ||
      url.pathname === '/ping') {
    return;
  }

  // geo.sqlite: Network-First (groß, selten geändert → nach Netz auch cachen)
  if (url.pathname.endsWith('.sqlite') || url.pathname.endsWith('.db')) {
    event.respondWith(networkFirstWithCache(event.request));
    return;
  }

  // sql-wasm.wasm und CDN-Ressourcen: Cache-First
  if (url.hostname !== self.location.hostname) {
    event.respondWith(cacheFirstWithNetwork(event.request));
    return;
  }

  // App-Shell und lokale Dateien: Cache-First
  event.respondWith(cacheFirstWithNetwork(event.request));
});

// Cache-First: aus Cache, sonst Netz (und dann cachen)
async function cacheFirstWithNetwork(request) {
  const cached = await caches.match(request);
  if (cached) return cached;
  try {
    const response = await fetch(request);
    if (response.ok) {
      const cache = await caches.open(CACHE_NAME);
      cache.put(request, response.clone());
    }
    return response;
  } catch(e) {
    // Offline und nicht im Cache — Fehler zurückgeben
    return new Response('Offline — Ressource nicht verfügbar', { status: 503 });
  }
}

// Network-First: Netz zuerst, Fallback Cache
async function networkFirstWithCache(request) {
  try {
    const response = await fetch(request);
    if (response.ok) {
      const cache = await caches.open(CACHE_NAME);
      cache.put(request, response.clone());
    }
    return response;
  } catch(e) {
    const cached = await caches.match(request);
    if (cached) return cached;
    return new Response('Offline — Datei nicht verfügbar', { status: 503 });
  }
}
