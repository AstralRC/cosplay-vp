---
name: cosplay-vp-anime-fx
description: Give finished cosplay CG footage the anime and game-cinematic look - on twos timing, hit stop, impact frames, cut-in panels, title slams, grade - and deliver 9:16 cuts and a before/after demo. Use when a comp is done and needs the anime language, or when making a showreel or pitch demo.
---

# Cosplay VP anime FX and delivery

Reference: `docs/06-anime-fx-language.md`.

## Timing and impact (MCP tools)

- `on_twos(input, output, hold=2)`: snappier, drawn-animation motion. Use on action beats, not on slow dialogue or faces.
- `impact_frames(input, output, frames=[...], length=2, mode="invert")`: 1–3 flash frames at each hit. Ask the user for the hit frame numbers, or find them from the shot sheet.
- Hit stop and speed ramps happen in the editor; describe where to put them (2–6 held frames on impact).

## Cut-in (ultimate move)

Describe or build in After Effects / Unreal:
1. Freeze or slow the action.
2. Slide in a panel with the matted close-up over a graphic in the character's colours.
3. Title slam: 120% → 100% over 3–4 frames with a flash.
4. Hold 12–24 frames, then cut back on an impact frame.

Use the character's real move name only when the work is licensed or unpaid fan work.

## Grade

Higher contrast and saturation, one strong colour per character, bloom on highlights. Keep toon filters light so the real costume still shows.

## Deliver

- `vertical(input, output)` → 1080x1920 for TikTok, Reels and Shorts. Check the crop keeps the face and prop.
- `side_by_side(raw_plate, final, output)` → before/after demo for showreels and pitch emails.
- Remind the user: label sponsored posts as ads, and follow platform AI-labelling rules if any element is AI-generated.

## Report

Output paths, the frames that got impact flashes, and the delivery sizes.
