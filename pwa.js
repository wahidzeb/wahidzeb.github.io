/* Games by Zaib: service worker registration + "Install app" prompt.
   Android/Chrome/Edge: uses beforeinstallprompt to show an Install card.
   iPhone/iPad Safari: shows a "Tap Share, then Add to Home Screen" hint.
   Not nagging: appears after a delay on the first visit (sooner on later visits),
   "Not now" hides it for 30 days, never shown when already installed / standalone.
   A quiet "Install app" link is also added to the footer whenever install is possible. */
(() => {
  "use strict";
  // GA4 custom events (safe: never throws if gtag is missing or blocked)
  const zt = (n, p) => { try { window.gtag && gtag("event", n, p || {}); } catch (e) {} };
  const NOT_GAME = /^(about|contact|privacy|terms|games|img|fonts)$/;
  document.addEventListener("click", (e) => {
    const a = e.target && e.target.closest && e.target.closest("a[href]");
    if (!a) return;
    let u; try { u = new URL(a.href, location.href); } catch (err) { return; }
    if (u.protocol !== "http:" && u.protocol !== "https:") return;
    if (u.host !== location.host) { zt("outbound_click", { link_url: u.href, link_domain: u.host, outbound: true }); return; }
    const g = u.pathname.match(/^\/games\/([a-z0-9-]+)\/?$/), m = u.pathname.match(/^\/([a-z0-9-]+)\/?$/);
    const where = location.pathname === "/" ? "hub" : "guide";
    if (m && !NOT_GAME.test(m[1])) {
      const card = a.closest(".card");
      zt("select_content", { content_type: "game", content_id: m[1], game_id: m[1], link_location: where });
      zt("game_click", { game_id: m[1], link_location: where, link_type: card ? (a.classList.contains("play") ? "play_button" : "thumbnail") : "link" });
    } else if (g) zt("select_content", { content_type: "guide", content_id: g[1], game_id: g[1], link_location: where });
  }, true);
  if ("serviceWorker" in navigator) {
    addEventListener("load", () => { navigator.serviceWorker.register("/sw.js", { scope: "/" }).catch(() => {}); });
  }
  const ls = { get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
               set(k, v) { try { localStorage.setItem(k, v); } catch (e) {} } };
  const standalone = matchMedia("(display-mode: standalone)").matches || matchMedia("(display-mode: fullscreen)").matches ||
                     matchMedia("(display-mode: minimal-ui)").matches || navigator.standalone === true;
  if (standalone) {
    ls.set("zg_installed", "1");
    try { if (!sessionStorage.getItem("zg_launch")) { sessionStorage.setItem("zg_launch", "1"); zt("pwa_launch", { display_mode: navigator.standalone === true ? "ios_standalone" : "standalone" }); } } catch (e) {}
    return;
  }

  // count visits (one per browser session)
  let visits = +(ls.get("zg_visits") || 0);
  try { if (!sessionStorage.getItem("zg_seen")) { sessionStorage.setItem("zg_seen", "1"); ls.set("zg_visits", String(++visits)); } } catch (e) {}
  const DAY = 864e5;
  const snoozed = () => Date.now() < +(ls.get("zg_install_snooze") || 0);
  const delay = visits >= 2 ? 3000 : 25000;

  const ua = navigator.userAgent;
  const isIOS = /iPhone|iPad|iPod/.test(ua) || (navigator.platform === "MacIntel" && navigator.maxTouchPoints > 1);
  const inApp = /FBAN|FBAV|Instagram|Line\/|GSA\/|Snapchat|TikTok|; wv\)/.test(ua);
  const isIOSSafari = isIOS && /Safari\//.test(ua) && !/CriOS|FxiOS|EdgiOS|OPiOS|YaBrowser|DuckDuckGo/.test(ua) && !inApp;

  const css = `.zg-inst{position:fixed;z-index:9999;left:50%;bottom:max(14px,env(safe-area-inset-bottom));transform:translate(-50%,140%);
width:min(440px,calc(100% - 24px));display:flex;gap:12px;align-items:center;padding:12px 12px 12px 14px;border-radius:20px;color:#f4f1ff;
font:14px/1.35 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;background:rgba(24,14,58,.94);border:1px solid rgba(168,85,247,.45);
box-shadow:0 14px 40px rgba(0,0,0,.55),0 0 30px rgba(168,85,247,.25);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);
transition:transform .45s cubic-bezier(.2,.8,.2,1),opacity .3s;opacity:0}
.zg-inst.on{transform:translate(-50%,0);opacity:1}
.zg-inst img{width:48px;height:48px;border-radius:12px;flex:none}
.zg-inst .t{flex:1;min-width:0}.zg-inst b{display:block;font-size:15px}.zg-inst span{color:#c9c1ea}
.zg-inst svg{width:18px;height:18px;vertical-align:-3px;fill:none;stroke:#67e8f9;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}
.zg-inst .go{flex:none;border:0;border-radius:14px;padding:10px 16px;font:inherit;font-weight:800;color:#fff;cursor:pointer;
background:linear-gradient(180deg,#c084fc,#9333ea 55%,#7e22ce);box-shadow:0 4px 0 #4c1d95}
.zg-inst .go:active{transform:translateY(3px);box-shadow:0 1px 0 #4c1d95}
.zg-inst .x{flex:none;align-self:flex-start;width:30px;height:30px;margin:-4px -4px 0 0;border:0;border-radius:50%;background:rgba(255,255,255,.08);
color:#d9ccff;font:20px/1 system-ui,sans-serif;cursor:pointer}
.zg-inst button:focus-visible{outline:3px solid #22d3ee;outline-offset:2px}
@media (orientation:landscape) and (max-height:540px){.zg-inst{left:auto;right:max(10px,env(safe-area-inset-right));bottom:max(8px,env(safe-area-inset-bottom));transform:translateY(140%);
width:auto;max-width:min(360px,calc(100% - 20px));gap:8px;padding:6px 6px 6px 8px;border-radius:14px;font-size:13px}
.zg-inst.on{transform:none}.zg-inst img{width:30px;height:30px;border-radius:8px}.zg-inst b{font-size:13px;white-space:nowrap}.zg-inst.and .t>span{display:none}
.zg-inst .go{padding:6px 12px;border-radius:10px;box-shadow:0 3px 0 #4c1d95}.zg-inst .x{width:26px;height:26px;margin:0;align-self:center;font-size:18px}}
@media (prefers-reduced-motion:reduce){.zg-inst{transition:none}}`;
  const SHARE = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3v12M8 7l4-4 4 4"/><path d="M6 11H5v10h14V11h-1"/></svg>';
  const ADD = '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="4" y="4" width="16" height="16" rx="4"/><path d="M12 8v8M8 12h8"/></svg>';

  let deferred = null, card = null, link = null;

  function hide(snooze) {
    if (snooze) ls.set("zg_install_snooze", String(Date.now() + 30 * DAY));
    if (card) { const c = card; card = null; c.classList.remove("on"); setTimeout(() => c.remove(), 500); pad(); }
  }
  function show(trigger) {
    if (card || standalone) return;
    zt("pwa_prompt_shown", { platform: deferred ? "android" : "ios", trigger: trigger === "link" ? "footer_link" : "auto" });
    if (!document.getElementById("zg-inst-css")) {
      const s = document.createElement("style"); s.id = "zg-inst-css"; s.textContent = css; document.head.appendChild(s);
    }
    card = document.createElement("div");
    card.className = deferred ? "zg-inst and" : "zg-inst"; card.setAttribute("role", "dialog"); card.setAttribute("aria-label", "Install Zaib Games");
    card.innerHTML = deferred
      ? `<img src="/img/pwa/icon-192.png" alt=""><div class="t"><b>Get the Zaib Games app</b><span>One tap from your home screen. Games you've played work offline.</span></div><button class="go" type="button">Install</button><button class="x" type="button" aria-label="Not now">×</button>`
      : `<img src="/img/pwa/icon-192.png" alt=""><div class="t"><b>Add Zaib Games to your Home Screen</b><span>Tap ${SHARE} <b style="display:inline">Share</b>, then ${ADD} <b style="display:inline">Add to Home Screen</b>.</span></div><button class="x" type="button" aria-label="Close">×</button>`;
    document.body.appendChild(card);
    card.querySelector(".x").onclick = () => { zt("pwa_prompt_dismiss", { platform: deferred ? "android" : "ios" }); hide(true); };
    const go = card.querySelector(".go");
    if (go) go.onclick = async () => {
      const d = deferred; if (!d) return hide(false);
      deferred = null; hide(false);
      zt("pwa_install_click", { platform: "android" });
      d.prompt();
      try { const r = await d.userChoice; zt("pwa_install_choice", { outcome: (r && r.outcome) || "unknown" }); if (r && r.outcome === "dismissed") ls.set("zg_install_snooze", String(Date.now() + 30 * DAY)); } catch (e) {}
      updateLink();
    };
    requestAnimationFrame(() => requestAnimationFrame(() => { if (!card) return; card.classList.add("on"); pad(); }));
    addEventListener("resize", pad);
  }
  /* reserve room at the bottom of the page for the card, so it never sits on top of content you can't scroll past */
  let padded = null;
  function pad() {
    try {
      if (!card) { if (padded !== null) { document.body.style.paddingBottom = padded; padded = null; } return; }
      if (padded === null) padded = document.body.style.paddingBottom || "";
      const h = card.getBoundingClientRect().height + 20;
      document.body.style.paddingBottom = Math.max(h, parseFloat(padded) || 0) + "px";
    } catch (e) {}
  }
  function updateLink() {
    const nav = document.querySelector("footer nav");
    const can = !!deferred || isIOSSafari;
    if (!nav) return;
    if (can && !link) {
      link = document.createElement("a"); link.href = "#install"; link.textContent = "Install app";
      link.onclick = (e) => { e.preventDefault(); show("link"); };
      nav.appendChild(link);
    } else if (!can && link) { link.remove(); link = null; }
  }
  const autoShow = () => { if (!snoozed() && ls.get("zg_installed") !== "1") setTimeout(() => show("auto"), delay); };

  addEventListener("beforeinstallprompt", (e) => {
    e.preventDefault(); deferred = e;
    ls.set("zg_installed", "0");
    updateLink(); autoShow();
  });
  addEventListener("appinstalled", () => { zt("pwa_installed", { platform: isIOS ? "ios" : "android" }); ls.set("zg_installed", "1"); deferred = null; hide(false); updateLink(); });

  if (isIOSSafari) {
    const go = () => { updateLink(); autoShow(); };
    document.readyState === "loading" ? addEventListener("DOMContentLoaded", go) : go();
  }
})();
