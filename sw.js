/* Games by Zaib service worker (scope "/").
   - Navigations / HTML: network-first, cached copy used only when offline.
     Every page you open (the hub and each game's /<repo>/index.html) is cached,
     so a game played once keeps working offline, but fresh builds always win online.
   - Fonts and icons: cache-first.  Other same-origin files (thumbnails, pwa.js, manifest):
     stale-while-revalidate, so updated thumbnails show up on the next visit.
   - Cross-origin requests (Google Analytics, AdSense, etc.) are never touched.
   Bump VERSION to drop old caches. */
const VERSION = "zg-2026-10-15-1";
const STATIC = VERSION + "-static";   // precache + cache-first assets
const PAGES = VERSION + "-pages";     // HTML pages (hub, guides, games)
const RUNTIME = VERSION + "-runtime"; // other same-origin files
const PRECACHE = [
  "/", "/manifest.webmanifest", "/pwa.js", "/favicon.ico",
  "/img/apple-touch-icon.png", "/img/icon-512.png",
  "/img/pwa/icon-192.png", "/img/pwa/icon-512.png", "/img/pwa/maskable-192.png", "/img/pwa/maskable-512.png"
];
const MAX_PAGES = 60, MAX_RUNTIME = 150;

// fetch with a hard timeout so a stalled network can never hang install or a navigation
const timed = (p, ms) => Promise.race([p, new Promise((_, rej) => setTimeout(() => rej(new Error("timeout")), ms))]);

self.addEventListener("install", (event) => {
  // Small precache only (no thumbnails), each fetch capped at 8s; install never blocks on a stalled request.
  event.waitUntil((async () => {
    const c = await caches.open(STATIC);
    await Promise.all(PRECACHE.map(async (u) => {
      try { const r = await timed(fetch(u, { cache: "reload" }), 8000); if (r.ok) await c.put(u, r); } catch (e) {}
    }));
    const hub = await c.match("/"); if (hub) await (await caches.open(PAGES)).put("/", hub.clone());
  })());
  self.skipWaiting(); // not awaited
});

self.addEventListener("activate", (event) => {
  event.waitUntil((async () => {
    const keep = [STATIC, PAGES, RUNTIME];
    await Promise.all((await caches.keys()).filter((k) => k.startsWith("zg-") && !keep.includes(k)).map((k) => caches.delete(k)));
    if (self.registration.navigationPreload) { try { await self.registration.navigationPreload.enable(); } catch (e) {} }
    await self.clients.claim();
  })());
});

const pageKey = (url) => { const u = new URL(url); return u.origin + u.pathname; }; // ignore ?source=pwa etc.

async function trim(name, max) {
  const c = await caches.open(name), keys = await c.keys();
  for (let i = 0; i < keys.length - max; i++) await c.delete(keys[i]);
}

const NAV_TIMEOUT = 2500; // ms: after this, show the cached copy / shell while the network keeps going in the background

async function cachedPage(url) {
  const key = pageKey(url), path = new URL(url).pathname;
  return (await caches.match(key, { ignoreSearch: true })) ||
         (!key.endsWith("/") && (await caches.match(key + "/", { ignoreSearch: true }))) ||
         (path === "/" || path === "/index.html" ? await caches.match("/", { ignoreSearch: true }) : undefined);
}

function networkFirstPage(event) {
  const req = event.request;
  // network side: preload (if any) else fetch; successful pages refresh the cache in the background
  const net = (async () => {
    let res; try { res = await event.preloadResponse; } catch (e) {}
    if (!res) res = await fetch(req);
    if (res && res.ok && res.type === "basic" && !res.redirected) {
      const copy = res.clone();
      event.waitUntil(caches.open(PAGES).then((c) => c.put(pageKey(req.url), copy)).then(() => trim(PAGES, MAX_PAGES)).catch(() => {}));
    }
    return res;
  })();
  net.catch(() => {});
  return (async () => {
    try { const r = await timed(net, NAV_TIMEOUT); if (r) return r; } catch (e) {}
    const hit = await cachedPage(req.url).catch(() => undefined);
    if (hit) return hit;
    // nothing cached: give the network a bit longer, then the offline shell (never hang)
    try { const r = await timed(net, 8000); if (r) return r; } catch (e) {}
    return offlinePage();
  })();
}

async function offlinePage() {
  const names = [];
  try {
    for (const r of await (await caches.open(PAGES)).keys()) {
      const p = new URL(r.url).pathname, m = p.match(/^\/([a-z0-9-]+)\/(index\.html)?$/);
      if (m && !["games", "about", "contact", "privacy", "terms"].includes(m[1])) names.push(m[1]);
    }
  } catch (e) {}
  const nice = (s) => s.replace(/-/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
  const list = names.length ? `<p>Games saved on this device:</p><p>${names.map((n) => `<a href="/${n}/">${nice(n)}</a>`).join("")}</p>` : "";
  const html = `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#0b0820"><title>Offline | Games by Zaib</title><style>
body{margin:0;min-height:100vh;display:grid;place-items:center;text-align:center;font:16px/1.5 system-ui,sans-serif;color:#f4f1ff;
background:radial-gradient(120% 80% at 50% -10%,#24124d 0%,#0b0820 55%,#06040f 100%)}main{padding:24px;max-width:420px}
h1{font-size:30px;margin:12px 0 6px}p{color:#b7b0d8}a{display:inline-block;margin:4px;padding:10px 16px;border-radius:12px;color:#fff;text-decoration:none;
background:rgba(168,85,247,.25);border:1px solid rgba(168,85,247,.5)}button{margin-top:14px;font:inherit;font-weight:700;color:#fff;border:0;border-radius:14px;
padding:12px 22px;background:linear-gradient(180deg,#c084fc,#7e22ce);cursor:pointer}</style></head><body><main>
<img src="/img/pwa/icon-192.png" width="72" height="72" alt=""><h1>You're offline</h1><p>This page hasn't been saved yet. Connect to the internet and try again.</p>
${list}<button onclick="location.reload()">Try again</button></main></body></html>`;
  return new Response(html, { status: 200, headers: { "Content-Type": "text/html; charset=utf-8", "Cache-Control": "no-store" } });
}

async function cacheFirst(req) {
  const hit = await caches.match(req, { ignoreSearch: true });
  if (hit) return hit;
  const res = await timed(fetch(req), 15000);
  if (res.ok && res.type === "basic") { const copy = res.clone(); caches.open(STATIC).then((c) => c.put(req, copy)); }
  return res;
}

async function staleWhileRevalidate(event) {
  const req = event.request, c = await caches.open(RUNTIME);
  const hit = await c.match(req);
  const net = fetch(req).then((res) => {
    if (res.ok && res.type === "basic" && res.status === 200) {
      const copy = res.clone(); event.waitUntil(c.put(req, copy).then(() => trim(RUNTIME, MAX_RUNTIME)));
    }
    return res;
  });
  if (hit) { event.waitUntil(net.catch(() => {})); return hit; }
  return timed(net, 15000).catch(() => Response.error());
}

self.addEventListener("fetch", (event) => {
  const req = event.request;
  if (req.method !== "GET") return;                     // POSTs (analytics beacons etc.) untouched
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;      // GA / AdSense / any third party: browser handles it
  if (req.headers.has("range")) return;                 // media range requests
  if (url.pathname === "/sw.js") return;
  const accept = req.headers.get("accept") || "";
  if (req.mode === "navigate" || (req.destination === "document") || accept.includes("text/html")) {
    event.respondWith(networkFirstPage(event));
  } else if (/^\/(fonts|img\/pwa)\//.test(url.pathname) || ["/favicon.ico", "/img/icon-512.png", "/img/apple-touch-icon.png"].includes(url.pathname)) {
    event.respondWith(cacheFirst(req));
  } else {
    event.respondWith(staleWhileRevalidate(event));
  }
});
