// Minimal service worker — just enables standalone mode
self.addEventListener('install', function(e) {
    self.skipWaiting()
})

self.addEventListener('activate', function(e) {
    self.clients.claim()
})

self.addEventListener('fetch', function(e) {
    // pass through all requests — no caching
    e.respondWith(fetch(e.request))
})