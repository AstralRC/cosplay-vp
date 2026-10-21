# 02 Shooting the plate

**Status:** Established practice. Most problems later in the pipeline start here, and are cheaper to fix on set than in post.

## Phone or camera settings

| Setting | Use | Why |
|---|---|---|
| Frame rate | Fixed 24 or 25 fps (30 if the platform needs it) | Phones default to variable frame rate, which breaks tracking and sync |
| Shutter | About 1/100 s at 24–25 fps, faster for action | Less motion blur gives cleaner mattes and more trackable frames |
| Exposure, focus, white balance | All locked | Auto changes flicker the key and confuse the tracker |
| Stabilisation | Off for tracked shots | Digital stabilisation warps the image, so the solve won't match |
| Lens | One lens, no zoom during the take | A changing focal length is much harder to solve |
| HDR, night mode, beauty filters | Off | They change frame to frame |
| Codec | Highest bitrate the device allows, ProRes or 10-bit HEVC if available | Compression blocks ruin hair edges |

On phones, a manual camera app (for example the free Blackmagic Camera app on iOS and Android) gives you these locks.

Run `probe` on every clip as soon as it comes off the device. It warns about variable frame rate and rotation flags.

## Screen and lighting

- **Light the screen and the performer separately.** Even light on the screen; the performer lit to match the virtual set's key direction.
- **Distance.** Keep the performer 2–3 m in front of the screen to cut green spill on costumes and hair.
- **Colour.** Green suits most costumes. Use blue for green costumes, wigs or props.
- **Rim light** behind the performer helps separate hair and lace from the background.
- **No screen?** AI matting (doc 03) works on ordinary backgrounds, but a plain, uncluttered wall still gives cleaner edges.

## Make it trackable

- Put **tracking markers** (tape crosses, 10–20 cm apart) on the screen and floor, away from the performer's outline.
- Shoot with **parallax**: a slight move left or right or forward. A camera that only pans on a tripod can't be solved in 3D; that needs a nodal solve.
- Avoid fast whip pans on phones. Rolling shutter skews the frame.

## Shoot extra

| Extra | Why |
|---|---|
| Clean plate: 3–5 s of the empty set, same camera move if possible | Prop removal, matte repair, light reference |
| Grey ball and colour chart in frame for a second | Match light direction and colour in Unreal |
| Measure one real distance (floor marker to marker) | Sets the scale of the camera solve |
| Phone gyro/IMU log if your app records it | A fallback when the visual solve fails |

## Shot sheet (one per shot)

```
Shot:            S03 "ultimate" cut-in
Character:       [owned or licensed by: ______ ]
Performer:       [name]  consent form: [yes]  under 18: [no / guardian form]
Moment:          turn to camera, raise weapon, freeze 4 frames, flash
Duration:        4 s
Camera:          handheld push-in 50 cm, eye height, 24 fps, 1/100, ISO locked
Screen / BG:     green, markers on floor
Virtual set:     [scene name], key light from camera left
Extras:          clean plate, grey ball, distance A–B = 2.00 m
```
