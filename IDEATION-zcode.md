# IDEATION — the PAGES LENS (zcode, 2026-10-21)

Territory: **the phone experience.** An ASCII viewfinder descendant
(chiaroscuro's lineage) that maps a room as Casey walks it, with
adaptive fidelity made VISIBLE, and something honest on screen while
the splats grow behind the glyphs. The phone is splat-room's missing
"moving seat" — the README says today's single fixed view must become
views that move before stage 2 can see a room; the phone in his hand is
the view that moves while he lives in the house.

Grounding (what these riffs build ON, all measured or read, not vibes):
- chiaroscuro's pipeline (downsample → brightness → change → pick
  glyph → pick color → room) and its doors — especially the
  **Viewfinder** (capture without rendering) and **edge/** (a
  Cloudflare Worker: the phone page's natural brain-home).
- The bench liaison's proven page tier: one-clock session bundles,
  braille conversion at exactly 80×24 from 160×96 luma, railed
  speakers, worklet taps, the probe pattern (SEED-CONVERSIONS §2).
- ADDENDUM-ASCII-PHONE: motion-indexed adaptive fidelity (still =
  high-res deltas-only; moving = low-res fast), tilt/GPS/video pose
  fused for walked maps.
- ADDENDUM-AWARENESS-CALCULATORS: the walk-by ENVELOPE is the robust
  signal; calculators, not answers.
- BRIEF-WAKE-AND-TURN: OVER as a trained transmit word (already a
  measured probe on the bench).

---

## 1. The Walking Viewfinder — capture without rendering, inverted

chiaroscuro's Viewfinder freezes a STILL. The phone inverts it: it
freezes the ROOM. The glyph grid is the live viewfinder; when fidelity
says "still" (idea 2) and the pose says "new vantage", the page PINS a
keyframe — a glyph snapshot with its pose guess — to a walked map that
accumulates behind the viewfinder all day.

```
┌─────────────────────────┐  ┌─────────────────────────┐
│ ░▒▓█ VIEWFINDER █▓▒░    │  │ THE WALKED MAP (grows)  │
│ ▓█▓  ╥╥╥      ▓▒░       │  │  k7──k6   k5            │
│ ▒█▒  ╜╜╜  ───  ▒░       │  │   ╲      ╲              │
│ ░█░   @@   o    ░       │  │    k4──k3──k2   k1      │
│  (live glyphs)          │  │     (pinned keyframes,  │
│  [● pinned 7]           │  │      newest = brightest)│
└─────────────────────────┘  └─────────────────────────┘
   front: what the camera sees    behind: what the walk has banked
```

Pin rule, stated: a keyframe pins when (a) the frame is STILL by the
motion index for ≥ 1 s, (b) the vantage differs from the nearest
pinned keyframe by more than a stated pose distance, (c) the glyph
grid's edge density (chiaroscuro's Sobel stage, already measured per
cell) clears a floor — blank walls don't bank. The phone never renders
the splat; it banks VIEWABLE EVIDENCE (glyph grid + pose + the raw
still for the bench's fidelity) and the bench/Oracle grows splats from
the pins. Capture without rendering, at room scale.

## 2. Fidelity Weather — the attention budget as texture

Adaptive fidelity made visible means the USER SEES the system's
attention, not a settings slider. The phone's glyph density IS the
weather instrument:

```
 STILL (you stopped):                MOVING (you walk):
 ┌───────────────────────┐           ┌───────────────────────┐
 │ ⣿⣿⠛⣿⣿⣿⠋⣿⣿⣿⣿⣿⣿⣿ │  hi-res   │ ▓▓  ░░    ▒▒  ░     │  lo-res
 │ ⣿⠋⣿⣿⣿⣿⣿⠛⣿⣿⣿⣿⣿⣿ │  braille  │   ▒▒▒      ░░▒     │  coarse
 │ ⣿⣿⣿⣿⠛⠛⣿⣿⣿⣿⣿⣿⣿⣿ │  + rain   │ ░░   ▓▓▓   ░     ░  │  fast
 │ ░░░░░░░░░░░░░░░░░░░░░ │  delta    │  (only what moves     │
 │  only CHANGED cells    │  afterimg │   re-renders at all)  │
 │  re-render; the rest   │           │                       │
 │  dims to afterimage    │           │                       │
 └───────────────────────┘           └───────────────────────┘
   ▲ fidelity bar: 48 cols            ▲ fidelity bar: 12 cols
```

The rule is ADDENDUM-ASCII-PHONE's (still = high-res deltas-only;
moving = low-res fast); the VISIBLE part is new: a one-row fidelity
bar (glyph columns, literally countable) plus delta-rain — unchanged
cells decay to a dim afterimage instead of vanishing, so the still
picture reads as PRESENT but CHEAP. The weather metaphor is the UI: he
glances and knows the system is spending attention where he is.

## 3. Ghost Behind the Glyphs — the registration screen

What he SEES while splats grow behind the glyphs: both at once. The
live ASCII viewfinder renders SOLID in front; the splat field, rendered
from the phone's estimated pose, GHOSTS behind at low opacity. The
product is the MISALIGNMENT: where glyph edges and ghost edges disagree,
the reconstruction is hungry, and the page can say so in its own
language — mismatched cells shimmer.

```
   glyph layer (solid, live)      ghost layer (faint, believed)
   ▓▓■░▒▓▓▓▒░▓▓▓▓▒▒░            ·:·º·:·:·:·:·:·:·:·:·
   ▓▓▓▓▒▒▓▓▓▓▒▓▓▓▓▓▒            ·:····:·:·····:···:·
   ░▒▓▓▓▓▒▒▓▓▓▓▓▓▓▒▒            ···:·:···:··:······
        ▲ door edge glyphs           ▲ the ghost's door is 2 cells left
        ── shimmer cells mark the drift; walk 2 steps left to feed it
```

The page never computes the splat — it fetches a low-res depth/edge
projection from the bench (the liaison serves it; the forwarder
pattern, reversed direction) and composites. The screen is a
REGISTRATION INSTRUMENT: Casey IS the camera mover, so the UI's job is
to make hunger visible where he can fix it by standing there.

## 4. Depth as Punctuation — audio as the depth sense, in the glyphs

splat-room's law: audio disciplines the splats. On the phone, the
walk-by ENVELOPE (the calculators addendum's robust signal — Doppler at
walking speed is beneath honesty) renders as a moving brightness wave
across the map when he passes the bench mic; and the phone's own chirp
(the probe rails already govern stimulus on the bench; the phone
inherits the rails) returns with a delay the page shows as PUNCTUATION
before wall glyphs:

```
   ..▓▓▓▓..        ::░░░░::        ...▒▒▒▒...
   near wall       mid wall        far wall
   (1 leading dot per ~5 ms of return; honest when the return is
    measured, absent when the band is dead — the lens file says so)
```

Depth cues are cheap, per-column, and never pretend to be a depth
MAP — they are punctuation, the way prosody punctuates a transcript.

## 5. Walk Receipts — the map as a shareable artifact

chiaroscuro's receipts pattern (frames are the receipts) extended to
the room: every walk auto-produces a one-screen WALK RECEIPT — the
walked map (idea 1) stamped with coverage shading, fidelity weather
history, and the session's honest numbers (keyframes banked, still/move
ratio, audio depth cues measured, dead-band disclosures from the lens
files). Diffable between walks; the EXPERIMENTS ledger gets a row with
a path to the receipt, never an inlined boast.

```
 WALK RECEIPT — 2026-10-21 14:32 · 11 min · 9 keyframes
 ██████████████▓▓▓▓▓▓▓░░░░░░░  coverage: dense W wall, hungry E
 k1─k2─k3─k4──k7   ▲ still 62% / moving 38%  ▲ 31 depth cues
        ╲ k5,k6   ▲ audio: 2 walk-bys, 0 dead-band events
                   bench: splats +4,100 this walk (fed by k4,k7)
```

## 6. Two-Time View — the palimpsest

Hold the phone up where you stood yesterday: yesterday's pinned
keyframe ghosts UNDER today's live glyphs. Unchanged room = the layers
click (glyphs agree); changed room = the mismatch GLOWS (new chair,
moved lamp). The room's change log, readable at a glance, for free —
it is idea 1's map read in time instead of space.

## 7. No Buttons — the glyph walkie-talkie

The phone page's chrome is glyphs, not widgets (chiaroscuro's doors
have almost no UI; the phone should have none): tap-hold = pin a
keyframe NOW, swipe = override fidelity weather for 10 s, double-tap =
OVER — the trained transmit word from the wake-and-turn brief, already
a measured conjunction on the bench. The phone is a walkie-talkie in
the glyph language: it talks to the bench with keyframes and OVERs, and
the bench's reply (digestion, co-reading screen mode) lands as a glyph
ticker, one line, no modal.

## 8. The Edge Directory — chiaroscuro's worker as the phone's home

chiaroscuro's edge/ is a deployed Cloudflare Worker; the phone page is
Cloudflare-hosted by plan. The DIVISION: the phone does glyphs LOCALLY
(camera never leaves the device — chiaroscuro's law, kept), the worker
keeps the pose graph, keyframe directory, and walk receipts; the bench
liaison remains the ROOM's brain (splats, lens files, self-checks) and
the worker talks to IT, not the other way around — fleet as upgrade
never dependency, the boat law: on the boat, the phone page degrades to
ideas 1+2 alone (local banking, local fidelity weather) and loses
nothing recorded.

---

## CROSS — steals and extensions

*(Sibling riffs had not landed when this file was written; the two
steals below are from chiaroscuro — a real seat's shipped work — and
two reserved slots name what I will extend the moment siblings land.
Steal honestly, credit plainly.)*

**Stolen from chiaroscuro — the `?mock=` piping (Viewfinder door).**
The Viewfinder's mock-image piping is how the PHONE gets tuned without
a phone: the bench's frame-bundle stills (already on the Jetson, 460 of
them) pipe into the phone page as mock camera frames, so fidelity
weather and pin rules are tuned against REAL room data at the desk
before the first walk. Extension: a `?mockWalk=` mode that replays a
walk's keyframe sequence as a synthetic walk, so the walked map and
receipt logic are testable end-to-end with no one standing up.

**Stolen from chiaroscuro — the receipts/walker vocabulary itself.**
Frames-as-receipts becomes walks-as-receipts (idea 5), and the ledger
culture it implies is why receipts carry measured numbers with stated
bars. This is the cleaner steal: not a feature, a DISCIPLINE, and it
is why idea 5's receipt prints the still/move ratio rather than a
satisfaction score.

**Reserved: [sibling riff slot 1].** The first sibling riff on audio
or pose will likely own the chirp schedule or the pose fusion — if so,
idea 4's punctuation and idea 1's pin rule should CONSUME their
calculator outputs verbatim (the liaison's lens registry is the
contract), not re-derive them.

**Reserved: [sibling riff slot 2].** The first sibling riff on the
splat/Blender side owns what idea 3's ghost layer actually receives; I
expect to steal its projection format whole and re-render it as glyphs
— the extension direction is: the ghost should be rendered THROUGH the
same glyph pipeline (a depth-ramp glyph set), not as pixels, so the
registration screen stays one language.
