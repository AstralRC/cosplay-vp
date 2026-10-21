# 03 Matting and keying

**Status:** Established. Tool licences differ a lot here; see the table at the end.

You need the performer as a clip with a clean alpha channel. There are two routes, and the best result often combines them.

## Chroma key (green or blue screen)

- Fast, predictable and free. `chroma_key` gives a first-pass key with ffmpeg (`chromakey` plus `despill`) and writes ProRes 4444, VP9 with alpha, or a PNG sequence.
- Tune `similarity` up until the screen is gone, and `blend` up to soften the edge. Then check hair and lace at 100% zoom.
- For finals, key in a compositor with proper edge tools: Unreal Composure, Blender, DaVinci Resolve or After Effects.

## AI matting (no screen needed)

Video matting models separate a person from any background:

| Model | Strength | Licence (check before commercial use) |
|---|---|---|
| Robust Video Matting (RVM) | Fast, temporally stable, good for people | GPL-3.0 |
| MatAnyone | Strong on hair; follows a target from a first-frame mask | NTU S-Lab License 1.0 (read its terms; S-Lab licences usually restrict commercial use) |

This repo doesn't bundle any model. `matte_external` runs whatever you installed with a command template, for example:

```
matte_external(input="plate.mp4", output="matte.mp4",
  command_template="python inference.py --input-source {input} --output-alpha {output}")
```

## Hybrid that works well

1. Shoot on a screen anyway.
2. Run the chroma key for the body and the AI matte for hair and fast motion.
3. Combine: take the AI matte where the key fails (hair, motion blur), the key elsewhere.
4. Despill last, after the matte is final.

## Problems and fixes

| Problem | Fix |
|---|---|
| Green fringe on hair | Despill, then a light edge colour correction toward the virtual set's colours |
| Costume is close to the key colour | Switch screen colour; or AI matte that region |
| Props held over the body (weapons, wands) | Make sure the model sees the prop in the first-frame mask; or rotoscope the prop |
| Flicker between frames | AI models with temporal memory (RVM, MatAnyone) flicker less than per-frame keys |
| Motion blur edges | A faster shutter on set (doc 02); keep some blur in the matte for realism |
| Hands crossing the face or other people | Hand-over masks: paint a few keyframes and let the model propagate |

## Check before moving on

Run `composite_preview` over a mid-grey still and over a bright still. Look at hair, fingers and prop edges. A matte that only looks right on one background isn't finished.
