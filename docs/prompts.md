# Prompt library

**Status:** Working prompts for Claude (or any agent) with the `cosplay-vp` MCP server and skills installed. Each prompt follows the same loop: **direct → check → fix**. The agent does the work; you judge the result at each checkpoint.

Prompts go out of date as models and tools change. The checks don't. If a prompt stops working, open an issue with what you saw.

## 1. Project rulebook (CLAUDE.md)

Put this file in the root of your Unreal or footage project so the agent follows the same rules every session.

```markdown
# Project rules for the AI agent

## Units and conventions
- Unreal units are centimetres. 1 COLMAP unit = 1 m unless the shot sheet says otherwise.
- Frame rate for this project: 24 fps. Conform every clip before use.
- Folder layout: footage/raw, footage/conformed, frames/<shot>, mattes/<shot>, colmap/<shot>, renders/<shot>.

## How to build in Unreal
- Build sets from one Python script that deletes and rebuilds everything it made. Never hand-edit what the script owns.
- Tag every actor you create with "cvp" and the shot name.
- Show me a screenshot after each major step.

## Checkpoints (stop and ask me)
1. Matte edge over grey and bright backgrounds.
2. Test-cube track over the plate.
3. First comp frame before rendering.

## Never
- Never use characters, logos or music the client doesn't own or license in paid work.
- Never contact or process footage of anyone under 18 without a guardian consent form on file.
- Never delete raw footage.
```

## 2. Shot brief

```
Plan a shot with the cosplay-vp-shot-planner skill.
Character: [original / owned by client: ___]
Performer: [name], over 18: [yes/no]
Moment: [e.g. ultimate move, transformation, turn-to-camera reveal]
Length: [10–30 s], platform: [TikTok / Reels / Shorts / YouTube]
Set: [virtual environment], mood: [colour, time of day]
Gear: [phone model / camera], screen: [green / blue / none]
Give me the shot list, the camera checklist and anything that blocks us.
```

**Check:** every shot has one moment, a camera move that can be tracked, and the extras (clean plate, grey ball, measured distance).

## 3. Plate prep

```
Probe every clip in footage/raw. Conform them to 24 fps into footage/conformed.
Key take_03 with chroma_key to mattes/s03/keyed.mov and show me composite_preview
over a mid-grey and a bright still.
```

**Check:** hair, fingers, prop edges at 100%.
**If it goes wrong:**
- Green fringe → "Raise despill and lower similarity by 0.02, preview again."
- Hair chewed off → "Run matte_external with my RVM install: `<command>`, then preview."
- Flicker → "Use the AI matte for the whole shot and keep the key only as a garbage matte."

## 4. Camera track

```
Extract frames from footage/conformed/take_03.mp4 at 12 fps into frames/s03.
Solve with colmap_solve into colmap/s03. Then convert with colmap_to_ue.
The two floor markers are 2.00 m apart. Work out the scale and tell me how.
```

**Check:** solved frames / total, no big gaps, and in Unreal the test cube stays on the floor marker.
**If it goes wrong:**
- Several models → "Re-extract at 24 fps for the first 3 seconds only and solve again."
- Tilted world → "Run colmap model_orientation_aligner on the model, re-export, re-convert."
- Cube slides slowly → "Check the frame rate in Sequencer matches 24 and the plate is an image sequence."

## 5. Unreal comp

```
Using the cosplay-vp-unreal-comp skill: put mattes/s03 as a Media Plate behind TrackedCam,
match the main light to come from camera left like on set, add a contact shadow
from a capsule proxy, and add one foreground smoke card. Screenshot frame 48.
```

**Check:** does the performer look lit by the world, touching the floor, and inside the space?
**If it goes wrong:**
- Pasted-on look → "Lower plate saturation 10%, lift blacks to match the set, add a rim light in the set's sign colour."
- Floating → "Darken and tighten the contact shadow; move the proxy to the feet."

## 6. Anime FX and delivery

```
Apply on_twos to the action beat only (frames 30–70) of renders/s03/comp.mp4,
add impact_frames at 52 and 61 (white, 2 frames), then make a vertical 9:16 cut
and a side_by_side with footage/conformed/take_03.mp4.
```

**Check:** the hits land on the beat, the vertical crop keeps the face and prop, the side-by-side starts on the same frame.

## 7. Live booth plan

```
Use the cosplay-vp-live-booth skill. Event: [name], [hours], [visitors/hour], fixed camera,
venue Wi-Fi unknown, budget [___]. Recommend an architecture, list hardware,
and give a latency_budget with your estimates labelled as estimates.
```

**Check:** the plan starts with the simplest booth (Unreal + OBS key on one machine) unless a requirement rules it out.

## 8. Fix loop, any stage

```
This is wrong: [what you see, and a screenshot]. Don't guess.
Tell me the two most likely causes, test the cheaper one first, show me the result.
```
