# Games by Zaib

Home / launcher page for Jahan Zaib's browser games — live at **https://zaibgames.com/**

| Game | Genre | Link |
|---|---|---|
| Moto Mayhem | Motorbike combat racer | https://zaibgames.com/moto-mayhem/ |
| Sky Glide | Paper plane flying | https://zaibgames.com/sky-glide/ |
| Horde Breaker | Zombie survival shooter | https://zaibgames.com/horde-breaker/ |
| Goal Frenzy | Arcade football | https://zaibgames.com/goal-frenzy/ |
| Shuttle Smash | Badminton (1P / 2P) | https://zaibgames.com/shuttle-smash/ |
| Kedimz Adventure | Platformer | https://zaibgames.com/kedimz-adventure/ |

Each game lives in its own repo (project site); this repo is only the root user site.

## Adding a game

1. Add a thumbnail to `img/` (600×375 webp, ~10–30 KB).
2. Edit the `GAMES` array near the bottom of `index.template.html`:
   ```js
   { name: "New Game", desc: "One-line pitch.", genre: "Arcade",
     url: "https://zaibgames.com/new-game/", img: "img/new-game.webp", color: "#f59e0b" },
   ```
   Leave `url: null` to show a "Coming soon" card.
3. Run `./build.sh` (inlines the display font → `index.html`), commit and push.

## Files

- `index.html` – the built, fully self-contained page (no external requests besides local images)
- `index.template.html` – source (same as index.html, with a `__FONT__` placeholder)
- `fonts/lilita-subset.woff` – subset of Lilita One (SIL OFL) inlined by `build.sh`
- `img/` – game thumbnails, `og.jpg` (1200×630 share preview), icons
- `#ad-slot` – empty ad banner placeholder (no ads)
- `.nojekyll` – serve files as-is

## Info pages, sitemap, robots

`tools/pages.py` (run by `./build.sh`) generates `/about/`, `/contact/`, `/privacy/`, `/terms/`,
`/games/` and one guide page per game at `/games/<slug>/` (description, how to play, controls, features),
plus `sitemap.xml` and `robots.txt`. To add a guide for a new game, add an entry to `GAME_INFO` in
`tools/pages.py`; it also appears in the hub's "About the games" section after you copy the block
pattern in `index.template.html`. Game URLs in the `GAMES` array are added to the sitemap automatically.
`ads.txt` (AdSense) and the `google-adsense-account` verification meta tag are present; no ad units or auto-ads script yet. Keep the `CNAME` and `ads.txt` files.
