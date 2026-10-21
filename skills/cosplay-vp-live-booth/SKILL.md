---
name: cosplay-vp-live-booth
description: Design a live "step into the anime" virtual production booth for events - choose between local Unreal + OBS, Aximmetry, or cloud Pixel Streaming, plan latency, hardware and visitor consent. Use when someone wants real-time cosplay CG at a convention, launch or activation.
---

# Cosplay VP live booth

Reference: `docs/07-live-booth-architectures.md`. Be clear about what is tested: Booth v0 and Architecture A are established; cloud (B) and hybrid (C) are hypotheses until benchmarked.

## 1. Ask the requirements

- Fixed camera or moving camera?
- How many visitors per hour, and clip length to take home?
- Power and internet at the venue (assume event Wi-Fi is unreliable).
- Budget for on-site hardware vs cloud.
- Effects: one background, or triggered cut-ins and impact overlays?

## 2. Recommend the simplest architecture that meets them

| Need | Recommend |
|---|---|
| Fixed camera, green screen, first event | Booth v0: Unreal background + OBS key on one GPU machine |
| Moving camera, tracking, several cameras | Aximmetry + Unreal (A) |
| Minimal on-site hardware, browser viewing | Cloud Unreal + Pixel Streaming (B), only after a latency test |
| Lowest latency | Local GPU |

Say plainly that Pixel Streaming does not take in a live camera feed by itself, and Aximmetry's composite isn't automatically available through Pixel Streaming.

## 3. Latency plan

Build a stage list and run `latency_budget(stages_ms, target_ms)`. Label every number as an estimate, then give the glass-to-glass test: film a stopwatch and the booth screen together, 20 samples, report median and worst.

## 4. Booth checklist

- GPU machine plus a spare, capture card, camera on a fixed mount, green screen with even light.
- OBS scene: Unreal background (NDI or window capture), keyed camera, effect overlays on hotkeys or a foot pedal, recording to a per-visitor file.
- Export each clip with `vertical`; hand it over by QR code or AirDrop.
- Visitor consent: signage before entry, ask before posting anyone, delete raw footage after the event unless they opted in. Guardians for minors.

## 5. Report

Architecture chosen and why, hardware list, latency estimate table, and the test plan. Point to `docs/09-open-questions-and-benchmarks.md` for how to share measured results.
