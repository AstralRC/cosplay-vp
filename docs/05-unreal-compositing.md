# 05 Unreal compositing

**Status:** Established. Exact panel names vary between Unreal Engine 5 versions; check against your version.

The goal is that the performer looks lit by, and standing in, the virtual world.

## Getting the plate into Unreal

| Method | Good for |
|---|---|
| Media Plate actor (UE 5.1+) | The simplest way to show a video or image sequence in the level |
| Composure plugin | Layered comps: plate, CG, mattes and colour passes, with a live preview |
| Card in the world | A textured plane placed in 3D, useful for 2.5D shots and depth effects |

Use an image sequence with alpha (PNG or EXR) for final renders; video files can drift a frame in Movie Render Queue.

## Make it sit in the world

1. **Match the lens.** The tracked camera's focal length and filmback come from the solve (doc 04).
2. **Match the light.** Point the main virtual light the way the real key light came from; use the grey ball from set as reference.
3. **Grade the plate toward the world.** Black level, white balance and saturation first; a little of the set's ambient colour on the performer's edges.
4. **Contact shadows.** A performer with no shadow floats. Options: a shadow from a proxy shape (capsule or rough mesh following the performer), or a shadow pass composited over the plate. In recent UE 5 versions, holdout and alpha output in Movie Render Queue help separate passes.
5. **Rim and spill from the world.** If the set has a bright sign behind the performer, add a matching edge light in the comp.
6. **Depth.** Put foreground CG in front of the performer (smoke, debris, a pillar edge) so they are inside the space, not on top of it.

## Rendering

- Render with Movie Render Queue: fixed frame rate matching the plate, anti-aliasing samples raised for motion.
- Render CG and plate separately when you plan to finish in After Effects or DaVinci Resolve. Render the final comp in Unreal when it's a fast turnaround.
- Keep one test-cube render per shot in the project folder as proof of the track.

## Using an AI agent with Unreal

If you run an Unreal MCP server (several open-source projects exist), the agent can place the media plate, import the camera CSV and queue renders. Keep these rules:

- One script builds the set and can be re-run: the agent edits the script, not the level by hand.
- Tag everything the agent creates so it can be found and rebuilt.
- The agent shows a screenshot at each checkpoint; a person approves before render.
