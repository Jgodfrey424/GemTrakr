const CACHE_NAME = "gemtrackr-cache-v1";
const urlsToCache = [
    "/",
    "/index",
    "/static/assets/css/black-dashboard.css?v=1.0.0",
    "/static/assets/js/core/jquery.min.js",
    "/static/assets/js/core/bootstrap.min.js",
    "/static/assets/js/core/popper.min.js",
    "/static/assets/js/plugins/chartjs.min.js",
    "/static/assets/fonts/nucleo.woff2",
    "/static/manifest.json"
];

self.addEventListener("install", function (event) {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => cache.addAll(urlsToCache))
    );
});

self.addEventListener("fetch", function (event) {
    event.respondWith(
        caches.match(event.request)
            .then(response => response || fetch(event.request))
    );
});
