---
name: cosplay-vp-shot-planner
description: Plan a CG cosplay virtual production shot or campaign - character moment, shot sheet, camera settings, consent and character-rights check. Use first, before any filming, when someone wants a cosplay CG video, anime cut-in, or virtual production shoot.
---

# Cosplay VP shot planner

You turn an idea ("make my cosplay look like the character's ultimate move") into shots that can be filmed and finished. This is the entry point of the cosplay-vp pipeline; the other skills pick up after filming.

## 1. Check rights and consent first

Ask, and record the answers on the shot sheet:
- Who owns the character? Paid or sponsored work must use a character the client owns or licensed, or an original one. Fan work stays unpaid.
- Is every performer 18 or over? If not: guardian consent form, payment through the guardian, age-appropriate brief only.
- Where will it be posted, and is it an ad? (It must be labelled.)

If paid work depends on a character nobody licensed, say so and suggest an original or client-owned character. Don't continue planning a paid piece around it.

## 2. Find the one moment

A short piece lands on one moment, not a story. Ask for, or propose, one of:
- the ultimate / special move (cut-in, title slam, impact)
- a transformation (before costume → after, on a match cut)
- the turn-to-camera reveal
- a weapon hit or smash past camera

## 3. Write the shot list

3–6 shots, each 2–5 s, for a 10–30 s piece. For each shot fill the sheet in `docs/02-shooting-the-plate.md`: moment, duration, camera move, screen colour, virtual set, light direction, extras (clean plate, grey ball, measured distance).

Rules of thumb:
- Shoot the cut-in close-up as its own take.
- Handheld push-ins track well; whip pans and zooms don't.
- Plan one locked-off shot: it needs no tracking and saves the edit if a solve fails.

## 4. Give the camera checklist

Fixed 24 or 25 fps, shutter about 1/100, exposure/focus/white balance locked, stabilisation off, no zoom, highest bitrate, markers on screen and floor, performer 2–3 m from the screen. Full table: `docs/02-shooting-the-plate.md`.

## 5. Hand off

Output: the shot sheet as a table, the camera checklist, and the rights/consent status. Then point to the next skills: `cosplay-vp-plate-prep` after filming, then `cosplay-vp-camera-track`, `cosplay-vp-unreal-comp`, `cosplay-vp-anime-fx`. For a live event booth use `cosplay-vp-live-booth` instead.

If the `cosplay-vp` MCP server is connected, its `knowledge` tool returns any doc page by name.
