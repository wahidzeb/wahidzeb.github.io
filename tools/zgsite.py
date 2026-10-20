"""Guides (/guides/<slug>/) and Tips & News (/news/<slug>/) for zaibgames.com.
Content lives in content/guides/<slug>.md and content/news/<slug>.md:
a few 'key: value' lines, a line with ---, then the text (see /workspace/adsense/POSTING.md).
Text markup: '## Heading', '### Sub heading', '- list item', '1. numbered item', **bold**,
[words](/link/), [words](play:slug) = play link, [words](guide:slug) = guide link,
and on their own line: {{shots}} (screenshot gallery), {{play}} (big Play button),
{{card slug}} (game card with Play and Guide buttons)."""
import html, json, os, re, datetime
e = html.escape

def parse(path):
    raw = open(path, encoding="utf-8").read()
    head, _, body = raw.partition("\n---\n")
    meta = {}
    for line in head.splitlines():
        if ":" in line and not line.startswith("#"):
            k, v = line.split(":", 1); meta[k.strip()] = v.strip()
    meta["body"] = body.strip()
    meta["slug"] = os.path.splitext(os.path.basename(path))[0]
    return meta

def words(text):
    t = re.sub(r"\{\{[^}]*\}\}", " ", text); t = re.sub(r"\]\([^)]*\)", "]", t)
    return len(re.findall(r"[A-Za-z0-9'’\-]+", t))

def inline(s, ctx):
    s = e(s, quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    def link(m):
        t, u = m.group(1), m.group(2)
        if u.startswith("play:"): u = f"/{u[5:]}/"
        elif u.startswith("guide:"): u = f"/guides/{u[6:]}/"
        elif u.startswith("news:"): u = f"/news/{u[5:]}/"
        ext = ' rel="noopener"' if u.startswith("http") else ""
        return f'<a href="{e(u)}"{ext}>{t}</a>'
    return re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", link, s)

def slugify(t): return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")

def md(text, ctx):
    out = []
    for block in re.split(r"\n\s*\n", text.strip()):
        lines = [l.rstrip() for l in block.strip().splitlines()]
        first = lines[0]
        if first == "{{shots}}": out.append(ctx["shots"]()); continue
        if first == "{{play}}": out.append(ctx["play"]()); continue
        m = re.match(r"\{\{card ([a-z0-9-]+)\}\}$", first)
        if m:
            out.append('<div class="gcards">' + "".join(ctx["card"](re.match(r"\{\{card ([a-z0-9-]+)\}\}", l).group(1)) for l in lines) + "</div>"); continue
        if first.startswith("## "):
            t = first[3:]; out.append(f'<h2 id="{slugify(t)}">{inline(t, ctx)}</h2>')
            if len(lines) > 1: out.append(md("\n".join(lines[1:]), ctx))
            continue
        if first.startswith("### "):
            out.append(f"<h3>{inline(first[4:], ctx)}</h3>")
            if len(lines) > 1: out.append("<p>" + inline(" ".join(lines[1:]), ctx) + "</p>")
            continue
        if all(l.startswith("|") for l in lines):
            rows = [[c.strip() for c in l.strip().strip("|").split("|")] for l in lines if not re.match(r"^\|[\s:|-]+\|?$", l)]
            head = "".join(f"<th>{inline(c, ctx)}</th>" for c in rows[0])
            body = "".join("<tr>" + "".join(f"<td>{inline(c, ctx)}</td>" for c in r) + "</tr>" for r in rows[1:])
            out.append(f'<div class="tbl"><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'); continue
        if all(l.startswith("- ") for l in lines):
            out.append("<ul>" + "".join(f"<li>{inline(l[2:], ctx)}</li>" for l in lines) + "</ul>"); continue
        if all(re.match(r"\d+\. ", l) for l in lines):
            out.append("<ol>" + "".join(f"<li>{inline(re.sub(r'^\d+\. ', '', l), ctx)}</li>" for l in lines) + "</ol>"); continue
        out.append("<p>" + inline(" ".join(lines), ctx) + "</p>")
    return "\n".join(out)

def faq_items(body):
    """Q&A pairs under a '## ... questions' / '## FAQ' heading (### question + answer)."""
    m = re.search(r"^## (?:FAQ|.*[Qq]uestions.*)$(.*?)(?=^## |\Z)", body, re.M | re.S)
    if not m: return []
    return [(q.strip(), re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", a.strip().replace("\n", " ").replace("**", "")))
            for q, a in re.findall(r"^### (.+)\n(.+?)(?=^### |\Z)", m.group(1), re.M | re.S)]

class Site:
    def __init__(self, root, page, site, owner, games, imgv, today):
        self.root, self.page, self.SITE, self.OWNER, self.imgv, self.today = root, page, site, owner, imgv, today
        self.games = {g["slug"]: g for g in games}
        self.order = [g["slug"] for g in games]
        gdir, ndir = os.path.join(root, "content/guides"), os.path.join(root, "content/news")
        self.guides = {}
        for f in sorted(os.listdir(gdir)):
            if f.endswith(".md"):
                g = parse(os.path.join(gdir, f)); self.guides[g["slug"]] = g
        self.posts = sorted([parse(os.path.join(ndir, f)) for f in os.listdir(ndir) if f.endswith(".md")],
                            key=lambda p: (p.get("date", ""), p["slug"]), reverse=True)
        self.posts = [p for p in self.posts if p.get("date", "") <= today]  # future-dated posts wait until their day

    def guide_url(self, slug): return f"/guides/{slug}/" if slug in self.guides else f"/games/{slug}/"
    def thumb(self, slug): return f"/img/{slug}.webp{self.imgv.get(slug, '')}"
    def name(self, slug): return self.games[slug]["name"]
    def play_btn(self, slug, label=None):
        return (f'<p class="playrow"><a class="play" href="/{slug}/">{PLAY}{e(label or ("PLAY " + self.name(slug).upper()))}</a></p>')
    def card(self, slug):
        g = self.games[slug]; gl = f'<a class="ghost" href="{self.guide_url(slug)}" aria-label="{e(g["name"])} guide">Guide</a>'
        return (f'<div class="gcard"><a href="/{slug}/" tabindex="-1" aria-hidden="true"><img src="{self.thumb(slug)}" alt="" width="600" height="375" loading="lazy" decoding="async"></a>'
                f'<div><b>{e(g["name"])}</b><span class="small">{e(g["tagline"])}</span>'
                f'<span class="btns"><a class="mini" href="/{slug}/" aria-label="Play {e(g["name"])}">Play</a>{gl}</span></div></div>')
    def shots(self, meta):
        items = [s.strip() for s in meta.get("shots", "").split(";") if s.strip()]
        if not items: return ""
        figs = []
        for it in items:
            f, alt, *cap = [x.strip() for x in it.split("|")]
            figs.append(f'<figure><img src="/img/guides/{f}" alt="{e(alt)}" width="393" height="852" loading="lazy" decoding="async">'
                        f'<figcaption>{e(cap[0] if cap else alt)}</figcaption></figure>')
        return '<div class="shots">' + "".join(figs) + "</div>"

    def org(self):
        return {"@type": "Organization", "name": "Games by Zaib", "url": self.SITE + "/",
                "logo": {"@type": "ImageObject", "url": self.SITE + "/img/icon-512.png"}}

    # ------------------------------------------------------------ guides
    def guide_page(self, gd):
        slug = gd["slug"]; g = self.games[slug]; url = f"{self.SITE}/guides/{slug}/"
        ctx = {"shots": lambda: self.shots(gd), "play": lambda: self.play_btn(slug), "card": self.card}
        body_html = md(gd["body"], ctx)
        rel = [r.strip() for r in gd.get("related", "").split(",") if r.strip() in self.games][:4]
        upd = gd.get("updated", self.today)
        crumbs = f'<nav class="crumbs" aria-label="Breadcrumb"><a href="/">Games</a> › <a href="/guides/">Guides</a> › <span>{e(g["name"])}</span></nav>'
        body = f"""{crumbs}
<span class="genre" style="--gc:{g['color']}">{e(g['genre'])}</span>
<h1>{e(gd['title'])}</h1>
<p class="lead">{inline(gd.get('lead', g['tagline']), ctx)}</p>
<p class="small">By {self.OWNER} · Updated {fmt_date(upd)} · Free to play, no download</p>
<a href="/{slug}/" tabindex="-1" aria-hidden="true"><img class="hero" src="{self.thumb(slug)}" alt="" width="600" height="375"></a>
{self.play_btn(slug)}
{body_html}
{self.play_btn(slug, "PLAY NOW")}
<h2 id="related">More games you might like</h2>
<div class="gcards">{''.join(self.card(r) for r in rel)}</div>
<p class="small"><a href="/guides/">All game guides</a> · <a href="/news/">Tips &amp; News</a> · <a href="/contact/">Send feedback</a></p>"""
        img = self.SITE + self.thumb(slug)
        shots = [self.SITE + "/img/guides/" + s.split("|")[0].strip() for s in gd.get("shots", "").split(";") if s.strip()]
        ld = [{"@context": "https://schema.org", "@type": "VideoGame", "name": g["name"], "url": f"{self.SITE}/{slug}/",
               "description": g["tagline"], "genre": g["genre"], "image": img, "screenshot": shots,
               "gamePlatform": ["Web browser", "Mobile phone", "Tablet", "Computer"], "applicationCategory": "Game",
               "operatingSystem": "Any", "inLanguage": "en", "isAccessibleForFree": True,
               "author": {"@type": "Person", "name": self.OWNER}, "publisher": self.org(),
               "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD", "availability": "https://schema.org/InStock"}},
              {"@context": "https://schema.org", "@type": "Article", "headline": gd["title"][:110], "description": gd["description"],
               "image": [img] + shots, "author": {"@type": "Person", "name": self.OWNER, "url": self.SITE + "/about/"},
               "publisher": self.org(), "datePublished": gd.get("published", upd), "dateModified": upd,
               "mainEntityOfPage": url, "about": {"@type": "VideoGame", "name": g["name"]}},
              crumbs_ld(self.SITE, [("Games", "/"), ("Guides", "/guides/"), (g["name"], f"/guides/{slug}/")])]
        faq = faq_items(gd["body"])
        if faq:
            ld.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]})
        self.page(f"/guides/{slug}/", gd.get("seo_title", gd["title"] + " | Games by Zaib"), gd["description"], body,
                  og_image=self.thumb(slug), ld=ld, og_type="article", active="/guides/")

    def guides_index(self):
        cats = {}
        for s in self.order:
            if s in self.guides: cats.setdefault(self.games[s]["genre"], []).append(s)
        n = sum(len(v) for v in cats.values())
        cards = "".join(self.card(s) for s in self.order)
        body = f"""<nav class="crumbs" aria-label="Breadcrumb"><a href="/">Games</a> › <span>Guides</span></nav>
<h1>Game guides</h1>
<p class="lead">Friendly, detailed guides for every game on Games by Zaib: how to play on a phone or computer, what each world and level holds, and tips for beginners and experts.</p>
<p>The guides are written by Zaib, who makes the games, so the level names, items and tricks match what you will see on screen. Pick a game below to read its guide, or tap Play to jump straight in. {'Looking for ideas instead? Our <a href="/news/">Tips &amp; News</a> page has beginner walkthroughs and round-ups of our games.' if self.posts else ''}</p>
<p class="small">{len(self.order)} games · updated {fmt_date(max([g.get("updated", self.today) for g in self.guides.values()] or [self.today]))}</p>
<div class="gcards">{cards}</div>"""
        ld = [{"@context": "https://schema.org", "@type": "CollectionPage", "name": "Game guides", "url": self.SITE + "/guides/",
               "hasPart": [{"@type": "Article", "headline": self.guides[s]["title"], "url": f"{self.SITE}/guides/{s}/"} for s in self.order if s in self.guides]}]
        self.page("/guides/", "Game Guides: Tips, Levels and Controls for Every Game | Games by Zaib",
                  "Detailed guides for every free game on Games by Zaib: phone controls, worlds and levels, beginner and advanced tips, and answers to common questions.",
                  body, ld=ld, active="/guides/")

    # ------------------------------------------------------------ news
    def post_page(self, p):
        slug = p["slug"]; url = f"{self.SITE}/news/{slug}/"
        ctx = {"shots": lambda: "", "play": lambda: "", "card": self.card}
        img_slug = p.get("image", "")
        img = self.thumb(img_slug) if img_slug in self.games else "/img/og.jpg"
        body = f"""<nav class="crumbs" aria-label="Breadcrumb"><a href="/">Games</a> › <a href="/news/">Tips &amp; News</a> › <span>{e(p['title'])}</span></nav>
<span class="genre" style="--gc:#7c3aed">{e(p.get('kind', 'Tips'))}</span>
<h1 class="h1post">{e(p['title'])}</h1>
<p class="lead">{inline(p.get('lead', p['description']), ctx)}</p>
<p class="small">By {self.OWNER} · {fmt_date(p['date'])}</p>
<img class="hero" src="{img}" alt="" width="600" height="375">
{md(p['body'], ctx)}
<h2 id="more">More from Tips &amp; News</h2>
<ul>{''.join(f'<li><a href="/news/{q["slug"]}/">{e(q["title"])}</a></li>' for q in [q for q in self.posts if q["slug"] != slug][:6])}</ul>
<p class="small"><a href="/news/">All posts</a> · <a href="/guides/">Game guides</a> · <a href="/">All games</a></p>"""
        ld = [{"@context": "https://schema.org", "@type": "BlogPosting", "headline": p["title"][:110], "description": p["description"],
               "image": [self.SITE + img], "author": {"@type": "Person", "name": self.OWNER, "url": self.SITE + "/about/"},
               "publisher": self.org(), "datePublished": p["date"], "dateModified": p.get("updated", p["date"]), "mainEntityOfPage": url},
              crumbs_ld(self.SITE, [("Games", "/"), ("Tips & News", "/news/"), (p["title"], f"/news/{slug}/")])]
        self.page(f"/news/{slug}/", p.get("seo_title", p["title"] + " | Games by Zaib"), p["description"], body,
                  og_image=img, ld=ld, og_type="article", active="/news/")

    def news_index(self):
        items = "".join(
            f'<article class="post"><a href="/news/{p["slug"]}/" tabindex="-1" aria-hidden="true"><img src="{self.thumb(p.get("image")) if p.get("image") in self.games else "/img/og.jpg"}" alt="" width="600" height="375" loading="lazy"></a>'
            f'<div><span class="small">{e(p.get("kind", "Tips"))} · {fmt_date(p["date"])}</span><h2><a href="/news/{p["slug"]}/">{e(p["title"])}</a></h2>'
            f'<p>{e(p["description"])}</p><a class="more" href="/news/{p["slug"]}/">Read more →</a></div></article>' for p in self.posts)
        body = f"""<nav class="crumbs" aria-label="Breadcrumb"><a href="/">Games</a> › <span>Tips &amp; News</span></nav>
<h1>Tips &amp; News</h1>
<p class="lead">Game tips, round-ups and updates from Games by Zaib. New posts arrive every week.</p>
<p>Here you will find beginner guides for our bigger games, lists of the best games for a quick break or a long session, picks for families, and a monthly look at what has changed on the site. Every post is written by playing the games, and every game it mentions is one click away.</p>
<div class="posts">{items}</div>"""
        ld = [{"@context": "https://schema.org", "@type": "Blog", "name": "Tips & News from Games by Zaib", "url": self.SITE + "/news/",
               "blogPost": [{"@type": "BlogPosting", "headline": p["title"], "url": f"{self.SITE}/news/{p['slug']}/", "datePublished": p["date"]} for p in self.posts]}]
        self.page("/news/", "Tips & News: Game Tips, Round-ups and Updates | Games by Zaib",
                  "Beginner guides, best-of lists, family picks and monthly updates for the free games on Games by Zaib.", body, ld=ld, active="/news/")

    def build(self):
        for gd in self.guides.values():
            if gd["slug"] in self.games: self.guide_page(gd)
        self.guides_index()
        for p in self.posts: self.post_page(p)
        if self.posts: self.news_index()

    def urls(self):
        out = [("/guides/", self.today, "0.8")] + ([("/news/", self.posts[0]["date"], "0.8")] if self.posts else [])
        out += [(f"/guides/{s}/", self.guides[s].get("updated", self.today), "0.8") for s in self.order if s in self.guides]
        out += [(f"/news/{p['slug']}/", p.get("updated", p["date"]), "0.7") for p in self.posts]
        return out

PLAY = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 4.5v15a1 1 0 0 0 1.53.85l12-7.5a1 1 0 0 0 0-1.7l-12-7.5A1 1 0 0 0 7 4.5z"/></svg>'

def fmt_date(d):
    try: return datetime.date.fromisoformat(d).strftime("%-d %B %Y")
    except Exception: return d

def crumbs_ld(site, items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": site + u} for i, (n, u) in enumerate(items)]}
