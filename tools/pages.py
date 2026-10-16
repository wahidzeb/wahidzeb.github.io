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
# cache-bust query for replaced thumbnails (bump when an img/<slug>.webp changes)
IMG_V = {'kedim-therapist': '?v=3', 'baby-kedim': '?v=1'}

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
  tagline="Untangle a packed parking lot and get every passenger onto the vehicle that matches their colour.",
  about=["Bus Bonanza is a traffic-jam passenger puzzle for phones and desktop browsers. A long, winding queue of passengers waits in colour runs. Below it, a packed lot holds glossy cars, vans and buses parked at all kinds of angles, and each one has an arrow on its roof. Tap a vehicle to drive it out, park it, and watch the matching passengers walk over and climb aboard.",
         "Hundreds of levels are generated by the game, and every one is solvable by design. A solver bot checks levels automatically, and the difficulty climbs smoothly with a few breather levels mixed in. Every five levels the scenery changes between beach, city, snow and night. You earn coins by winning levels and spend them on power-ups and extra parking spots."],
  how=["Tap a vehicle to drive it out of the lot. Vehicles only drive forward, the way their arrow points. If another vehicle is in the way, it bumps and shakes and stays put.",
       "A vehicle that gets out drives around the ring road into a free parking spot. Passengers at the front of the queue board a parked vehicle of their colour. Cars seat 4, vans 6 and buses 10. A full vehicle leaves and frees its spot.",
       "You run out of space when every spot is taken and the next passenger matches none of the parked vehicles. Dig out the colour the queue needs next before you fill your spots with the wrong ones.",
       "Power-ups: VIP flies any vehicle, even a blocked one, to the VIP spot. Arrange sorts the queue. Jumble reshuffles the colours of the vehicles in the lot. Undo takes back a move. The three locked spots can be opened with coins for one level.",
       "If you run out of space, you can undo, continue for coins or retry. Finishing without power-ups earns 3 stars."],
  controls=[("Drive a vehicle","Tap it","Mouse click"),("Power-ups","Buttons along the bottom (lower left in landscape)","U or Z for Undo"),("Pause","II button","Esc")],
  features=["Hundreds of procedurally generated levels, each solvable by design and checked by a solver bot, plus level select with stars",
            "Cars, vans and buses (4, 6 and 10 seats) at free angles, each with a direction arrow",
            "A long, winding passenger queue in colour runs, with cute bobbing passengers who walk over to board",
            "A parking row with a VIP spot and three spots you can unlock",
            "VIP, Arrange and Jumble power-ups with count badges, plus Undo",
            "Beach, city, snow and night themes that change every five levels",
            "Glossy pseudo-3D vehicles with soft shadows, bump-and-shake collisions, particles, and music and sound effects made in code",
            "Portrait, landscape and desktop layouts, with progress saved on your device"]),
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
dict(slug="baby-kedim", name="Baby Kedim", genre="Casual", color="#ec4899",
  tagline="A cozy virtual pet game: raise baby Kedim the black cat and watch him grow up.",
  about=["Baby Kedim is a virtual pet game for phones and desktop browsers. Kedim is a cute baby black cat who needs food, fun, a bath and sleep. Rings on the room buttons show how he feels, and caring for him keeps him happy.",
         "A happy Kedim grows from Kitten to Kid, Teen and Adult. The mini-game he plays most decides whether he grows up as Therapist Kedim, Snack-Swing Kedim or Adventurer Kedim. Kedim never gets hurt: if you forget him he just gets sulky or messy and stops growing until you care for him again."],
  how=["Kitchen: drag a food to Kedim's mouth.",
       "Bathroom: rub the soap all over him, then tap Rinse.",
       "Bedroom: tap Lights off for a nap. He wakes up when he is rested.",
       "Playroom: pet him for purrs, throw the ball, talk to him and play mini-games for coins.",
       "Spend coins on hats, collars, glasses and decor for his home.",
       "Keep all his needs up so he keeps growing toward his grown-up form."],
  controls=[("Feed","Drag food to Kedim's mouth","Mouse drag"),("Bath","Rub the soap over Kedim, then tap Rinse","Mouse drag"),("Pet / play","Tap or stroke Kedim, tap the ball","Mouse"),("Pause","II button","Esc")],
  features=["Four rooms: Kitchen, Bathroom, Bedroom and Playroom",
            "6 mini-games: Snack Swing, Fish Catch, Feel-Good Clinic, Yarn Pop, Kedim Dash and Treasure Dive",
            "Grows from Kitten to Kid, Teen and Adult, with 3 grown-up forms",
            "Dress-up items like hats, bows, scarves and glasses, plus home decor and themes",
            "Gentle care: Kedim never gets hurt, he only gets sulky when you forget him",
            "Sound and music settings, with progress saved on your device"]),
dict(slug="block-glide", name="Block Glide", genre="Puzzle", color="#8b5cf6",
  tagline="Slide soft clay blocks through matching color gates and clear the board.",
  about=["Block Glide is a cozy color block sliding puzzle for phones and desktop browsers. The board is packed with chunky clay blocks in tetromino-like shapes, and the walls around it have colored gates. Drag a block to a gate of its own color and it slides out of the board.",
         "There are 160 levels across 8 themed chapters. A solver bot has checked that every one can be cleared within its timer or move limit. There is also a fresh Daily Challenge each day with a streak counter. Spend the coins you win on block skins, color themes and boosters."],
  how=["Drag a block to slide it around the grid. Blocks can't pass through other blocks or walls, so you often have to move a few out of the way first.",
       "When a block touches a gate of the same color and fits inside the gate's width, it whooshes out. Clear several in a row for a combo.",
       "Clear every block to win. Most levels have a timer, which starts on your first move, or a move counter. Finishing with plenty left earns 3 stars.",
       "Watch for the new mechanics: arrow blocks that only slide one way, ice blocks that thaw as you clear others, two-color layered blocks, locks that open when the key block leaves, board stars worth coins, swirl blocks you tap to rotate, gates that change color, and bombs that count down with each move.",
       "Boosters: Hammer smashes one block, Freeze stops the timer for 12 seconds, Vacuum removes every block of one color, Undo takes back a move, and Extra adds 5 moves or 15 seconds."],
  controls=[("Move a block","Drag it","Mouse drag"),("Rotate a swirl block","Tap it","Click"),("Boosters","Buttons along the bottom (right side in landscape)","1-5, U or Z for Undo"),("Pause / restart","II button","P / Esc, R")],
  features=["160 levels in 8 chapters, each checked by a solver bot, with a level map and up to 3 stars per level",
            "Arrow, ice, layered, locked, rotating and bomb blocks, shifting gates and collectible stars",
            "A Daily Challenge generated in your browser, a streak counter, a 7-day gift calendar and 14 achievements",
            "5 boosters: Hammer, Freeze, Vacuum, Undo and Extra moves/time",
            "Shop with 6 block skins (including Block Buddies with blinking faces) and 6 color themes",
            "Soft 3D clay blocks, snappy dragging with a ghost preview, particle exits, combos, confetti, and music and sound effects made in code",
            "Tutorial hand hints, color-blind symbols, sound, music, vibration and graphics settings, with progress saved on your device"]),
dict(slug="horizon-pilot", name="Horizon Pilot", genre="Simulation", color="#38bdf8",
  tagline="A 3D flight game: fly 7 planes through 25 missions over an island world.",
  about=["Horizon Pilot is a 3D flying game for phones and desktop browsers. You start in a small trainer at Zaib International and explore an island with mountains, valleys, lakes, a coastline, cities and 7 airports, under day, dusk, night and storm skies.",
         "The career has 25 missions: ring courses, landings and crosswind landings, splashdowns, cargo drops, firefighting, sea rescues, air shows, an engine failure, a jammed landing gear and jet races. Earn coins and XP to rank up, buy new planes, upgrade engines and paint them in new liveries. Free Flight hides 30 golden stars, and there is a new Daily Challenge every day."],
  how=["Push the throttle (right slider) up, roll down the runway and gently pull back on the stick to take off.",
       "Drag the stick (left side) to bank and climb or dive. Let go and the assisted controls level the wings for you. Hold the stick all the way to one side for a full roll, or all the way up or down for a loop.",
       "Follow the objective at the top of the screen and the green markers: fly through rings, reach waypoints or find the target.",
       "To land, line up with the runway, lower the GEAR and FLAPS, slow down and follow the glide path dots. Touch down gently and hold BRAKE to stop.",
       "Switch cameras with CAM: chase, cockpit with instruments, or cinematic. AUTO lets the autopilot fly when you need a break (it caps that mission at 2 stars)."],
  controls=[("Steer / pitch","Virtual stick on the left, or tilt your phone","Arrows / WASD"),("Throttle","Slider on the right","Shift / Ctrl, R / F, 1-0"),
            ("Gear / flaps","GEAR and FLAPS buttons","G / V"),("Brake","Hold BRAKE","B"),("Rudder","Automatic in assisted mode","Q / E"),
            ("Action (drop, water, smoke)","Action button","Space"),("Camera","CAM button","C"),("Pause","II button","P / Esc")],
  features=["Real 3D WebGL graphics: terrain, ocean, clouds, cities, airports with runway lights and PAPI, and day, dusk, night and storm skies",
            "7 aircraft: Sparrow trainer, Bumblebee biplane, Pelican floatplane, Hornet aerobatic, Falcon business jet, Atlas airliner and Viper fighter",
            "An arcade-sim flight model with assisted controls, stalls, flaps, gear, wind and turbulence",
            "25 career missions with briefings, maps and up to 3 stars each",
            "Free Flight with 30 golden stars, plus a Daily Challenge with a streak bonus",
            "Upgrades, liveries, smoke colours, coins, XP and ranks",
            "Chase, cockpit and cinematic cameras, glide-path guidance, and an interactive tutorial",
            "Sound made in code, automatic graphics quality, and progress saved on your device"]),
dict(slug="haulway-heroes", name="Haulway Heroes", genre="Simulation", color="#f59e0b",
  tagline="A 3D trucking career: haul tricky cargo across highways, hairpins and storms, then back into the dock.",
  about=["Haulway Heroes is a 3D truck-driving game for phones and desktop browsers. You start with a small cab-over truck in Port Bayu and take contracts from the job board: general goods, electronics, fragile glass, livestock, fuel, logs, new cars, and oversized loads that follow an escort car.",
         "Each route is a real 3D road through highways, cities with traffic lights, mountain hairpins, deserts, snowy passes, fog and rainy nights, with a full day and night cycle. Along the way you meet AI traffic, gas stations, weigh stations, toll gates and speed cameras. At the end you reverse the articulated trailer into the loading bay. Earn money and XP to buy 6 trucks, including the hand-painted Rangeela art truck, plus trailers, upgrades, paint, decals, lights and horns."],
  how=["Pick a contract on the job board. Harder cargo pays more: glass and cattle hate rough driving, and fuel and oversized loads are heavy.",
       "Press GAS to drive and BRAKE to slow down. Steer with the on-screen wheel, by tilting your phone, or with the arrow buttons (choose in Settings). The gearbox is automatic unless you pick manual.",
       "Follow the blue GPS line on the minimap. Keep to the speed limit, stop at red lights, slow down for toll gates and pull into weigh stations when asked. Refuel at gas stations before the tank runs dry.",
       "Long trailers cut corners, so take hairpins wide and slowly. Turning too sharply in reverse can jackknife the trailer.",
       "At the depot, stop, tap D to switch to R, and back the trailer into the glowing bay. The dock panel shows your alignment. Tap Auto-park if you want the yard crew to do it for a smaller bonus.",
       "You earn stars and pay for time, cargo damage, comfort and clean driving. Spend it in the Garage and Shop, try Free Roam, the Daily Challenge and 8 parking challenges, or take the guided first delivery."],
  controls=[("Gas / brake","GAS and BRAKE pedals","Up / Down or W / S"),("Steer","Steering wheel, tilt, or arrow buttons","Left / Right or A / D"),
            ("Drive / reverse","D / R button","R"),("Gears (manual)","+ and - buttons","Z / X"),("Handbrake","P button","Space"),
            ("Horn / indicators / lights","Horn, arrow and light buttons","H, Q / E, L"),("Cruise control","CC button","K"),("Camera","Camera button","C"),("Pause","II button","P / Esc")],
  features=["Real 3D WebGL graphics: trucks, articulated trailers, terrain, cities, mountains, deserts and snow, with a day and night cycle, headlights, rain with wipers, fog and snow",
            "Truck physics with trailer off-tracking, jackknifing, air brakes, damage and fuel",
            "8 cargo types, including fragile glass, livestock, fuel tankers, logs, car carriers and escorted oversized loads",
            "AI traffic, traffic lights, gas stations, weigh stations, toll gates and speed cameras",
            "Reverse docking with an alignment guide and optional auto-park",
            "6 trucks and several trailers, upgrades, paint, decals, lights and horns",
            "Career with XP, levels and a city map, plus Free Roam, a Daily Challenge, 8 parking challenges and a guided tutorial",
            "Chase, cab and top cameras, a rear-view mirror, minimap with GPS, and engine, horn, rain and radio sounds made in code"]),
dict(slug="chai-tycoon", name="Chai Tycoon", genre="Idle", color="#ea580c",
  tagline="Grow a tiny roadside chai stall into a chai empire of dhabas, cafés and a delivery fleet.",
  about=["Chai Tycoon is an idle tycoon game for phones and desktop browsers with a South Asian street-food feel. You start with a single roadside chai stall. Customers in kurtas, topis, dupattas and turbans line up for steaming kulhads, and the chaiwala pours each one from a height.",
         "Grow from the stall into 8 businesses: Paratha Tawa, Samosa Counter, Lassi Bar, Highway Dhaba, City Cafés, Delivery Fleet and Chai Export Co. Each one opens up along the bazaar as you buy it, with rickshaws, delivery bikes and a truck-art export truck on the road and a day and night cycle overhead. Hire managers to automate everything, earn while you are away, and Franchise for Stars that make every new run faster."],
  how=["Tap the street scene to serve chai. Every tap pays you and starts any shop that is waiting for you.",
       "Buy more of each shop with the BUY button (x1, x10, x100, NEXT milestone or MAX). Owning 25, 50, 100, 200, 300 and 400 of a shop doubles its speed, and getting every shop to 10, 25, 50 and more doubles all profits.",
       "Hire a manager for each shop in the Managers tab so it keeps running by itself. Shops with a manager also earn while you are away, up to an offline cap (2 hours at first), and a welcome-back summary shows what they made.",
       "Buy upgrades to multiply profits. Watch for timed events: the Cricket Match Rush (all profits x3), the Eid Special, Monsoon Pakora Time and the Wedding Order tap challenge. Catch the golden kulhad when it floats by.",
       "When your Franchise tab shows enough Stars, franchise: you start over, but each unspent Star adds 2% profit forever. You can also spend Stars on perks like Family Recipe (profits x2), Long Naps (longer offline time) and Head Start.",
       "Claim the daily reward to build a 7-day streak that ends with a permanent Golden Kettle bonus, and collect 54 achievements for +1% profit each."],
  controls=[("Serve chai / catch golden kulhad","Tap the street","Space / Enter"),("Buy shops","BUY buttons","1-8, X changes the amount"),("Hire managers","Managers tab","Shift + 1-8"),("Switch tabs","Bottom tabs (side in landscape)","Tab"),("Pause","II button","P / Esc")],
  features=["8 businesses from a roadside chai stall to a chai export company, each with its own speed, profit and cost curve",
            "Managers that automate shops, plus offline earnings with a cap and a welcome-back summary",
            "Speed and profit milestones, empire milestones and 106 upgrades",
            "Franchise prestige with Stars and 7 permanent perks",
            "Timed events: Cricket Match Rush, Eid Special, Monsoon Pakora Time and the Wedding Order, plus golden kulhads",
            "7-day daily reward streak, 54 achievements, rank titles and big-number formatting (K, M, B, T, aa, ab...)",
            "Animated street-food scene with walking customers, steam, truck art, rickshaws, delivery bikes and a day and night cycle",
            "Tabla and sitar-style music and sound effects made in code, with progress saved on your device"]),
dict(slug="noodle-clash", name="Noodle Clash", genre="Arcade", color="#ff4fa3",
  tagline="A snake battle arena: eat glowing orbs, boost, and make clever AI snakes crash into you.",
  about=["Noodle Clash is a snake battle arena game for phones and desktop browsers. You start as a short noodle in a neon arena full of glowing orbs. Eat them to grow longer and thicker, climb the live leaderboard and take the crown. It runs completely offline against AI snakes, so there is no waiting for a server.",
         "The AI snakes have real personalities. Hunters chase heads and cut across their path, cowards flee from anything bigger, encirclers coil around smaller snakes and tighten the loop, and grazers chase the richest food. Play the endless Classic arena, a 3-minute Rush with double orbs, a Battle Royale where the zone shrinks until one snake is left, or a split-screen Duo where two players share one phone in landscape."],
  how=["Steer your snake. On a phone, drag anywhere to use the floating joystick, or switch to Follow finger in Settings. On a computer, point with the mouse or use the arrow keys (or A and D).",
       "Eat the glowing orbs to grow. The big, bright orbs come from snakes that crashed, so they are worth a lot.",
       "Hold the lightning button, tap with a second finger, or hold the mouse button or Space to boost. Boosting is fast but burns length and leaves a trail of orbs behind you.",
       "Any snake whose head touches another snake's body explodes. Boost in front of rivals so they run into you, coil around smaller snakes to trap them, and never touch a body with your own head. The red border is deadly too.",
       "In Battle Royale, stay inside the purple zone. Outside it you shrink quickly. In Rush and Duo you respawn, and whoever is longest when the timer ends wins.",
       "Earn coins from length, clashes, daily missions and achievements, and spend them on skins and patterns in the Shop."],
  controls=[("Steer","Floating joystick or follow finger","Mouse, Left / Right or A / D"),("Boost","Lightning button or second finger","Mouse button, Space, Up or W"),
            ("Pause","II button","P / Esc"),("Duo player 1","Left half joystick + boost","A / D, W or Shift"),("Duo player 2","Right half joystick + boost","Left / Right, Up or Enter")],
  features=["4 modes: endless Classic, 3-minute Rush, Battle Royale with a shrinking zone, and a 2-player split-screen Duo",
            "Smart AI snakes: hunters, cowards, encirclers and grazers with different skill levels and obstacle avoidance",
            "Smooth, curvy snakes with boost trails, glowing orbs and explosive crashes",
            "Live leaderboard with a crown for the leader, plus a minimap",
            "18 skins and 8 patterns, including animated Neon Pulse, bought with coins",
            "3 daily missions, 19 achievements and an interactive tutorial",
            "Many snakes on screen at a smooth frame rate thanks to spatial hashing and automatic graphics quality",
            "Music and sound effects made in code, and progress saved on your device"]),
dict(slug="gobble-hole", name="Gobble Hole", genre="Arcade", color="#7b3cff",
  tagline="A 3D city eater: drag a black hole around and swallow everything smaller than you, up to whole skyscrapers.",
  about=["Gobble Hole is a 3D arcade game for phones and desktop browsers. You control a hungry black hole in a colourful low-poly world. Anything smaller than the hole tips over and falls in: traffic cones, bins, benches, people, lamp posts, trees, cars and buses. Every bite makes you bigger, until you can swallow houses, shops and whole skyscrapers, which sink into the ground with a rumble.",
         "Play on four maps: Sunny City with roads, parks and parking lots, Coco Beach with umbrellas, boats and hotels, Hayday Farm with fields, animal pens, barns and a windmill, and Orbit Station with rovers, domes and a rocket. Classic mode gives you 2 minutes against 7 AI holes that grow, hunt and run away. Solo mode asks you to eat the whole map for three stars, and in Battle the safe zone shrinks until only one hole is left."],
  how=["Drag anywhere on the screen to move your hole, like a floating joystick. On a computer, use WASD or the arrow keys, or drag with the mouse.",
       "Anything smaller than your hole falls in when you move over it. Start with cones, people and bins, then move on to benches, trees and cars as you grow.",
       "The bar under your score fills as you grow. Each new size lets you swallow bigger things: buses, then houses, then towers.",
       "In Classic, a hole that is clearly bigger than another can swallow it. Chase smaller holes for big bonuses and keep away from bigger ones. If you are eaten, you respawn after a moment with half your size.",
       "In Solo there are no rivals. Clear the map before the 2 minutes run out: 50% earns one star, 80% two and 100% three. Arrows point to the last few objects.",
       "In Battle there are no respawns. Stay inside the safe zone, because holes outside it shrink and disappear. Be the last hole standing, or the biggest when time runs out.",
       "Earn coins every round and spend them on hole skins, trails and new maps. Finish the 3 daily missions and unlock achievements for bonus coins."],
  controls=[("Move","Drag anywhere (floating joystick)","WASD / arrow keys, or drag with the mouse"),("Pause","II button","P / Esc")],
  features=["Satisfying eating physics: objects teeter on the rim, tumble in and buildings sink with a shake",
            "Classic rounds against 7 AI holes with a live leaderboard, Solo 100% challenges with stars, and Battle with a shrinking zone",
            "4 maps (city, beach, farm and space station) with around 50 kinds of objects, moving cars, buses, tractors, rovers, people and animals",
            "13 hole skins, including Rainbow, Galaxy and Royal Gold, and 9 trails such as hearts, fire and confetti",
            "3 daily missions, 16 achievements and an interactive tutorial",
            "Real 3D WebGL with instanced rendering, culling and automatic graphics quality, so it stays smooth on phones",
            "An x-ray outline that keeps your hole visible behind tall buildings",
            "Music and sound effects made in code, and progress saved on your device"]),
dict(slug="kedim-snack-swing", name="Kedim's Snack Swing", genre="Puzzle", color="#ff9d3c",
  tagline="A rope-cutting physics puzzle: cut the ropes and swing the fish treat into Kedim the cat's mouth.",
  about=["Kedim's Snack Swing is a physics puzzle game for phones and desktop browsers. Kedim, the orange cat from Kedimz Adventure and Kedim Therapist, is hungry. His fish treat hangs from ropes, and you cut them so it swings, flies and drops straight into his mouth. Kedim follows the treat with his eyes, opens his mouth wider as it gets close, chomps happily when you feed him and sulks when it falls.",
         "There are 120 levels in 6 themed snack boxes: Kitchen, Garden, Toy, Space, Magic and Spooky. New ideas arrive one at a time: bubbles, air cushions, spikes, moving pins, auto-ropes, the gravity switch, bouncy pads, portals and timed spiders. Every level has 3 stars to collect and was checked by an automated solver. There is also a daily level with a streak bonus, a shop with 9 treat skins and 11 hats, and 20 awards."],
  how=["Swipe (or drag with the mouse) across a rope to cut it. One swipe can cut several ropes, so aim carefully.",
       "Time your cuts: let the treat swing and cut at the right moment so it flies toward Kedim.",
       "Collect the 3 stars on the way. Stars unlock the next snack boxes.",
       "Bubbles lift the treat. Tap the treat to pop the bubble. Tap an air cushion to blow the treat the way it points, and tap the gravity button to flip gravity.",
       "Avoid spikes, and cut a rope before its spider crawls down to steal the treat. Portals teleport the treat but snap any ropes still attached. Green rings grab the treat with a new rope.",
       "Stuck? Use a hint to watch the full solution. You start with 3 hints and can buy more with coins you earn by finishing levels."],
  controls=[("Cut a rope","Swipe across it","Drag with the mouse, or 1-9"),("Pop the bubble","Tap the treat","Space"),("Air cushion","Tap it","Q / E"),
            ("Gravity switch","Tap it","G"),("Restart / hint","HUD buttons","R / H"),("Pause","II button","P / Esc")],
  features=["120 physics puzzles in 6 themed boxes, plus a daily level",
            "Smooth rope physics with swinging, slack and dangling cut ends",
            "10 mechanics: ropes, bubbles, air cushions, spikes, moving pins, auto-ropes, gravity switch, bouncy pads, portals and timed spiders",
            "3 stars per level, every level verified solvable by an automated solver",
            "Hints that replay the full solution",
            "Shop with treat skins and hats for Kedim, coins, and 20 awards",
            "An expressive cartoon cat: idle, hungry, happy and sad animations",
            "Music and sound effects made in code, and progress saved on your device"]),
dict(slug="fortress-frontline", name="Fortress Frontline", genre="Strategy", color="#d4a017",
  tagline="A fantasy tower defense game: build, upgrade and hold the line against goblins, flyers and bosses.",
  about=["Fortress Frontline is a tower defense game for phones and desktop browsers, inspired by Kingdom Rush. Build towers on stone spots beside winding roads and stop waves of monsters before they reach your castle gate. It has a rich top-down cartoon look with spell effects, explosions and lightning, and it plays in both portrait and landscape.",
         "There are 30 handcrafted levels across 4 worlds: Greenvale, Sandspire Dunes, Frostpeak Pass and Ashen Wastes. Every world ends with a boss: the Gorehorn Warlord, the Sandmaw Worm, Varkoth the Lich King and Infernax the Fire Drake. You earn up to 3 stars per level and spend them in a permanent upgrade tree, and endless mode tests how many waves you can survive."],
  how=["Tap an empty stone spot to open the build menu. Tap a tower once to see its stats, then tap again to build it.",
       "Archers hit ground and air, Artillery deals splash damage to ground troops, Mages pierce armour and Frost towers slow enemies.",
       "Tap a tower to upgrade it. After 3 tiers, choose 1 of 2 specialised branches, such as the Ranger Lodge or the Volley Bastion, or the Storm Spire or the Void Obelisk.",
       "Tap the skull flag (or Next Wave) to call the next wave early. You get bonus coins and shorter ability cooldowns.",
       "Use Meteor Strike to blast groups and Reinforcements to block the road with soldiers. Both recharge over time.",
       "Watch for healers, splitters, burrowers, summoners and flyers, and keep 18 or more lives for three stars."],
  controls=[("Build / select","Tap a spot or tower","Click, or 1-4 to choose"),("Upgrade / sell","Radial menu","U / Enter, S"),("Next wave","Skull flag or button","Space / N"),
            ("Meteor Strike","Meteor button, then tap","Q"),("Reinforcements","Soldiers button, then tap","W / E"),("Speed / pause","1x and II buttons","F, P / Esc")],
  features=["30 handcrafted levels in 4 worlds, each with a boss fight",
            "4 towers with 3 tiers and 2 specialised branches each",
            "17 enemy types: fast, armoured, flying, healers, splitters, burrowers, summoners and more",
            "Meteor Strike and Reinforcements hero abilities with cooldowns",
            "Early wave calls for bonus coins",
            "3-star ratings and a permanent star upgrade tree",
            "Endless mode, an encyclopedia and 1x/2x speed",
            "Music and sound effects made in code, and progress saved on your device"]),
dict(slug='number-dash', name='Number Dash', genre='Puzzle', color='#4cb8ff',
  tagline='A fun math runner: steer through + − × ÷ gates, answer quick sums and grow your number to beat the Number Monster.',
  about=['Number Dash is a math runner for phones and desktop browsers, made for young kids and grown-ups alike. Your Number Buddy starts at 1 and dashes down a bright track. Every gate shows a sum: + and × gates make your number grow, − and ÷ gates make it shrink. Choosing well is the real puzzle: +10 beats ×2 when your number is small, but ×2 wins once it is big.', 'Quiz doors ask a quick question, like 7 + 5 or 6 × 8, and running through the right answer adds it to your number. At the end of every level a Number Monster waits with its own number. Be bigger and you win, and the closer you get to the best possible number, the more stars you earn. There are 60 levels across six worlds (Sunny Meadow, Desert Dunes, Candy Land, Snowy Peaks, Tropic Beach and Starry Space), 12 Buddies to unlock with coins, and three math levels: Easy (adding and taking away), Medium (times tables) and Hard (big sums, dividing and squares).'],
  how=['Drag left or right anywhere on the screen (or use the arrow keys) to steer your Number Buddy.', 'Blue gates (+ and ×) make your number bigger. Red gates (− and ÷) make it smaller. When both gates are blue, work out which one gives the bigger number.', 'On quiz doors, work out the sum on the red banner and run through the door with the right answer to add it to your number.', 'Dodge the grumpy minus clouds and collect coins along the way.', "Reach the finish with a number bigger than the Number Monster's to clear the level. Finish near the best possible number for 3 stars.", 'Spend coins on new Buddies, and pick Easy, Medium or Hard math in Settings.'],
  controls=[('Steer', 'Drag left / right', 'Left / Right arrows or A / D'), ('Pause', 'II button', 'P / Esc'), ('Start', 'Play button', 'Enter / Space')],
  features=['60 levels across 6 colourful worlds', '+ − × ÷ gates where picking the bigger number is the puzzle', 'Quiz doors with quick sums, times tables and dividing', 'Easy, Medium and Hard math levels for ages 5 to adult', 'Number Monster finale, 3-star ratings and coins', '12 cute Buddies to unlock, plus achievements', 'Music and sound effects made in code, and progress saved on your device']),
dict(slug='pirate-isles', name='Pirate Isles', genre='Adventure', color='#1b8fd6',
  tagline='A cartoon pirate sailing adventure: trade cargo between ports, dig up treasure, beat pirate bosses and upgrade your ship.',
  about=['Pirate Isles is a top-down pirate sailing adventure for phones and desktop browsers. You captain a little sloop in a bright island sea with four harbour towns (Coral Bay, Palm Harbor, Frost Point and Sunset Town) and eight wild islands, from palm-covered Turtle Isle to spooky Skull Rock.', 'A 12-mission story teaches you to sail, then sends you on cargo runs, treasure hunts and pirate patrols, and ends with two boss battles against Captain Redbeard and Admiral Blackfin. After that, every port has fresh contracts. Cannons fire automatically and the battles are cartoon-style: beaten pirates wave a white flag and sail off to sulk. Spend your gold on hull, sail, cannon and cargo upgrades, and buy bigger ships as your rank grows.'],
  how=['Drag anywhere on the screen and your ship turns and sails toward your finger. Drag further to sail faster. On a keyboard, use WASD or the arrow keys.', 'Your cannons fire by themselves at the nearest pirate ship in range. Keep moving to dodge their cannonballs.', 'Follow the yellow arrow and the minimap to your current mission.', "Sail slowly into a harbour's anchor ring and tap Dock (or press E) to pick missions, repair and visit the shipyard.", 'For cargo missions, dock to load the crates, then dock at the destination port to deliver them.', 'Your ship slowly repairs itself when you are out of battle. If it is wrecked, you restart at the last port you docked at.'],
  controls=[('Steer and sail', 'Drag anywhere', 'WASD / arrow keys'), ('Fire cannons', 'Automatic', 'Automatic'), ('Dock at a port', 'Dock button', 'E / Enter'), ('Pause', 'II button', 'P / Esc')],
  features=['A big island sea with 4 harbour towns and 8 wild islands', '12 story missions plus endless contracts: cargo, treasure, salvage and pirate bounties', 'Two boss battles: Captain Redbeard and Admiral Blackfin', 'Auto-firing cartoon cannons with splashes, smoke and white-flag surrenders', 'Upgrade the hull, sails, cannons and cargo hold, and unlock the Brigantine and Galleon', 'Ranks, XP, achievements, a minimap and an objective arrow', 'Sea-shanty music and sound effects made in code, and progress saved on your device']),
dict(slug='sunny-acres', name='Sunny Acres', genre='Simulation', color='#7ccf4f',
  tagline='A cozy farm game: plant and harvest crops, care for cute animals, bake treats and fill truck orders.',
  about=['Sunny Acres is a relaxing farm game for phones and desktop browsers, made for kids and grown-ups. Start with six little fields and a handful of coins, plant wheat and corn, and grow your farm into a busy countryside business with 20 fields, a chicken coop, a cow pasture, a sheep meadow, a bakery, a dairy, a kitchen and a loom.', 'Planting and harvesting are quick and satisfying: pick a seed once, then swipe across as many fields as you like. Animals need feeding from your own crops, and buildings turn crops, eggs, milk and wool into goodies worth much more. Villagers post orders on the truck board, and every delivery earns coins and XP. Progress is saved on your device, and crops keep growing while you are away.'],
  how=['Tap an empty field and choose a seed. Keep your finger down and swipe over more empty fields to plant the same seed.', 'Crops bounce and sparkle when they are ready. Tap or swipe over them to harvest. Each field gives 2 crops.', 'Tap an animal pen to feed it (chickens eat wheat, cows eat corn and sheep eat carrots), then tap again later to collect eggs, milk or wool.', 'Tap a building such as the Bakery to make goodies from your crops and animal products, and tap it again to collect them.', 'Open Orders to send the truck with what villagers ask for. Skip an order you do not like and a new one arrives.', 'Drag to look around the farm. Use the Barn to sell extra items and the Shop to buy fields, a bigger barn and more animals.'],
  controls=[('Plant / harvest', 'Tap or swipe over fields', 'Click or drag over fields'), ('Look around', 'Drag the farm', 'Drag, mouse wheel to zoom'), ('Orders, barn, shop', 'Bottom buttons', 'Click the buttons'), ('Menu', 'II button', 'Click II')],
  features=['6 crops, 3 kinds of animals and 4 production buildings', '11 goodies to make, from bread and cheese to pumpkin pie and sweaters', 'Truck orders from friendly villagers, with coins and XP rewards', 'Swipe to plant and harvest lots of fields at once', 'Level up to unlock new crops, animals, buildings and recipes', 'Buy up to 20 fields, extra animals and a bigger barn', 'Gentle music and sounds made in code, offline growth and progress saved on your device']),
dict(slug='skyfire-squadron', name='Skyfire Squadron', genre='Shooter', color='#2f8fe0',
  tagline='A cartoony airplane shooter: auto-fire at enemy planes and bomb ships, subs and island guns across 32 missions.',
  about=['Skyfire Squadron is a free cartoon airplane shooter. Your plane fires automatically while you steer through waves of enemy fighters and drop bombs on battleships, carriers, submarines and island guns.', 'There are 32 missions across sunny seas, palm isles, frosty fjords and a thunder night, each area ending with a giant multi-part boss. Unlock 5 planes, upgrade them and recruit wingmen. Progress is saved on your device.'],
  how=['Tap Play and pick a mission.', 'Drag anywhere to fly your plane. Your guns fire automatically.', 'Dodge enemy bullets and shoot down planes.', 'Line up over ships, subs and island guns to bomb them.', 'Grab power-ups, then beat the boss at the end of the area.', 'Spend coins on upgrades, new planes and wingmen.'],
  controls=[('Fly', 'Drag anywhere', 'Mouse drag, or arrow keys / WASD'), ('Fire', 'Automatic', 'Automatic'), ('Drop a bomb', 'BOMB button', 'B key'), ('Mega attack', 'Mega button', 'Space'), ('Pause', 'II button', 'P or Esc')],
  features=['32 missions in 4 areas', 'Giant multi-part bosses', '5 planes to unlock and upgrade', 'Wingmen to recruit', 'Bombs for ships, submarines and island guns', 'Progress saved on your device']),
dict(slug='bolt-brigade', name='Bolt Brigade', genre='Shooter', color='#f59e0b',
  tagline='A family-friendly cover shooter: pop out to blast wind-up toy robots, duck to reload. 35 missions, 5 bosses.',
  about=['Bolt Brigade is a free, family-friendly cover shooter. The enemies are wind-up toy robots that go CLANK, not people, and you fight them from behind crates and walls.', 'Play 35 missions across 5 stages, each with a boss, and upgrade your blasters with the coins you collect. Progress is saved on your device.'],
  how=['Tap Play and choose a mission.', 'Hold the screen to pop out of cover and auto-fire.', 'Aim by moving your finger or mouse over the robots.', 'Let go to duck behind cover and reload.', 'Use the EMP button to stun lots of robots at once.', 'Clear every wave, beat the boss and upgrade your blasters.'],
  controls=[('Pop out & fire', 'Hold the screen', 'Hold the mouse button or Space'), ('Aim', 'Move your finger', 'Move the mouse'), ('Duck & reload', 'Let go', 'Release'), ('EMP', 'EMP button', 'E key'), ('Pause', 'II button', 'Esc')],
  features=['35 missions across 5 stages', '5 boss robots', 'Blaster upgrades', 'Simple hold-to-shoot, let-go-to-hide controls', 'Family-friendly toy robot enemies', 'Progress saved on your device']),
dict(slug='critter-keep-rescue', name='Critter Keep Rescue', genre='Adventure', color='#7fd0f0',
  tagline='Sneak, rescue and collect 30 cute critters across 36 levels.',
  about=['Critter Keep Rescue is a free kids game that mixes gentle stealth with critter collecting. Your critters earn coins in a cozy keep, and cheeky raccoon bandits keep borrowing them.', 'Sneak through 36 rescue levels to bring them home, hatch eggs, merge for rarer critters and defend your keep.'],
  how=['Tap Rescue to start a level.', "Move your keeper and stay out of the bandits' sight.", 'Reach the critters and lead them home.', 'Hatch eggs and merge critters in your keep.', 'Build fences, a bell and a guard puppy, and tap raiding bandits to chase them off.'],
  controls=[('Move', 'Drag / tap', 'Arrow keys or WASD, or click'), ('Keep actions', 'Tap the buttons', 'Click the buttons')],
  features=['36 stealth rescue levels', '30 cute critters to collect', 'Hatch and merge', 'Keep defences and raids', 'Kid-friendly, progress saved on your device']),
dict(slug='beat-buddies', name='Beat Buddies', genre='Music', color='#7b4dff',
  tagline='Drag 25 cute singing buddies onto the stage and make your own song.',
  about=['Beat Buddies is a free music game for kids. 25 buddies each sing, drum or beatbox a loop that always stays in time, so every mix sounds good.', 'Find secret combos for special animations, record your song and share it with a link.'],
  how=['Drag a buddy from the tray onto the stage to add its sound.', 'Drag a buddy off the stage to remove it.', 'Try different mixes of beats, bass, melody, chords and voices.', 'Discover secret combos.', 'Record your mix and share the link.'],
  controls=[('Add / remove a buddy', 'Drag', 'Drag with the mouse'), ('Record / play / share', 'Top buttons', 'Click the buttons')],
  features=['25 singing, drumming and beatboxing buddies', 'Loops always in time', 'Secret combos', 'Record and share songs with a link', 'Kid-friendly, works offline once loaded']),
dict(slug='silly-sprout-garden', name='Silly Sprout Garden', genre='Kids', color='#ff9ad5',
  tagline='Plant magic seeds and grow 34 silly creature-plants in a cozy garden game for kids.',
  about=['Silly Sprout Garden is a free garden game for kids. Every magic seed grows into a funny creature-plant, from the Cactus Penguin to the Banana Shark, and there are 34 to collect.', 'Water your plots, harvest, sell and buy new seeds. Special weather brings rare golden, rainbow and glowing mutations to fill your collection book. Progress saves on your device.'],
  how=['Tap an empty plot to plant a seed.', 'Water your sprouts and wait for them to grow.', 'Harvest ready plants and sell them for coins.', 'Buy new seeds to discover more creatures.', 'Watch for special weather to catch rare mutations.'],
  controls=[('Plant / water / harvest', 'Tap a plot', 'Click a plot'), ('Menus', 'Tap the buttons', 'Click the buttons')],
  features=['34 silly creature-plants to collect', 'Golden, rainbow and glowing mutations', 'Changing weather', 'Collection book', 'Kid-friendly, no reading needed to play', 'Progress saved on your device']),
dict(slug='betta-bestie', name='Betta Bestie', genre='Pets', color='#3b82f6',
  tagline='Feed, play and watch TV with your own pet betta fish.',
  about='Betta Bestie is a free, kid-friendly virtual pet game. Your betta never gets hurt: if you are away she just feels a little sad until you come back. Feed her every day to grow your streak and open a daily gift.',
  how=['Feed her daily: tap Feed, then tap the water to drop pellets. Stop when she says she is full.', 'Tap Clean to rub away algae and use Water for a fresh water change.', 'Tap her to say hi; drag your finger and she follows.', 'Play five mini-games to earn coins and XP.', 'Spend coins in the Shop on decor, plants, gravel, TV channels and cushions. Level up to unlock new colours.'],
  controls=[('Feed, pet, pop, jump', 'Tap', 'Click'), ('Lead her, wipe algae', 'Drag', 'Drag')],
  features=['A gorgeous animated betta in 10 colours', 'Cosy room with a blue sofa, TV cartoons and real day/night', '5 mini-games plus TV time', 'Daily streak, daily gift, levels and 19 achievements', 'Free, no ads during play, saves on your device']),
dict(slug="juicy-merge", name="Juicy Merge", genre="Puzzle", color="#ff6b4a",
  tagline="A juicy fruit merge physics puzzle: drop, merge and chain fruits all the way up to the Watermelon.",
  about=["Juicy Merge is a fruit merge physics puzzle for phones and desktop browsers. You drop fruits into a glass jar, and when two of the same fruit touch they squish together into the next size up: Blueberry, Cherry, Lime, Plum, Lemon, Orange, Apple, Peach, Coconut, Pineapple and finally the Watermelon. Merge two Watermelons for a Juice Jackpot.",
         "Fruits roll, stack and settle with a custom physics engine, and every merge bursts with juice splashes, sparkles and squash-and-stretch. Quick merges in a row build combo chains for bonus points. Play endless Classic, race the clock in Timed mode, or try the Daily Challenge, where everyone gets the same fruit order and a daily goal. Earn coins to unlock themed jars, fruit skins and power-ups."],
  how=["Drag left or right (or move the mouse) to aim the fruit above the jar, then let go (or click) to drop it.",
       "When two of the same fruit touch, they merge into the next fruit up. The Next box shows which fruit comes after this one.",
       "Merge several times within a moment of each other to build a combo chain. Each step raises your score multiplier, up to x4.",
       "Keep the pile below the red line. If a fruit rests above it for 3 seconds, the jar overflows and the game ends.",
       "Use power-ups when you are stuck: Shake stirs the whole jar, Pop removes one fruit, and Upgrade grows a fruit by one size.",
       "Timed mode lasts 90 seconds, and Orange or bigger merges add time. The Daily Challenge pays a coin reward when you hit its goal."],
  controls=[("Aim","Drag","Left / Right or A / D, or move the mouse"),("Drop","Release","Space, Down or Enter, or click"),
            ("Power-ups","Shake, Pop and Upgrade buttons","1 / 2 / 3, then Left / Right and Enter to pick a fruit"),("Pause","II button","P / Esc")],
  features=["11 fruit sizes with cute faces, from Blueberry to Watermelon",
            "Stable, satisfying fruit physics with rolling, stacking and no jitter",
            "Juicy merge effects, combo chains and a Juice Jackpot",
            "Next-fruit preview, aim guide and a red line with a 3-second grace timer",
            "Classic, Timed and Daily Challenge modes",
            "Shake, Pop and Upgrade power-ups",
            "6 themed jars and 5 fruit skins to unlock with coins, plus 19 achievements",
            "Music and sound effects made in code, and progress saved on your device"]),
dict(slug="zaib-city", name="Zaib City", genre="Simulation", color="#ffb21f",
  tagline="A family-friendly 3D open-world city adventure: borrow cars, help the city with jobs, race, stunt and explore.",
  about=["Zaib City is a family-friendly 3D open-world city game for phones and desktop browsers. The bright low-poly city has a downtown of glass towers, a leafy suburb, a sunny beach with a boardwalk pier and a harbour, an industrial zone, a big park with a lake, a highway loop and Sunset Hill with stunt ramps. Time flows from sunrise to starry night, and the weather changes between sunshine, clouds, rain and fog.",
         "Everyone in Zaib City is friendly. Walk up to any parked car or any car in traffic: the driver politely stops, steps out, waves and lends it to you. Traffic follows the roads and the traffic lights, pedestrians stroll the sidewalks and jump aside, and bumps are always harmless and funny. Instead of a wanted level you build Reputation by driving nicely, waiting at red lights and helping people.",
         "Earn cash and XP with taxi fares, pizza and parcel deliveries, ambulance runs to the hospital, fire truck call-outs with a water cannon, police speed patrols where you bump speeders to pull them over, street races, time trials, parking challenges, a bus route and stunt shows. A 22-mission story with friendly characters unlocks new districts. Spend your cash on 14 cars at the dealership, paint and upgrades at the garage, and homes that work as save points."],
  how=["On foot, drag the left side of the screen to walk (push further to run) and tap JUMP. Drag the right side to look around.",
       "Tap ENTER next to any car to get in. Traffic drivers stop, hop out and wave. Tap EXIT to get out.",
       "Drive with the left and right arrows, GAS and BRAKE (hold BRAKE to reverse). Hold DRIFT while turning to slide, and press NITRO for a boost. Tilt or stick steering is in Settings.",
       "Follow the pink GPS line on the minimap. Gold ★ markers are story missions and coloured beams are jobs. Drive into a marker and tap the button that appears.",
       "Open the phone for jobs, the story list, car delivery, homes, districts, daily challenges and awards. On the big map, tap anywhere to set a waypoint.",
       "Visit Sprocket's Garage to repair, paint and upgrade, Zaib Motors to buy cars, and homes to rest and save. Find the hidden stars and land every stunt jump."],
  controls=[("Walk / run","Left stick","WASD / arrows, Shift to run"),("Jump","JUMP button","Space"),("Enter / exit car","ENTER button","E"),
            ("Steer, gas, brake","Arrow, GAS and BRAKE buttons (or tilt)","A / D, W, S"),("Drift / nitro","DRIFT and NITRO buttons","Space / Shift"),
            ("Horn, siren, water cannon","Horn, siren and SPRAY buttons","H, Q, F"),("Map, phone, pause","Map, phone and pause buttons","M, Tab, P / Esc")],
  features=["A big open city: downtown, suburb, beach and harbour, industrial zone, park, highway loop and a stunt hill",
            "Borrow any car: friendly drivers stop, step out and wave",
            "15 vehicles including a taxi, police cruiser, ambulance, fire engine, bus, motorbike and supercar",
            "Arcade handling with drifting, nitro, jumps, cosmetic damage and garage repairs",
            "11 job types plus a 22-mission story with characters and dialogue",
            "AI traffic with traffic lights, pedestrians who dodge and wave, and Reputation instead of crime",
            "Day/night cycle and weather, minimap with GPS, a full map with waypoints and a phone menu",
            "Cars, paint, upgrades, homes, unlockable districts, daily challenges and achievements, saved on your device"]),
dict(slug='30-floors-up', name='30 Floors Up', genre='Survival', color='#f97316',
  tagline='A kid-friendly day-by-day zombie survival strategy game: ration, barricade and outsmart the goofy Shamblers.',
  about=['30 Floors Up is a survival strategy game for phones and desktop browsers. You are stuck in an apartment on the 30th floor while goofy green Shamblers shuffle around outside. Each day brings a new story card and a few actions, and every choice costs something.', 'Ration your water and food, fortify the door, keep the noise down, trade with your neighbours and plan your escape to the roof. The zombies are silly rather than scary, so it suits younger players too.'],
  how=["Each morning, read the day's card and pick one of its choices. Icons show which supplies each choice changes.", 'Spend your actions for the day: Fortify, Scavenge, Catch rain, Rest, Trade or Craft.', 'Keep an eye on your water, food, health and noise. Noise draws the Shamblers to your door.', 'Tap End day when you are done, and survive day by day until you can escape to the roof.'],
  controls=[('Choose an action', 'Tap a card or button', 'Click'), ('End the day', 'End day button', 'Click')],
  features=['Day-by-day survival with story and event cards', 'Water, food, health and noise to balance', 'Fortify, scavenge, trade and craft', 'Goofy, kid-friendly Shamblers instead of scary zombies', 'Cosy cartoon art, music and sound effects', 'Progress saved on your device']),
dict(slug='rail-rush', name='Rail Rush', genre='Puzzle', color='#2f7a45',
  tagline='A kid-friendly train puzzle game: flip the track switches and get every train to the right station.',
  about=['Rail Rush is a train track switching puzzle for phones and desktop browsers. Colourful trains roll along branching tracks, and you flip the switches so each one reaches the station of the same colour.', 'There are 30 levels across meadows, canyons and snowy peaks, with collectible engines and upgrades to unlock as you go.'],
  how=['Watch the trains coming along the track and check their colours.', 'Tap a switch to change which way the track goes.', 'Send each train into the station that matches its colour. A wrong station costs you.', 'Clear every train in the level to win stars, then unlock new engines and upgrades.'],
  controls=[('Flip a switch', 'Tap the switch', 'Click the switch')],
  features=['30 levels across meadows, canyons and snowy peaks', 'Colour-matching track switching puzzles', 'Collectible engines and upgrades', 'Bright cartoon art, music and sound effects', 'Progress saved on your device']),
dict(slug='tank-rumble', name='Tank Rumble', genre='Shooter', color='#3b82f6',
  tagline='A kid-friendly toy tank battle game: just drive, your tank fires by itself.',
  about=['Tank Rumble is a cartoon tank action game for phones and desktop browsers. Drive a cute toy tank around a play-mat arena while it fires automatically, popping waves of goofy robots into bolts and stars.', 'Fight through stages that end in big boss bots, pick power perks between waves and upgrade or unlock new tanks in the garage.'],
  how=['Drag anywhere on the screen to drive. Your tank aims and fires by itself.', 'Dodge enemy shots and pick up the bolts and stars that robots drop.', 'Choose a power perk when one is offered to make your tank stronger.', 'Beat the boss bot at the end of each stage, then spend your bolts in the garage.'],
  controls=[('Drive', 'Drag anywhere', 'Drag with the mouse'), ('Fire', 'Automatic', 'Automatic'), ('Pause', 'Pause button', 'Esc')],
  features=['Simple one-finger controls with auto-fire', 'Waves of goofy robots and big boss bots', 'Power perks to pick during each run', 'Garage upgrades and unlockable tanks', 'Cartoon toy-room art, music and sound effects', 'Progress saved on your device']),
dict(slug='corner-office', name='Corner Office', genre='Idle', color='#6366f1',
  tagline='An idle office game: tap, hire funny coworkers and get promoted from Intern all the way to CEO.',
  about=['Corner Office is an idle rank-up game for phones and desktop browsers. Start as an intern at a small desk, tap to work, play quick office tasks and earn coins.', 'Hire funny coworkers to earn for you, reach your performance goals and get promoted up 10 ranks to CEO. Your desk and office get fancier with every promotion.'],
  how=['Tap your desk to work and earn coins.', 'Play quick office tasks such as Coffee Rush, File Frenzy and Inbox Zero for bigger rewards.', 'Hire coworkers and buy upgrades so you earn coins even when you are not tapping.', 'Fill the performance bar to get promoted to the next floor and rank.'],
  controls=[('Work', 'Tap your desk', 'Click your desk'), ('Tasks and office', 'Tasks / Office tabs', 'Click')],
  features=['Climb 10 ranks from Intern to CEO', 'Quick office mini-tasks', 'Hire funny coworkers for idle income', 'Your office grows fancier with every rank', 'Cartoon art, music and sound effects', 'Progress saved on your device']),
dict(slug='dream-room', name='Dream Room', genre='Design', color='#ff7a59',
  tagline='An interior design makeover game: design dream rooms for happy clients.',
  about=['Dream Room is an interior design game for phones and desktop browsers. Fun clients ask you to make over their rooms, and you pick the furniture, colours, rugs, lights and walls.', "Match each client's style, colour palette and budget, then watch the big before and after reveal. There are 32 levels, multi-room homes and hundreds of decor pieces."],
  how=["Read the client's brief: their style, palette and budget.", 'Tap a glowing + in the room to choose a piece, or pick a category such as Sofa or Walls.', "Keep within the budget and match the client's taste for a better score.", 'Tap Done when every spot is filled to see the before and after reveal.'],
  controls=[('Place or change a piece', 'Tap a + or an item', 'Click'), ('Finish the room', 'Done button', 'Click')],
  features=['32 levels with multi-room homes', 'Hundreds of furniture and decor pieces', 'Client styles, palettes and budgets to match', 'Big before and after reveals', 'Soft cartoon art, music and sound effects', 'Progress saved on your device']),
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
    # text fields may be given as a single string or a list of paragraphs/items (a bare string must not be iterated per letter)
    for k in ('about', 'how', 'features'):
        if isinstance(g.get(k), str): g[k] = [g[k]]
    rows = "".join(f"<tr><td>{e(a)}</td><td>{e(t)}</td><td>{e(k)}</td></tr>" for a, t, k in g["controls"])
    body = f"""<span class="genre" style="--gc:{g['color']}">{e(g['genre'])}</span>
<h1>{e(g['name'])}</h1>
<p class="lead">{e(g['tagline'])} Free to play in your browser, no download or sign-up.</p>
<a href="/{g['slug']}/"><img class="hero" src="/img/{g['slug']}.webp{IMG_V.get(g['slug'],'')}" alt="{e(g['name'])} gameplay screenshot" width="600" height="375"></a>
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
         og_image=f"/img/{g['slug']}.webp{IMG_V.get(g['slug'],'')}")

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

def sort_by_hub_order():
    """Keep the guides list / about page in the same ranked order as the hub's GAMES array."""
    order = [p.strip("/") for p in game_paths()]
    GAME_INFO.sort(key=lambda g: order.index(g["slug"]) if g["slug"] in order else len(order))

if __name__ == "__main__":
    sort_by_hub_order()
    for g in GAME_INFO: game_page(g)
    games_index(); about(); contact(); privacy(); terms(); sitemap()
    print("info pages, sitemap.xml and robots.txt built")
