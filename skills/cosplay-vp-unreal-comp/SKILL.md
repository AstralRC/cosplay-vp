---
name: cosplay-vp-unreal-comp
description: Composite a matted cosplay plate into an Unreal Engine 5 set - media plate or Composure, lens and light matching, contact shadows, foreground depth, Movie Render Queue settings. Use when keyed or matted cosplay footage needs to sit inside a virtual environment.
---

# Cosplay VP Unreal comp

Reference: `docs/05-unreal-compositing.md`. Panel names vary across UE 5 versions; check the user's version before giving exact clicks.

## Inputs to confirm

- Matted plate as an image sequence with alpha (PNG/EXR preferred over video).
- Tracked camera (from `cosplay-vp-camera-track`) or, for locked-off shots, the real lens and camera height.
- The virtual set and the direction of the real key light (shot sheet).

## Steps

1. Bring the plate in: Media Plate actor for simple shots; Composure when layering CG, mattes and passes.
2. Match the lens: the camera's focal length and filmback from the solve.
3. Match light: main light from the same side as on set, using the grey ball reference. Grade the plate toward the world: black level, white balance, saturation, then edge colour.
4. Ground the performer: contact shadow from a proxy shape, or a separate shadow pass. A floating performer is the most common giveaway.
5. Add depth: at least one foreground element in front of the performer (smoke, debris, a pillar edge).
6. Render with Movie Render Queue at the plate's frame rate, image sequence output, higher anti-aliasing for motion. Render CG and plate separately if finishing in After Effects or Resolve.

## Working through an Unreal MCP server

If an Unreal MCP server is connected: build the set from one re-runnable script, tag every actor you create, and send a screenshot after placing the plate, after light matching and before rendering. The user approves before the render is queued.

## Report

Screenshot or frame path, what was matched (lens, light, grade, shadow), and open issues. Next: `cosplay-vp-anime-fx`.
