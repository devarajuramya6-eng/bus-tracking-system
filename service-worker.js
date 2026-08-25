/**
 * CityBus Enterprise Platform - Service Worker
 * File: service-worker.js
 * 
 * Provides offline caching, network-first API fetching, and background sync.
 */

const CACHE_NAME = 'citybus-v2.0.0';
const STATIC_ASSETS = [
  './',
  './index.html',
  './passenger-map.html',
  './journey-planner.html',
  './buses.html',
  './bus-details.html',
  './routes.html',
  './stops.html',
  './tickets.html',
  './my-tickets.html',
  './driver.html',
  './conductor.html',
  './dispatcher.html',
  './admin.html',
  './offline.html',
  './css/style.css',
  './css/tokens.css',
  './css/themes_dark.css',
  './css/components.css',
  './css/map_components.css',
  './css/animations.css',
  './css/responsive.css',
  './js/data.js',
  './js/core/theme.js',
  './js/core/api.js',
  './js/core/auth.js',
  './js/core/store.js',
  './js/core/notifications.js',
  './js/core/pwa.js',
  './js/components/toast.js',
  './js/components/modal.js',
  './js/components/command_palette.js',
  './js/simulator.js'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(STATIC_ASSETS).catch(err => {
        console.warn('[CityBus SW] Some static assets failed to cache:', err);
      });
    })
  );
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
    })
  );
  self.clients.claim();
});

self.addEventListener('fetch', (event) => {
  const url = new URL(event.request.url);

  // For API endpoints: Network First with graceful error
  if (url.pathname.startsWith('/api/')) {
    event.respondWith(
      fetch(event.request).catch(() => {
        return new Response(JSON.stringify({ offline: true, message: 'Device currently offline' }), {
          headers: { 'Content-Type': 'application/json' }
        });
      })
    );
    return;
  }

  // For Static Assets & Navigation: Cache First with Network Fallback
  event.respondWith(
    caches.match(event.request).then((cached) => {
      return (
        cached ||
        fetch(event.request).catch(() => {
          if (event.request.mode === 'navigate') {
            return caches.match('./offline.html');
          }
        })
      );
    })
  );
});
