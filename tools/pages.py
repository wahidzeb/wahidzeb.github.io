#!/usr/bin/env python3
"""Generates the static info pages (about, contact, privacy, terms, games/<slug>/),
sitemap.xml and robots.txt for https://zaibgames.com/.
Run via ./build.sh (or directly: python3 tools/pages.py). Edit GAME_INFO below to add
an info page for a new game. Game URLs for the sitemap are also read from the GAMES
array in index.template.html, so any card there is included automatically."""
import html, os, re, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://zaibgames.com"
EMAIL = "wahid.zeb@gmail.com"
OWNER = "Zaib"
GA_TAG = """<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-0WE2FDHVM9"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-0WE2FDHVM9');
</script>"""
UPDATED = "11 October 2026"
LASTMOD = "2026-10-11"
e = html.escape

# ---------------------------------------------------------------- game info
GAME_INFO = [
 dict(slug="moto-mayhem", name="Moto Mayhem", genre="Racing", color="#f97316",
  tagline="A motorbike combat racer: ride fast, hit hard, finish first.",
  about=["Moto Mayhem is a road-rash style motorbike racing game for phones and desktop browsers. Every race puts you on a winding highway against seven rival bikers, and the quickest way past them is often a well-timed punch or kick.",
         "Race through five tracks, from the easy curves of Sunset Coast to the icy hairpins of Frost Peak. Win cash, buy faster bikes in the garage and upgrade your engine, tires and armor to climb the standings."],
  how=["Throttle is automatic. Steer to stay on the road and dodge traffic and roadside objects.",
       "Ride alongside a rival and attack toward their side. Kicks reach further and hit harder but are slower than punches.",
       "Empty a rival's health bar to knock them off their bike for bonus cash. Grab a club for heavy hits, or knock out a rival carrying one to steal it.",
       "Watch both bars: crashes damage your BIKE (zero means wrecked), and hits drain your RIDER health (zero means you are knocked down and lose time).",
       "From Red Canyon on, a police biker patrols. Get knocked down near him and you are busted with a fine, or knock him out for a big bonus.",
       "Finish in the top 3 to unlock the next track."],
  controls=[("Steer","Hold the left/right side of the screen (Touch), slide your thumb (Drag) or tilt your phone (Tilt)","← / →"),
            ("Brake","BRAKE button","↓"),("Punch left / right","◀ PUNCH / PUNCH ▶","A / D"),
            ("Kick left / right","◀ KICK / KICK ▶","Q / E"),("Pause","II button","P / Esc")],
  features=["5 tracks: Sunset Coast, Pine Valley, Red Canyon, Neon City and Frost Peak, with rising traffic, hills and oncoming cars",
            "7 rival bikers per race with their own health bars and aggression",
            "4 bikes to buy, from the Rustbucket 250 to the Thunderbolt 1200",
            "Garage upgrades for engine, tires and armor",
            "Pickups: cash, wrench (bike repair), medkit (health), nitro (speed boost) and clubs",
            "Police patrols on later tracks",
            "Three steering modes (Touch, Drag, Tilt with calibration), vibration and sound settings",
            "Progress saved on your device"]),
 dict(slug="sky-glide", name="Sky Glide", genre="Casual", color="#ec4899",
  tagline="A hand-drawn paper plane flying game.",
  about=["Sky Glide is a one-touch flying game with a sketchbook look. You pilot a paper plane: hold to lift, release to glide, and thread your way past pencils, birds, cranes, storm clouds and even black holes.",
         "Fly through five worlds, from a school classroom to outer space, each with its own art, music, obstacles and physics. Chain near misses into combos, collect hidden stars and coins, and unlock new planes in the hangar."],
  how=["Hold anywhere on the screen to lift the plane; release to glide down.",
       "Avoid obstacles. Passing close to one without touching it gives a near-miss bonus, and near misses in a row build a combo multiplier up to x8.",
       "Collect coins and the 3 hidden stars in each level. Clear a level to unlock the next one.",
       "Pick up power-ups: Shield, Magnet, Slow-mo and Boost (Boost smashes through obstacles).",
       "Spend coins in the Hangar on new planes with different lift, glide, control and hearts.",
       "Try Endless mode to fly through all five worlds in a row and beat your best distance."],
  controls=[("Lift","Hold anywhere","Hold Space / ↑ / W or the mouse button"),
            ("Glide","Release","Release"),("Pause","Pause button (top right)","P / Esc")],
  features=["5 worlds and 20 levels: Classroom, Sunny Park, City Rooftops, Stormy Skies and Outer Space",
            "World-specific physics, such as low gravity in space and gusts and downdrafts in the storm",
            "Endless mode with rising speed and a saved best distance",
            "60 hidden stars to find",
            "7 plane designs with perks like a bigger magnet, longer power-ups or +50% coins",
            "14 goals that pay out bonus coins",
            "Music and sound effects generated live in the browser",
            "Progress saved on your device"]),
 dict(slug="horde-breaker", name="Horde Breaker", genre="Shooter", color="#ef4444",
  tagline="A top-down zombie survival shooter.",
  about=["Horde Breaker is a twin-stick style zombie shooter built for touch screens. Auto-fire is on by default: you focus on moving and dodging while your gun locks onto the most dangerous zombie.",
         "Survive five cursed maps, from Suburbia to a rain-soaked Night City. Between waves you pick roguelite power cards that stack for the run, and you can call in specials like an Air Strike or a Black Hole. The cartoon style keeps it gore-free."],
  how=["Move with the left joystick (or WASD). Your weapon aims and fires automatically.",
       "Keep moving. Brutes telegraph a charge, spitters fire acid, bloaters explode and crawlers lunge.",
       "After each cleared wave, pick 1 of 3 power cards. The perks stack for the rest of the run.",
       "Use your special when the ring is full. Kills recharge it faster.",
       "Throw grenades, drop an auto-turret and dash out of trouble; the dash gives brief invulnerability.",
       "Earn coins to buy and upgrade weapons, specials and survivor stats in the Armory."],
  controls=[("Move","Left joystick","WASD / arrow keys"),
            ("Aim + fire","Automatic (touch the right side to aim manually)","Automatic, or hold the left mouse button"),
            ("Special","Big corner button","C"),("Dash","Dash button","Space / Shift"),
            ("Grenade","Grenade button","G / right-click"),("Turret","Turret button","E / F"),
            ("Reload","Button beside the weapon panel","R"),("Switch weapon","Tap the weapon panel","Q / Tab / 1–3 / mouse wheel"),
            ("Pause","Pause button","P / Esc")],
  features=["Campaign of 5 maps and 20 levels with wave, timed-survival and boss levels, each with 3 stars",
            "Endless survival on any map with a boss every 5 waves",
            "7 zombie types and 5 named bosses",
            "19 stackable power-card perks such as Vampire, Drone Buddy and Cryo Rounds",
            "4 specials: Air Strike, Rage Mode, Black Hole and Tesla Storm",
            "8 upgradeable weapons, from pistol to minigun, plus 15 power-ups",
            "Aim modes (Auto, Assist, Manual), left-handed layout and joystick options",
            "Progress saved on your device"]),
 dict(slug="goal-frenzy", name="Goal Frenzy", genre="Sports", color="#22c55e",
  tagline="Fast, glossy arcade football (soccer).",
  about=["Goal Frenzy is an arcade football game with a 3D-perspective stadium, curling shots and over-the-top power shots. Matches are short and fast, and they play well with a thumb on a phone or on a keyboard.",
         "Play a Quick Match against the CPU, take on a friend on the same device, win the 8-team Zaib Cup, run a full League season or settle it in a Penalty Shootout. Create your own club, earn coins and upgrade your squad."],
  how=["Move with the floating joystick on the left side of the screen.",
       "Tap SHOOT to shoot; hold it for more power and swipe across the button to curl the ball.",
       "Tap PASS for a ground pass; hold it for a lob or through ball. Hold SPRINT to run faster (uses stamina).",
       "Without the ball, SHOOT becomes SLIDE (tackle) and PASS becomes SWITCH player.",
       "Fill the power meter and press POWER to unleash a special shot such as Fire Shot or Banana Curve.",
       "In penalties, swipe up toward the goal to shoot and tap where you want to dive when you are in goal."],
  controls=[("Move","Left thumb (floating joystick)","Arrows / WASD"),("Shoot / slide","SHOOT button or swipe on the right half","Space / J"),
            ("Pass / switch","PASS button or tap on the right half","X / K"),("Sprint","SPRINT (hold)","Shift / L"),
            ("Power shot","POWER","E / Q"),("Pause","Pause button","P / Esc")],
  features=["Modes: Quick Match, Zaib Cup (knockout), League (7 matchdays) and Penalty Shootout",
            "2 players on one device, each with their own half of the screen (P1 WASD, P2 arrows on keyboard)",
            "5v5 or 7v7, four difficulties from Easy to Legend",
            "7 power shots, including Phantom Shot and Sky Meteor",
            "16 fictional clubs plus your own custom club, kit and badge colours",
            "Day, dusk and night matches with slow-motion goal replays",
            "Interactive training tutorial and assisted controls",
            "Progress saved on your device"]),
 dict(slug="shuttle-smash", name="Shuttle Smash", genre="Sports", color="#0ea5e9",
  tagline="3D badminton with swipe-to-hit controls.",
  about=["Shuttle Smash is a badminton game for phones with a portrait 3D-perspective court and realistic shuttlecock physics, including drag and tumbling feathers. Your player moves to the shuttle automatically, so you only need to think about where and how hard to hit.",
         "Play a quick match against the CPU or a friend on the same phone, travel the World Tour against fictional rivals, or win the Zaib Open knockout. Earn coins for stat upgrades, rackets, outfits and power shots."],
  how=["Swipe to hit: the swipe direction sets your aim and its length and speed set the power.",
       "A short swipe plays a drop or net shot, a long swipe plays a clear or lob, and a long swipe on a high shuttle is a jump smash. Tap for an automatic shot.",
       "The power button fills during rallies. Use it for Thunder Smash, Fire Clear, Phantom Drop or Tornado Shot.",
       "In 2-player mode, sit facing each other: P1 swipes on the bottom half and P2 on the top half.",
       "Win rallies to score. Matches use rally scoring to 21 (win by 2, cap 30), or 11/15 points."],
  controls=[("Hit / aim","Swipe (direction = aim, length = power)","J / K / L soft, medium, hard; ← / → aim"),
            ("Auto shot","Tap","Space"),("Power shot","Power button","E"),("Pause","Pause button","P")],
  features=["Quick Match: 1 player vs CPU (4 difficulties) or 2 players on one phone",
            "World Tour: 10 stages across 5 day and night venues",
            "Zaib Open: 8-player knockout bracket",
            "Training: 6 challenges with a coach",
            "4 power shots, rackets, outfits and stat upgrades",
            "Slow motion, replays, commentator callouts and crowd reactions",
            "Progress saved on your device"]),
 dict(slug="kedimz-adventure", name="Kedimz Adventure", genre="Platformer", color="#f59e0b",
  tagline="A side-scrolling platformer starring Kedimz the cat.",
  about=["Kedimz Adventure is a mobile-first side-scrolling platformer. Kedimz the cat sets out to bring back the Golden Bells across five worlds of four levels each, and every world ends with a boss fight.",
         "Jump, run and paw-swipe through Meadow Hills, Sunscorch Desert, Frostbite Caverns, Ember Castle and Cloud Kingdom. Collect gems and coins, find secret bonus rooms and spend your coins on cat skins, hats and upgrades. All characters, art and music are original."],
  how=["Move left and right. Keep holding a direction and Kedimz speeds up into a run.",
       "Press JUMP to jump; hold it for a higher jump. Stomp on enemies or swipe them with your paw.",
       "Break bricks and hit blocks to find coins and power-ups. Some pipes lead to secret bonus rooms.",
       "Damage is forgiving: you shrink first, then lose a heart. Falling into a pit costs a heart and puts you back on safe ground.",
       "Collect 3 gems in each level and beat your best time. 100 coins give an extra life.",
       "Defeat the boss at the end of each world to open the next."],
  controls=[("Move","◀ ▶ buttons (or joystick)","← → / A D"),("Jump","JUMP (hold for higher)","Space / ↑ / W / Z / K"),
            ("Paw swipe / fire / ice / enter","Action button","X / J / C / Shift (↓ / S enters)"),("Pause","⏸ button","Esc / P")],
  features=["5 worlds and 20 levels with their own scenery, enemies, hazards and music",
            "5 bosses: Mole King, Scarab Pharaoh, Yeti, Magma Golem and Storm Owl",
            "Power-ups: Size Up, Fire Paw, Ice Paw, Wings (double jump), Coin Magnet and Star",
            "World map with 3 gems per level and best times",
            "Shop with cat skins, hats and upgrades",
            "Checkpoints, moving and falling platforms, springs, spikes and lava",
            "Button or joystick controls, adjustable button size and left-handed layout",
            "Progress saved on your device"]),
 dict(slug="meowstronauts", name="Meowstronauts", genre="Shooter", color="#a855f7",
  tagline="Two space cats fly their rockets across the galaxy. Play solo or 2-player co-op.",
  about=["Meowstronauts is an arcade space flyer and shooter for phones and desktop browsers. Sunny the yellow cat and Shadow the black cat ride their rockets across six planets to get home. Along the way they dodge asteroids, collect fish stars and blast space mice and robots.",
         "Each planet has its own look, music, hazards and boss: Moon Cheese, Candy Planet, Ice Comet, Lava World, Black Hole and finally Home: Purrth. Play alone and swap between the two cats at any time, or team up with a friend on the same phone. All characters, art and music are original."],
  how=["Drag anywhere on the screen to fly. Your cat follows your finger's movement and shoots automatically.",
       "Tap the big button to use your cat's power. Sunny's Sun Shield blocks and reflects bullets. Shadow's Shadow Cloak phases through everything and ends with a burst.",
       "Collect fish stars to fill the MEOW meter, then unleash a Mega Meow shockwave that clears every bullet on screen.",
       "In 1 Player the other cat flies as a sidekick. Tap SWAP to switch cats; each cat has its own power cooldown.",
       "In 2 Players, Player 1 drags on the left half and Player 2 on the right half. Fly into a knocked-out friend's bubble to rescue them.",
       "Shoot the glowing ? UFOs to get power-ups, and beat the boss at each planet to unlock the next one."],
  controls=[("Fly","Drag anywhere (or floating joystick)","WASD / Arrow keys"),("Cat power","Big button","Space"),
            ("Mega Meow","MEOW button","E"),("Swap cats (1P)","SWAP button","Shift / Q"),("Pause","⏸ button","Esc / P")],
  features=["6 planets with their own scenery, hazards, music and boss fights",
            "Two cats with different weapons and powers, with cat swapping in 1 Player",
            "2-player co-op on one phone with full multi-touch",
            "Power-ups: Mega Laser, Fish Magnet, Bubble Shield, Mega Meow, Mini-Cats, Rocket Boost, Time Purr, Double Shot and Extra Heart",
            "3 stars per planet, 18 missions and an Endless Voyage mode that saves your best distance",
            "Shop with rocket upgrades, 12 costumes and 7 rocket skins",
            "Easy, Normal and Hard difficulty with warnings before every hazard",
            "Progress saved on your device"]),
 dict(slug="fin-frenzy", name="Fin Frenzy", genre="Arcade", color="#06b6d4",
  tagline="Be the shark: eat fish, grow bigger and battle ocean bosses.",
  about=["Fin Frenzy is an underwater arcade game for phones and desktop browsers. You play a hungry shark that starts small and grows by eating fish. Your hunger bar keeps dropping, so you have to keep eating, while avoiding predators, mines, jellyfish and harpoons.",
         "Dive through five zones: Coral Reef, Shipwreck Bay, Arctic Ice, Deep Sea and The Abyss, where the only light comes from glowing creatures. Each zone has five levels and ends with a boss fight. Earn coins to unlock new sharks from the Hammerhead to the Megalodon and fit them with gadgets like a jetpack and a laser visor."],
  how=["Drag anywhere on the screen to steer with a floating joystick, or switch to follow-finger mode in Settings.",
       "Swim into fish that are smaller than you to eat them. Auto-bite is on by default. Bigger fish glow red: stay away until you have grown.",
       "Keep the hunger bar full. Eating quickly builds a combo, and filling the Frenzy meter makes you faster and lets you eat almost anything for a short time.",
       "Tap BOOST (or double-tap) for a burst of speed and BITE for a strong bite. Boost uses stamina, which refills on its own.",
       "Pick up power-ups such as Magnet, Bubble Shield, Jet Boost, Laser, Mega Bite, Heal and Gold Rush.",
       "Complete each level's goal to earn up to 3 stars. In boss levels, eat and grow first, then bite the boss when it is tired or stunned to deal critical damage."],
  controls=[("Swim","Drag anywhere (floating joystick) or follow your finger","WASD / Arrow keys"),("Boost","BOOST button or double-tap","Space / Shift"),
            ("Bite","BITE button (auto-bite is on by default)","X / J"),("Pause","II button","P / Esc")],
  features=["5 ocean zones with 25 levels, each with a different goal, plus an Endless mode for each zone that saves your best score",
            "5 bosses: King Crab, The Iron Tide submarine, Frost Narwhal, Giant Squid and Abyss Angler",
            "6 sharks to unlock and upgrade: Reef Shark, Hammerhead, Mako, Tiger Shark, Great White and Megalodon",
            "Gadgets with 5 upgrade levels each: Jetpack, Laser Visor, Coin Magnet, Armor Plates, Big Belly and Frenzy Charm",
            "Combos, Frenzy mode, Gold Rush, treasure chests, missions and Lucky Shell revives",
            "Light rays, caustics, parallax scenery and glowing deep-sea creatures, all drawn in code",
            "Stick or follow-finger controls, left-handed layout, graphics quality, sound, music and vibration settings",
            "Progress saved on your device"]),
 dict(slug="bus-bonanza", name="Bus Bonanza", genre="Puzzle", color="#eab308",
  tagline="Clear the jammed parking lot and send every passenger home on the right bus.",
  about=["Bus Bonanza is a color-matching bus parking puzzle for phones and desktop browsers. The parking lot is jammed with buses facing every direction. Tap a bus to drive it out to the station, where a line of passengers waits to board the bus that matches their color. When a bus is full it drives away and frees its bay.",
         "There are 120 levels, and a solver bot has checked that every one can be won without boosters. There is also a fresh Daily Challenge each day. Some levels swap the parking lot for a Crowd Rush, where you tap passengers to send them to the arriving buses. Spend the coins you win on bus skins, the City, Beach, Snow and Night themes, and boosters."],
  how=["Tap a bus to drive it out of the lot. Buses only drive forward, in the direction of the arrow on the roof. If another bus or obstacle is in the way, it bumps and stays put.",
       "Each bus parks in a free station bay. Passengers at the front of the line board a parked bus of their color, one at a time. A full bus departs and frees its bay.",
       "You lose when every bay is taken and the next passenger matches none of the parked buses, so plan which colors you bring in.",
       "In Crowd Rush levels, tap a passenger who has a clear path to the top. If they match the waiting bus they board it. If not, they sit on the bench, and a full bench ends the level.",
       "Watch for the new mechanics: 4-, 6- and 10-seat buses, grey mystery buses, padlocked buses that need the key bus to leave first, ice that melts as other buses depart, garages that release more buses, VIP passengers worth bonus coins, and timed levels.",
       "Boosters: Extra Bay opens another bay or bench seat, Undo takes back a move, Shuffle rearranges waiting passengers, Magnet pulls matching passengers onto parked buses, and Helicopter airlifts any bus or passenger. Fewer bumps earn more stars."],
  controls=[("Drive a bus / send a passenger","Tap it","Mouse click"),("Boosters","Buttons along the bottom (right side in landscape)","1-5, U or Z for Undo"),("Pause","II button","P / Esc")],
  features=["120 levels, each checked by a solver bot, plus a level map with up to 3 stars per level",
            "Two modes: Parking Lot and Crowd Rush",
            "Mystery buses, locks and keys, ice, garages, VIP passengers, timed levels and 4-, 6- and 10-seat buses",
            "A Daily Challenge generated in your browser, with bonus coins and a streak counter",
            "5 boosters: Extra Bay, Undo, Shuffle, Magnet and Helicopter",
            "Shop with 7 bus skins and 4 themes (City, Beach, Snow, Night)",
            "Shaded pseudo-3D buses and people, smooth driving animations, combos, confetti, and music and sound effects made in code",
            "Tutorial hand hints, sound, music, vibration and graphics settings, with progress saved on your device"]),
 dict(slug="neon-dash", name="Neon Dash", genre="Arcade", color="#22d3ee",
  tagline="One tap, 200 neon levels: jump the spikes and dash to the finish gate.",
  about=["Neon Dash is a one-tap rhythm runner for phones and desktop browsers. A glowing cube races through a synthwave city on its own, and your only job is to jump at the right moment to clear pink spikes and purple blocks on the way to the finish gate.",
         "There are 200 levels. Each one has a fixed layout, so practice pays off, and a solver has checked that each one can be beaten with fair timing. Later levels are faster and packed tighter. Every level has its own synthwave track and color theme, and the coins you collect unlock 44 neon cube skins."],
  how=["Your cube moves forward automatically. Tap the screen, or press Space, the Up arrow or W, to jump.",
       "Touching a spike or a block ends the run. You cannot stand on blocks, so jump clean over everything.",
       "Hold the button to jump again the moment you land. This is the easiest way through tight runs of spikes, and a short input buffer also catches taps that come slightly early.",
       "Grab the yellow coins floating in the air. Finishing a level gives 5 bonus coins and unlocks the next one.",
       "The bar at the top shows your progress, and a yellow mark shows your best run on that level. After a crash, tap to retry straight away.",
       "Spend coins in the Skin Shop. Tip: in portrait you see less of the track ahead, so turning your phone sideways helps on later levels."],
  controls=[("Jump (hold to keep jumping)","Tap / hold anywhere","Space, Up arrow or W"),("Pause","II button","P / Esc"),("Restart level","Pause, then Restart","R")],
  features=["200 levels with fixed layouts, each checked by a solver, with unlocks and best percentage per level",
            "44 neon cube skins to buy with coins",
            "Synthwave city with parallax, a striped sun, a moving grid floor, glow, trails, particle bursts and screen shake",
            "10 synthwave music tracks and sound effects made in code with WebAudio",
            "Hold-to-jump, an input buffer and a resume countdown after pausing",
            "Plays in portrait or landscape and pauses itself when you switch tabs",
            "Sound, music and vibration settings, with progress saved on your device"]),
dict(slug="kedim-therapist", name="Kedim Therapist", genre="Casual", color="#f97316",
  tagline="A cozy, funny therapy office run by a cat: help 12 silly animal patients feel better.",
  about=["Kedim Therapist is a cozy comedy game for phones and desktop browsers. You play as Dr. Kedim, a ginger tabby therapist with a red scarf, a dry wit, a Ph.D. in Napping and a habit of knocking things off his desk. Silly animal patients visit his office with funny problems, and your replies decide how the session goes.",
         "There are 36 story sessions with 12 patients, including a dog terrified of the mailman, a goldfish with a three-second memory, a ghost afraid of the dark and a dragon with anger issues. Each patient comes back for a three-part story and graduates with a celebration. Between sessions you can decorate the office, dress up Kedim, read his patient notebook, and take on endless walk-ins and a daily patient. The writing is kind and family-friendly, with the occasional gentle mental-health tip."],
  how=["Tap the dialogue box to read the patient's lines. When it is your turn, pick a reply marked Kind, Funny or Wise.",
       "Good replies raise the mood meter at the top. Silly ones cause comic disasters (feathers, flames, fleeing patients) and lower it.",
       "Each session includes a therapy mini-game: Breathe With Me, Untangle Thoughts, Feelings Match, Worry Jar, Ink Blot Test, Purr Therapy or Whack-a-Thought. A better score gives a bigger mood boost.",
       "The final mood sets the star rating. Two or more stars moves the story forward, and each review earns coins.",
       "Stuck? Tap the Insight Nap button: Kedim naps and highlights the best reply.",
       "Spend coins in the Shop on office decor, outfits, fur colors and upgrades. Cozy decor makes patients arrive in a better mood. After the first two sessions the Walk-in Clinic opens, with random patients and a double-coin daily patient."],
  controls=[("Advance dialogue","Tap the dialogue box","Space / Enter"),("Choose a reply","Tap a reply","1, 2 or 3"),("Mini-games","Tap, drag or hold (shown on each intro card)","Mouse"),("Pet Kedim / knock items over","Tap Kedim or the desk items","Mouse"),("Pause","II button","P / Esc")],
  features=["36 story sessions with 12 animal patients, follow-up stories and graduation celebrations",
            "Branching Kind, Funny and Wise replies with comic results for the wrong ones",
            "7 therapy mini-games",
            "Shop with 30 office decorations, 21 Kedim outfits, 9 fur colors and 5 upgrades",
            "Kedim's Notebook of patient files, a weekly appointment calendar and 26 achievements",
            "Endless walk-in clinic and a daily patient with streaks",
            "Typewriter speech bubbles with animal babble voices, and lo-fi music and sound effects made with WebAudio",
            "Plays in portrait or landscape, pauses when you switch tabs, and saves progress on your device"]),
]
# ---------------------------------------------------------------- layout
CSS = """@font-face{font-family:"Zaib Display";src:url(/fonts/lilita-subset.woff) format("woff");font-display:swap}
:root{--bg:#0b0820;--line:rgba(255,255,255,.12);--txt:#f4f1ff;--mut:#b7b0d8;--a1:#a855f7;--a2:#22d3ee;--a3:#f472b6;
--display:"Zaib Display","Arial Rounded MT Bold","Trebuchet MS",system-ui,sans-serif}
*{box-sizing:border-box;margin:0;padding:0}html{-webkit-text-size-adjust:100%}
body{min-height:100vh;color:var(--txt);font:16px/1.6 system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
background:radial-gradient(120% 60% at 50% -10%,#24124d 0%,#0b0820 55%,#06040f 100%) fixed,var(--bg)}
a{color:#c4b5fd}a:hover{color:#67e8f9}
.wrap{max-width:860px;margin:0 auto;padding:max(18px,env(safe-area-inset-top)) max(16px,env(safe-area-inset-right)) 28px max(16px,env(safe-area-inset-left))}
.top{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:10px;padding:6px 0 18px}
.logo{font-family:var(--display);font-size:26px;text-decoration:none;color:#fff;text-shadow:0 2px 0 #4c1d95,0 0 18px rgba(168,85,247,.6)}
.top nav{display:flex;flex-wrap:wrap;gap:6px}
.top nav a{text-decoration:none;color:#d9ccff;font-size:14px;font-weight:600;padding:6px 12px;border-radius:999px;border:1px solid var(--line);background:rgba(255,255,255,.05)}
.top nav a:hover{border-color:rgba(168,85,247,.6);color:#fff}
.panel{border-radius:22px;padding:clamp(18px,4vw,34px);background:linear-gradient(180deg,rgba(255,255,255,.08),rgba(255,255,255,.03));
border:1px solid var(--line);box-shadow:0 10px 30px rgba(0,0,0,.45),inset 0 1px 0 rgba(255,255,255,.12)}
h1{font-family:var(--display);font-weight:400;font-size:clamp(36px,8vw,58px);line-height:1;margin-bottom:12px;
background:linear-gradient(100deg,#fff,#e9d5ff 40%,#67e8f9 60%,#f9a8d4);-webkit-background-clip:text;background-clip:text;color:transparent}
h2{font-family:var(--display);font-weight:400;font-size:26px;letter-spacing:.01em;margin:26px 0 8px;color:#f5f0ff}
h3{font-size:17px;margin:18px 0 6px}
p,li{color:#ddd8f5}p{margin:8px 0}ul,ol{margin:8px 0 8px 22px}li{margin:4px 0}
.lead{font-size:18px;color:var(--mut)}.small{font-size:14px;color:var(--mut)}
.hero{display:block;width:100%;aspect-ratio:16/10;object-fit:cover;border-radius:16px;border:1px solid var(--line);margin:14px 0 6px;background:#140f2e}
.genre{display:inline-block;padding:4px 10px;border-radius:999px;font-size:11px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:#fff;background:var(--gc,#a855f7)}
table{width:100%;border-collapse:collapse;margin:10px 0;font-size:15px}
th,td{text-align:left;padding:9px 10px;border-bottom:1px solid var(--line);vertical-align:top}th{color:#e9d5ff;font-weight:700}
.tbl{overflow-x:auto}
.play{display:inline-flex;align-items:center;justify-content:center;gap:10px;min-height:54px;padding:0 28px;margin:14px 0 4px;border-radius:16px;text-decoration:none;
font-family:var(--display);font-size:24px;letter-spacing:.06em;color:#fff;background:linear-gradient(180deg,#c084fc 0%,#9333ea 55%,#7e22ce 100%);
box-shadow:0 6px 0 #4c1d95,0 10px 24px rgba(147,51,234,.45),inset 0 2px 0 rgba(255,255,255,.35);text-shadow:0 2px 0 rgba(59,7,100,.6)}
.play:hover{color:#fff;filter:brightness(1.1)}.play svg{width:22px;height:22px;fill:currentColor}
.cards{display:grid;gap:14px;grid-template-columns:repeat(auto-fill,minmax(min(100%,240px),1fr));margin-top:10px}
.cards a{display:block;text-decoration:none;color:var(--txt);padding:14px;border-radius:16px;border:1px solid var(--line);background:rgba(255,255,255,.04)}
.cards a:hover{border-color:rgba(168,85,247,.6)}.cards b{font-family:var(--display);font-weight:400;font-size:21px;display:block}
footer{text-align:center;color:rgba(183,176,216,.75);font-size:13px;margin-top:26px}
footer nav{display:flex;flex-wrap:wrap;justify-content:center;gap:4px 14px;margin-bottom:8px}footer a{color:#c4b5fd;text-decoration:none}
footer a:hover{text-decoration:underline}footer b{color:#e9d5ff}"""

PLAY_ICON = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 4.5v15a1 1 0 0 0 1.53.85l12-7.5a1 1 0 0 0 0-1.7l-12-7.5A1 1 0 0 0 7 4.5z"/></svg>'
FOOTER_LINKS = [("/", "Games"), ("/about/", "About"), ("/contact/", "Contact"), ("/privacy/", "Privacy Policy"), ("/terms/", "Terms of Use")]

def nav():
    return "".join(f'<a href="{u}">{t}</a>' for u, t in FOOTER_LINKS if u != "/terms/")

def footer():
    links = "".join(f'<a href="{u}">{t}</a>' for u, t in FOOTER_LINKS)
    return f'<footer><nav aria-label="Site">{links}</nav>Made with ♥ by <b>{OWNER}</b> · © {datetime.date.today().year} Games by Zaib</footer>'

def page(path, title, desc, body, og_image="/img/og.jpg"):
    url = SITE + path
    doc = f"""<!doctype html>
<html lang="en">
<head>
{GA_TAG}
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="author" content="{OWNER}">
<meta name="theme-color" content="#0b0820">
<meta name="color-scheme" content="dark">
<link rel="canonical" href="{url}">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="/img/apple-touch-icon.png">
<link rel="manifest" href="/manifest.webmanifest">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Zaib Games">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<script src="/pwa.js" defer></script>
<meta property="og:type" content="website">
<meta property="og:site_name" content="Games by Zaib">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}{og_image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{SITE}{og_image}">
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
<header class="top"><a class="logo" href="/">Games by Zaib</a><nav aria-label="Main">{nav()}</nav></header>
<main class="panel">
{body}
</main>
{footer()}
</div>
</body>
</html>
"""
    out = os.path.join(ROOT, path.strip("/"), "index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w").write(doc)

def lis(items): return "<ul>" + "".join(f"<li>{e(i)}</li>" for i in items) + "</ul>"

# ---------------------------------------------------------------- game pages
def game_page(g):
    rows = "".join(f"<tr><td>{e(a)}</td><td>{e(t)}</td><td>{e(k)}</td></tr>" for a, t, k in g["controls"])
    body = f"""<span class="genre" style="--gc:{g['color']}">{e(g['genre'])}</span>
<h1>{e(g['name'])}</h1>
<p class="lead">{e(g['tagline'])} Free to play in your browser, no download or sign-up.</p>
<a href="/{g['slug']}/"><img class="hero" src="/img/{g['slug']}.webp" alt="{e(g['name'])} gameplay screenshot" width="600" height="375"></a>
<a class="play" href="/{g['slug']}/">{PLAY_ICON}PLAY {e(g['name'].upper())}</a>
<h2>About the game</h2>
{''.join(f'<p>{e(p)}</p>' for p in g['about'])}
<h2>How to play</h2>
<ol>{''.join(f'<li>{e(s)}</li>' for s in g['how'])}</ol>
<h2>Controls</h2>
<div class="tbl"><table><thead><tr><th>Action</th><th>Touch</th><th>Keyboard / mouse</th></tr></thead><tbody>{rows}</tbody></table></div>
<h2>Features</h2>
{lis(g['features'])}
<h2>Good to know</h2>
<p>{e(g['name'])} runs on phones, tablets and computers in any modern browser. It is a single web page with no plug-ins. Your progress (levels, coins, unlocks and settings) is saved only in your browser's local storage on this device. Clearing your browser data resets it. See our <a href="/privacy/">Privacy Policy</a>.</p>
<p>{e(g['name'])} was designed and made by {OWNER}. <a href="/">Browse all games</a> or <a href="/contact/">send feedback</a>.</p>
<a class="play" href="/{g['slug']}/">{PLAY_ICON}PLAY NOW</a>"""
    page(f"/games/{g['slug']}/", f"{g['name']}: How to Play, Controls & Features | Games by Zaib",
         f"{g['name']} by Zaib: {g['tagline']} How to play, controls and features. Free in your browser, no download.", body,
         og_image=f"/img/{g['slug']}.webp")

def games_index():
    cards = "".join(f'<a href="/games/{g["slug"]}/"><b>{e(g["name"])}</b><span class="small">{e(g["tagline"])}</span></a>' for g in GAME_INFO)
    body = f"""<h1>Game guides</h1><p class="lead">How to play, controls and features for every game on Games by Zaib.</p>
<div class="cards">{cards}</div>"""
    page("/games/", "Game Guides: How to Play | Games by Zaib", "How to play, controls and features for every free browser game by Zaib.", body)

# ---------------------------------------------------------------- static pages
def about():
    items = "".join(f'<li><a href="/games/{g["slug"]}/">{e(g["name"])}</a>: {e(g["tagline"])}</li>' for g in GAME_INFO)
    body = f"""<h1>About Games by Zaib</h1>
<p class="lead">Games by Zaib is a small independent collection of free arcade games that you can play instantly in your web browser, made with phones in mind.</p>
<h2>About the studio</h2>
<p>Games by Zaib is an independent studio making free, colourful browser games. The focus is on quick, fun games that are easy to pick up on a phone, with enough depth (levels, upgrades and unlocks) to keep you coming back.</p>
<h2>How the games work</h2>
<p>Each game is a single web page written in HTML5 and JavaScript. There is nothing to download or install and no account to create. The games work on phones, tablets and computers, with touch, keyboard and mouse controls. Music and sound effects are generated in the browser, and your progress is stored locally on your device.</p>
<p>The characters, art, music and code in these games are original work. Teams, clubs and rivals that appear in the sports games are fictional.</p>
<h2>The games</h2>
<ul>{items}</ul>
<p>New games are added regularly. Check the <a href="/">home page</a> for the latest.</p>
<h2>Free to play</h2>
<p>All games are free. To help cover the cost of making new games, this site may show advertising in the future, as described in the <a href="/privacy/">Privacy Policy</a>.</p>
<h2>Get in touch</h2>
<p>Found a bug, have an idea, or want to say hi? Visit the <a href="/contact/">contact page</a> or email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>"""
    page("/about/", "About | Games by Zaib", f"Games by Zaib is a collection of free browser arcade games made by independent studio Games by Zaib.", body)

def contact():
    body = f"""<h1>Contact</h1>
<p class="lead">I'd love to hear from you, whether it's feedback, a bug report, a game idea or a business enquiry.</p>
<h2>Email</h2>
<p><a class="play" href="mailto:{EMAIL}?subject=Games%20by%20Zaib">✉ {EMAIL}</a></p>
<p>I usually reply within a few days.</p>
<h2>Reporting a bug</h2>
<p>To help me fix a problem quickly, please include:</p>
<ul><li>the name of the game and what you were doing when the problem happened</li>
<li>your device and browser (for example "Android phone, Chrome" or "iPhone, Safari")</li>
<li>a screenshot, if you can</li></ul>
<h2>Privacy requests</h2>
<p>For any question about your privacy or the data described in our <a href="/privacy/">Privacy Policy</a>, email the same address with "Privacy" in the subject line.</p>
<p class="small">Games by Zaib is an independent game studio.</p>"""
    page("/contact/", "Contact | Games by Zaib", f"Contact Games by Zaib: feedback, bug reports and enquiries.", body)

def privacy():
    body = f"""<h1>Privacy Policy</h1>
<p class="small">Last updated: {UPDATED}</p>
<p>This Privacy Policy explains how Games by Zaib (<a href="{SITE}/">zaibgames.com</a>, "the site", "we", "us") handles information when you visit the site and play its games. By using the site you agree to this policy.</p>

<h2>Summary</h2>
<ul><li>You can play every game without an account. We do not ask for your name, email address or any other account details.</li>
<li>Game progress and settings are saved only in your browser's local storage on your device.</li>
<li>We use Google Analytics to measure visits to the site (see <a href="#analytics">Analytics</a>).</li>
<li>Third-party vendors, including Google, may use cookies to show ads based on your visits to this and other websites. You can opt out of personalised advertising (see below).</li></ul>

<h2>Information we collect</h2>
<h3>No account data</h3>
<p>The site has no registration, login, user profiles, chat or comment features. We do not collect your name, email address, phone number, payment details or other account data while you browse or play.</p>
<h3>Game saves in local storage</h3>
<p>Our games use your browser's <strong>localStorage</strong> to remember things like unlocked levels, coins, high scores, purchased in-game items (bought with in-game coins only) and settings such as sound and controls. This data stays on your device. It is not sent to us and we cannot see it. You can delete it at any time with the game's "Reset progress" option or by clearing your browser's site data for zaibgames.com.</p>
<h3>Information you send us</h3>
<p>If you email us, we receive your email address and whatever you write. We use it only to reply to you and do not share it or add you to any mailing list.</p>
<h3>Hosting and server logs</h3>
<p>The site is hosted on GitHub Pages (GitHub, Inc.). Like any web host, GitHub may process technical information such as your IP address and browser type to deliver the pages and keep the service secure. See the <a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement" rel="noopener">GitHub Privacy Statement</a>.</p>
<h3 id="analytics">Analytics</h3>
<p>The site uses Google Analytics to measure visits, such as how many people visit, which pages and games they open and roughly where they come from. Google Analytics uses cookies and similar technologies, and the information it collects is processed by Google. See <a href="https://policies.google.com/technologies/partner-sites" rel="noopener">How Google uses information from sites or apps that use our services</a>. You can opt out of Google Analytics by installing the <a href="https://tools.google.com/dlpage/gaoptout" rel="noopener">Google Analytics Opt-out Browser Add-on</a>.</p>

<h2>Advertising and cookies</h2>
<p>To keep the games free, we use or may use Google AdSense and other third-party advertising vendors to display ads on the site.</p>
<ul>
<li>Third-party vendors, including Google, use cookies to serve ads based on a user's prior visits to this website or other websites.</li>
<li>Google's use of advertising cookies enables it and its partners to serve ads to our users based on their visits to this site and/or other sites on the Internet.</li>
<li>You may opt out of personalised advertising by visiting <a href="https://adssettings.google.com" rel="noopener">Google Ads Settings</a> (adssettings.google.com).</li>
<li>You can also opt out of some third-party vendors' use of cookies for personalised advertising by visiting <a href="https://www.aboutads.info" rel="noopener">www.aboutads.info</a> (and <a href="https://www.youronlinechoices.eu" rel="noopener">www.youronlinechoices.eu</a> in Europe).</li>
</ul>
<p>Cookies are small text files stored by your browser. Ad vendors may also use similar technologies such as web beacons, device identifiers and local storage to measure ads and prevent fraud. To learn more about how Google uses information from sites that use its services, see <a href="https://policies.google.com/technologies/partner-sites" rel="noopener">How Google uses information from sites or apps that use our services</a> and <a href="https://policies.google.com/technologies/ads" rel="noopener">How Google uses cookies in advertising</a>.</p>
<p>If you do not opt out, you may still see ads, but they will be less relevant to you. You can also block or delete cookies in your browser settings. The games will still work, although blocking local storage will stop your progress from being saved.</p>

<h2>Consent for visitors in the EEA, UK and Switzerland</h2>
<p>Where required by law (for example under the GDPR and UK GDPR), when ads are shown we will ask for your consent through a consent message from a Google-certified consent management platform before personalised ads or non-essential cookies are used. You can change or withdraw your choice at any time through that message. Where personalised ads are not allowed, only non-personalised or limited ads are shown.</p>

<h2>Children's privacy</h2>
<p>Our games are family-friendly and suitable for a general audience, but the site is not directed specifically at children under 13 (or the minimum age in your country). We do not knowingly collect personal information from children. Children should ask a parent or guardian before using the internet and emailing anyone, including us. If you are a parent or guardian and believe your child has sent us personal information, contact us and we will delete it.</p>

<h2>Your rights</h2>
<p>Depending on where you live, you may have rights to access, correct or delete personal data we hold about you. Since we only hold data you email to us, contact us at the address below to make a request.</p>

<h2>Third-party links</h2>
<p>The site may link to other websites. We are not responsible for their content or privacy practices, so please review their privacy policies.</p>

<h2>Changes to this policy</h2>
<p>We may update this policy, for example when we start showing ads or add new features. The "Last updated" date at the top shows when it last changed.</p>

<h2>Contact</h2>
<p>Questions about this policy? Email <a href="mailto:{EMAIL}">{EMAIL}</a> or visit the <a href="/contact/">contact page</a>.<br>Games by Zaib</p>"""
    page("/privacy/", "Privacy Policy | Games by Zaib", "Privacy Policy for Games by Zaib: local game saves, advertising cookies (including Google), opt-out links and contact details.", body)

def terms():
    body = f"""<h1>Terms of Use</h1>
<p class="small">Last updated: {UPDATED}</p>
<p>These terms apply to your use of Games by Zaib at zaibgames.com ("the site"). By using the site you agree to them. If you do not agree, please do not use the site.</p>
<h2>Using the games</h2>
<p>The games are free to play for personal, non-commercial entertainment. You agree not to:</p>
<ul><li>copy, modify, redistribute, resell or re-host the games or their code, art or music without written permission</li>
<li>embed the games on other websites in a way that presents them as your own or removes credits</li>
<li>attempt to disrupt, overload or attack the site, or interfere with any advertising shown on it, including by generating invalid ad clicks or impressions</li>
<li>use the site in any way that breaks the law</li></ul>
<h2>Intellectual property</h2>
<p>The games, including their code, characters, artwork, music, sound effects and text, are the work of Games by Zaib and are protected by copyright. All rights are reserved except where stated. Any teams, clubs, players or rivals in the games are fictional. Some text fonts are used under their open licences.</p>
<h2>In-game items</h2>
<p>Coins, upgrades and other in-game items are earned through play only. They have no real-world monetary value, cannot be bought, sold or exchanged, and may be lost if your browser data is cleared.</p>
<h2>Advertising</h2>
<p>The site may show ads from third parties such as Google. We are not responsible for the content of ads or for third-party websites they link to. See our <a href="/privacy/">Privacy Policy</a> for how advertising cookies are used.</p>
<h2>No warranty</h2>
<p>The site and games are provided "as is" and "as available", without warranties of any kind. We do not guarantee that they will always be available, error-free or compatible with your device, or that saved progress will be kept.</p>
<h2>Limitation of liability</h2>
<p>To the fullest extent permitted by law, Games by Zaib is not liable for any indirect, incidental or consequential loss or damage arising from your use of, or inability to use, the site or games.</p>
<h2>Health note</h2>
<p>Take regular breaks while playing. Some games contain flashing effects and screen shake; most games let you reduce effects in their settings.</p>
<h2>Changes</h2>
<p>We may update these terms or change, add or remove games at any time. Continued use of the site after a change means you accept the updated terms.</p>
<h2>Governing law</h2>
<p>These terms are governed by the laws of Malaysia.</p>
<h2>Contact</h2>
<p>Email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>"""
    page("/terms/", "Terms of Use | Games by Zaib", "Terms of Use for Games by Zaib, free browser games by Zaib.", body)

# ---------------------------------------------------------------- sitemap/robots
def game_paths():
    """Game paths from the GAMES array in index.template.html (plus GAME_INFO)."""
    src = open(os.path.join(ROOT, "index.template.html")).read()
    m = re.search(r"const GAMES = \[(.*?)\n\];", src, re.S)
    paths = []
    for u in re.findall(r'url:\s*"([^"]+)"', m.group(1) if m else ""):
        u = re.sub(r"^https?://(wahidzeb\.github\.io|zaibgames\.com)", "", u)
        if u.startswith("/"):
            paths.append(u if u.endswith("/") else u + "/")
    for g in GAME_INFO:
        if f"/{g['slug']}/" not in paths: paths.append(f"/{g['slug']}/")
    return paths

def sitemap():
    pages = [("/", "1.0"), ("/games/", "0.6"), ("/about/", "0.5"), ("/contact/", "0.4"), ("/privacy/", "0.3"), ("/terms/", "0.3")]
    pages += [(f"/games/{g['slug']}/", "0.7") for g in GAME_INFO]
    pages += [(p, "0.9") for p in game_paths()]
    xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    xml += [f"  <url><loc>{SITE}{p}</loc><lastmod>{LASTMOD}</lastmod><priority>{pr}</priority></url>" for p, pr in pages]
    xml.append("</urlset>")
    open(os.path.join(ROOT, "sitemap.xml"), "w").write("\n".join(xml) + "\n")
    open(os.path.join(ROOT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")

if __name__ == "__main__":
    for g in GAME_INFO: game_page(g)
    games_index(); about(); contact(); privacy(); terms(); sitemap()
    print("info pages, sitemap.xml and robots.txt built")
