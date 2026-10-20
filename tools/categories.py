"""Crawlable category hubs: /games/ (index) and /games/<cat>/. Intros are hand-written; game facts come from the guides."""
from html import escape as e

CATEGORIES = [
 ("idle", "Idle and Tycoon Games", "Idle & tycoon",
  "Free idle and tycoon games: Boss Town Tycoon, Chai Tycoon and Corner Office. Build a business, buy upgrades and watch your money grow, in your browser with no download.",
  ["Idle games are the ones where you tap a little, buy a lot and watch the numbers climb, even when you put the phone down for a while. We have three of them, and they are more different than they look.",
   "<b>Boss Town Tycoon</b> starts you with $10 and one empty lot and grows into a whole town of businesses, with investors to sell to, stars, ranks and perks that make every new run faster. <b>Chai Tycoon</b> begins with one chaiwala and one kettle and grows into a whole bazaar of shops run by managers, and <b>Corner Office</b> climbs the career ladder from Intern on floor 2 to the CEO's office on floor 60, with quick office minigames along the way.",
   "Each one has its own long-term goal. In Boss Town Tycoon, selling your town to investors starts you over, but every investor makes all your shops earn 2% more on the next run. In Chai Tycoon, shops with a manager keep earning while you are away, up to an offline limit. In Corner Office, funny coworkers help you climb from floor to floor toward the top.",
   "All three save your progress on your device, so short sessions are fine. If you are not sure where to start, our comparison post explains how they differ, how long each one takes and which one suits you."],
  ["boss-town", "chai-tycoon", "corner-office"], "/news/idle-games-compared/", "Boss Town, Chai Tycoon or Corner Office? Our three idle games compared"),
 ("puzzle", "Puzzle and Brain Games", "Puzzle",
  "Free puzzle games for phone and computer: Bus Bonanza, Rail Rush, Juicy Merge, Block Glide, Number Dash and Kedim's Snack Swing. Think first, then tap. No download.",
  ["These are the games where thinking ahead matters more than fast fingers. Each one is built around a single clear idea, and the levels slowly ask you to plan a little further.",
   "In <b>Bus Bonanza</b> you free vehicles from a packed car park in the order the passenger queue needs them. In <b>Rail Rush</b> you tap switches so each train reaches the station of its colour, and every station has a symbol as well as a colour. <b>Juicy Merge</b> drops fruit into a jar, where matching pieces merge into bigger fruit. <b>Block Glide</b> slides clay blocks through matching gates, <b>Kedim's Snack Swing</b> asks you to cut ropes so a treat swings into a hungry cat's mouth, and in <b>Number Dash</b> you steer a runner through gates that add, take away, multiply or divide so you finish bigger than the Number Monster.",
   "Most levels are short, so these games fit into a spare few minutes, and every one saves your progress on your device. Each guide below explains the rules and the habits that help you earn three stars."],
  ["bus-bonanza", "rail-rush", "juicy-merge", "block-glide", "kedim-snack-swing", "number-dash"], "/news/driving-games-guide/", "On the move: our bike, truck, train and bus games compared"),
 ("racing", "Racing, Driving and Flying Games", "Racing & driving",
  "Free racing, driving and flying games: Moto Mayhem, Haulway Heroes, Horizon Pilot and Zaib City. Race motorbikes, haul cargo, fly planes and drive around a 3D city.",
  ["If it has wheels or wings, it is here. These four games all put you in control of a vehicle, but they ask for very different skills.",
   "<b>Moto Mayhem</b> is a fast motorbike race against seven rivals, with cartoon punches and kicks and five tracks from Sunset Coast to Frost Peak. <b>Haulway Heroes</b> is the calm one: a 3D truck-driving game where smooth driving and good parking earn the best pay. <b>Horizon Pilot</b> is a flight game on a 3D island with seven airports and assisted controls, so a child can take off on the first try. <b>Zaib City</b> is an open 3D city to explore on foot and by car, where you earn money driving taxis, delivering pizza and putting out fires.",
   "The 3D games need a reasonably recent phone, and quality adjusts automatically. Moto Mayhem includes cartoon fighting between riders, so it suits older children best."],
  ["moto-mayhem", "haulway-heroes", "horizon-pilot", "zaib-city"], "/news/flying-games-guide/", "Up in the air: our four flying games, from paper planes to jet fighters"),
 ("kids", "Gentle Games for Younger Players", "Kids & cozy",
  "Calm, kind games for younger children: Silly Sprout Garden, Betta Bestie, Baby Kedim, Dream Room, Sunny Acres, Critter Keep Rescue and more. Free, no download, no sign-up.",
  ["These games are built so younger children can play at their own pace, with big buttons, light reading and nothing scary. When something goes wrong, the result is always kind: a plant just grows a little slower, a pet is a bit hungry, or a giggling raccoon sends you back to the start.",
   "Grow funny plant creatures in <b>Silly Sprout Garden</b>, look after a pet fish in <b>Betta Bestie</b> or a black kitten in <b>Baby Kedim</b>, decorate rooms for clients in <b>Dream Room</b>, run a small farm in <b>Sunny Acres</b>, or make music with <b>Beat Buddies</b>. <b>Critter Keep Rescue</b> adds a little excitement, with sneaking past patrolling raccoons to free critters from cages, and <b>Kedim Therapist</b> is a kind, funny story about a cat who listens to silly patients.",
   "Not every game on the site is aimed at young children, since some are action games. This page collects the ones we would hand to a five- or six-year-old with confidence. Each guide explains the controls and what to expect."],
  ["silly-sprout-garden", "betta-bestie", "baby-kedim", "dream-room", "sunny-acres", "beat-buddies", "critter-keep-rescue", "kedim-therapist"], "/news/gentle-games-for-young-kids/", "No timers, no losing: five gentle games for younger children"),
 ("action", "Action and Adventure Games", "Action",
  "Free cartoon action and adventure games: Skyfire Squadron, Bolt Brigade, Tank Rumble, Meowstronauts, Horde Breaker, Fortress Frontline, Pirate Isles and more. No download.",
  ["Quick reflexes and cartoon chaos. These games have bosses to beat, upgrades to buy and stars to chase, but the style stays light: robots pop into bolts and coins, beaten pirates wave a white flag and sail away, and nobody is shown getting hurt.",
   "Shooters such as <b>Skyfire Squadron</b>, <b>Meowstronauts</b> and <b>Tank Rumble</b> fire automatically, so all your attention goes on dodging. <b>Bolt Brigade</b> is a cover shooter where ducking at the right moment matters most. <b>Fortress Frontline</b> is tower defence, <b>Pirate Isles</b> is a sailing adventure, and <b>Hop Heights</b> and <b>Kedimz Adventure</b> are platformers. <b>Horde Breaker</b> and <b>30 Floors Up</b> have goofy cartoon zombies and suit older children.",
   "Our post on first-try lessons explains the one habit that made each of several of these games click for us, which is a good place to start if a first round goes badly."],
  ["skyfire-squadron", "bolt-brigade", "tank-rumble", "meowstronauts", "fortress-frontline", "pirate-isles", "hop-heights", "kedimz-adventure", "horde-breaker", "30-floors-up", "gobble-hole", "fin-frenzy", "noodle-clash"], "/news/first-try-lessons/", "We lost first: what five of our games taught us on the first try"),
 ("arcade", "Quick Arcade Games", "Quick arcade",
  "Short, replayable arcade games: Sky Glide, Neon Dash, Gobble Hole, Fin Frenzy, Noodle Clash and Hop Heights. One-minute rounds, simple controls, free in your browser.",
  ["Arcade games are for when you have a minute or two. Rounds are short, the controls fit on one thumb, and the goal is simple: go a bit further or score a bit more than last time.",
   "<b>Sky Glide</b> is a paper plane with one control: hold to lift and let go to glide, with five worlds from a classroom to outer space. <b>Neon Dash</b> is a one-button runner in a glowing synthwave city, <b>Gobble Hole</b> lets you steer a hungry hole that swallows a city, <b>Fin Frenzy</b> puts you in charge of a hungry shark, and <b>Noodle Clash</b> is a snake-style battle in a giant noodle bowl that two players can share on one phone. <b>Hop Heights</b> adds a 3D obstacle course.",
   "All of them save your best scores on your device. The guides below share the small tricks, like short taps in Sky Glide, that make the biggest difference."],
  ["sky-glide", "neon-dash", "gobble-hole", "fin-frenzy", "noodle-clash", "hop-heights"], "/news/two-player-games-one-phone/", "Two players, one phone: our games you can play together"),
 ("sports", "Sports Games", "Sports",
  "Free sports games: Goal Frenzy arcade football and Shuttle Smash badminton, both with a two-player mode on one phone. Play in your browser, no download.",
  ["Short, fast matches with simple swipe and button controls. Both of our sports games can be played alone against the computer or by two people sharing one phone or tablet.",
   "<b>Goal Frenzy</b> is arcade football with curling shots and over-the-top power shots. In two-player mode each person controls their team from their own half of the screen. <b>Shuttle Smash</b> is badminton where your player runs to the shuttle by itself and you decide the shot by swiping: a short swipe for a drop shot near the net, a long swipe to send it to the back, and a long swipe on a high shuttle for a jump smash. Its two-player mode works best with the phone flat on a table and the players facing each other.",
   "On a computer, Goal Frenzy's Player 1 uses W A S D and Player 2 uses the arrow keys, while on a phone each player gets their own joystick and buttons. Goal Frenzy offers 5-a-side and 7-a-side matches, and 5-a-side is easier to follow when you are starting out.",
   "Both games are cartoon style, with short matches that suit a quick break or a family rematch. Our two-player post explains how each mode splits the screen and how to set up a fair match."],
  ["goal-frenzy", "shuttle-smash"], "/news/two-player-games-one-phone/", "Two players, one phone: our games you can play together"),
]

def build(page, site, SITE, posts):
    def postlink(url, title):
        slug = url.strip("/").split("/")[-1]
        return f'<p>Read more: <a href="{url}">{e(title)}</a></p>' if slug in posts else ""
    chips = "".join(f'<a class="ghost" href="/games/{c[0]}/">{e(c[2])}</a>' for c in CATEGORIES)
    index_cards = "".join(
        f'<div class="cat"><h2><a href="/games/{slug}/">{e(title)}</a></h2><p>{e(desc)}</p><p class="small">{len(games)} games</p></div>'
        for slug, title, short, desc, intro, games, purl, ptitle in CATEGORIES)
    body = f"""<p class="crumbs"><a href="/">Games</a> › Categories</p>
<h1>Browse Games by Category</h1>
<p class="lead">Games by Zaib has free games of many kinds, from calm pet and garden games to fast shooters and racing. Pick a category to see the games in it, with a short introduction to each and a link to its full guide.</p>
<p>Some games appear in more than one category. Gobble Hole, for example, is in both Action and Quick arcade. Every game plays in the browser on phones, tablets and computers, with no download or sign-up, and saves your progress on your device.</p>
{index_cards}
<p>Looking for tips instead? Every game has a <a href="/guides/">guide</a>, and <a href="/news/">Tips &amp; News</a> has round-ups and comparisons.</p>"""
    page("/games/", "Game Categories: Puzzle, Idle, Racing, Action, Kids and More | Games by Zaib",
         "Browse free browser games by category: idle and tycoon, puzzle, racing and driving, gentle games for kids, action, quick arcade and sports. No download.", body, active="/games/")
    urls = ["/games/"]
    for slug, title, short, desc, intro, games, purl, ptitle in CATEGORIES:
        games = [g for g in games if g in site.games]
        others = "".join(f'<a class="ghost" href="/games/{c[0]}/">{e(c[2])}</a>' for c in CATEGORIES if c[0] != slug)
        body = f"""<p class="crumbs"><a href="/">Games</a> › <a href="/games/">Categories</a> › {e(short)}</p>
<h1>{e(title)}</h1>
<p class="lead">{intro[0]}</p>
{''.join(f'<p>{p}</p>' for p in intro[1:])}
<h2>The games</h2>
<div class="gcards">{''.join(site.card(g) for g in games)}</div>
{postlink(purl, ptitle)}
<h2>More categories</h2>
<p class="btns">{others}</p>"""
        ld = [{"@context": "https://schema.org", "@type": "CollectionPage", "name": title, "url": f"{SITE}/games/{slug}/",
               "hasPart": [{"@type": "VideoGame", "name": site.name(g), "url": f"{SITE}/{g}/"} for g in games]},
              {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
                  {"@type": "ListItem", "position": 1, "name": "Games", "item": f"{SITE}/"},
                  {"@type": "ListItem", "position": 2, "name": "Categories", "item": f"{SITE}/games/"},
                  {"@type": "ListItem", "position": 3, "name": short, "item": f"{SITE}/games/{slug}/"}]}]
        page(f"/games/{slug}/", f"{title}: Free in Your Browser | Games by Zaib", desc, body, ld=ld, active="/games/")
        urls.append(f"/games/{slug}/")
    return urls
