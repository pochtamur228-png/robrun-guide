/* ROB RUN Справочник — офлайн-режим.
 * Страница: сначала сеть (обновления приходят сразу), без сети — сохранённая копия.
 * Шрифты и telegram-web-app.js: из кэша сразу, в фоне обновляем.
 * Запросы к боту (POST) — только сеть. При изменении файлов из CORE поднимай V.
 */
const V = "rr-v18";
const APP = V + "-app", LIB = V + "-lib";
const CORE = ["./", "index.html", "assets/icon-32.png", "assets/icon-180.png", "assets/hero.jpg", "assets/bg.jpg"];

self.addEventListener("install", e => {
  e.waitUntil(caches.open(APP).then(c => c.addAll(CORE)).then(() => self.skipWaiting()));
});
self.addEventListener("activate", e => {
  e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => !k.startsWith(V)).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});

async function networkFirst(req) {
  const c = await caches.open(APP);
  try {
    const r = await fetch(req);
    if (r.ok) c.put(req, r.clone());
    return r;
  } catch (e) {
    const hit = await c.match(req, {ignoreSearch: req.mode === "navigate"});
    if (hit) return hit;
    if (req.mode === "navigate") { const idx = await c.match("index.html"); if (idx) return idx; }
    throw e;
  }
}
async function staleWhileRevalidate(req) {
  const c = await caches.open(LIB);
  const hit = await c.match(req);
  const net = fetch(req).then(r => { if (r.ok || r.type === "opaque") c.put(req, r.clone()); return r; }).catch(() => hit);
  return hit || net;
}

self.addEventListener("fetch", e => {
  const req = e.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);
  if (url.origin === location.origin) { e.respondWith(networkFirst(req)); return; }
  if (/fonts\.(googleapis|gstatic)\.com|telegram\.org/.test(url.host)) e.respondWith(staleWhileRevalidate(req));
});
