# 06 Anime FX language

**Status:** Established craft. These are the moves that make live footage read as anime or a game cinematic.

## Timing

| Technique | What it is | How |
|---|---|---|
| On twos | Each drawing held for 2 frames at 24 fps: snappier, less smooth motion | `on_twos(hold=2)`; use 3 for a heavier, older look |
| Hit stop | Freeze for 2–6 frames on impact so the hit lands | Hold frames in the edit; pair with a camera shake after |
| Speed ramp | Fast into the pose, slow on the pose | Time remap in the editor |
| Anticipation | A small move the opposite way before the big move | Direct it on set, emphasise in the edit |

## Impact

| Technique | What it is | How |
|---|---|---|
| Impact frames | 1–3 frames of inverted, white or high-contrast image at the moment of impact | `impact_frames(frames=[...], length=2, mode="invert" or "white")` |
| Shockwave and speed lines | Radial lines or a ring from the impact point | After Effects, or Niagara / a card in Unreal |
| Smear | The weapon or limb stretched across a frame | Motion blur boosted on one frame, or a painted frame |
| Camera shake | Short, decaying shake after impact | Sequencer camera shake, or in post |

## The cut-in (ultimate / special move)

The signature of game cinematics: the action pauses, the character's face or pose appears in a panel, a name or move title slams in, then back to action.

1. Freeze or slow the action (hit stop).
2. Slide in a panel: the performer's close-up, matted, over a graphic background in the character's colours.
3. Title slam: move name scaled from 120% to 100% over 3–4 frames, with a flash.
4. Hold 12–24 frames, then cut back on an impact frame.

Shoot the close-up as its own take; the wide plate rarely has enough resolution.

## Grade

- Higher contrast and saturation than live action, with a strong colour key per character.
- Bloom on highlights and emissive props.
- Optional: a light outline or posterise effect. Use sparingly; a fully "toon" filter fights the real costume.

## Delivery

- `vertical` crops to 1080x1920 for TikTok, Reels and Shorts. Frame the action so the crop keeps the face and prop.
- `side_by_side` puts the raw plate next to the final: the most effective showreel and pitch format.
- Label paid posts as ads, and label any AI-generated elements where the platform requires it (doc 08).
