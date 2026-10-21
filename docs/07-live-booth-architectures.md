# 07 Live booth architectures

**Status:** Partly hypothesis. Architecture A is established. B and C are design ideas that still need proof-of-concept testing.

**The booth:** visitors stand in front of a camera (and usually a green screen) and see themselves inside a virtual anime or game environment, live, and leave with a short clip.

## Aximmetry and Pixel Streaming solve different problems

[Aximmetry](https://aximmetry.com/) is virtual production software for real-time compositing, camera tracking, green screen, virtual studios and LED walls. It works with Unreal Engine: Unreal renders the world, Aximmetry runs the live production.

[Pixel Streaming](https://github.com/EpicGamesExt/PixelStreamingInfrastructure) streams Unreal Engine's rendered output to a web browser, which lets the rendering GPU sit somewhere else.

| Capability | Aximmetry | Pixel Streaming |
|---|---|---|
| Main function | Virtual production | Remote delivery of Unreal rendering |
| Green screen compositing | Yes | Not built in |
| Camera tracking | Yes, with compatible hardware | Not built in |
| Unreal Engine integration | Yes | Native Unreal feature |
| Browser video delivery | Needs a separate streaming setup | Yes |
| Cloud GPU deployment | Needs custom infrastructure | Common deployment model |
| Removes the need for a local GPU | No | Can move rendering to a remote GPU |

**They are complementary, not replacements.** Aximmetry produces the virtual scene. Pixel Streaming delivers Unreal output to remote viewers.

## Booth v0: the simplest thing that works (start here)

Fixed camera, no tracking, one GPU laptop or desktop.

```
Camera ─► capture card ─► OBS (chroma key) ─┐
                                            ├─► OBS scene ─► screen + recording
Unreal Engine (live background, fixed cam) ─┘   (window capture or NDI)
```

- Unreal renders the set from a camera matched to the real camera's height and lens.
- OBS keys the camera feed and layers it over the Unreal output. Use NDI or window capture to bring Unreal into OBS.
- Effects: trigger a pre-rendered cut-in or impact overlay from a hotkey or a foot pedal.
- Output: the booth screen, plus a 10–15 s recording per visitor exported with `vertical`.

## Architecture A: local virtual production

```
Camera ─► Aximmetry + Unreal Engine ─► OBS ─► display / recording
```

- **Pros:** no internet round-trip; camera and render stay in sync; supports compositing and tracking.
- **Cons:** needs a powerful GPU workstation on site; more equipment to transport.
- **Best for:** professional production and latency-sensitive booths.

## Architecture B: cloud Unreal + Pixel Streaming (hypothesis)

```
Camera ─► video uplink ─► cloud GPU running Unreal ─► Pixel Streaming ─► booth display
```

- **Pros:** possibly lighter hardware on site; browser-based viewing.
- **Challenges:** Pixel Streaming does not take in a live camera feed by itself, so you need a custom camera transport and compositing path. Event internet is unreliable. Round-trip latency reduces responsiveness.
- **Best for:** portable installations where cloud rendering matters and some delay is acceptable.

## Architecture C: hybrid Aximmetry + cloud Unreal (experimental)

```
Camera ─► local Aximmetry / keying ─► network video ─► cloud Unreal ─► Pixel Streaming ─► display
```

- **Pros:** separates capture on site from rendering remotely.
- **Challenges:** complex synchronisation and networking; custom integration; bandwidth and latency. Aximmetry's final composite is not automatically available through Pixel Streaming.

## Choosing

| Requirement | Approach |
|---|---|
| Fixed-camera green screen booth | Booth v0: Unreal + OBS key |
| Professional moving-camera production | Aximmetry + Unreal (A) |
| Lightweight booth hardware | Cloud Unreal + Pixel Streaming (B), after testing |
| Lowest latency | Local GPU rendering |
| Several cameras and tracking | Consider Aximmetry |
| Interactive browser experience | Pixel Streaming |

## Latency budget

Use `latency_budget` to plan, then measure glass-to-glass: film a running stopwatch and the booth screen in one shot and compare.

```
latency_budget({"camera + capture": 50, "key": 10, "unreal render": 17, "obs compose": 17, "display": 25}, target_ms=150)
```

These example numbers are placeholders, not measurements.

## Roadmap

1. **Local prototype:** one Unreal environment, a live camera feed, green screen compositing, display and record, measure latency and frame rate.
2. **Cloud experiment:** Unreal on a cloud GPU, Pixel Streaming, a camera uplink; test round-trip latency and stability against the local prototype.
3. **Advanced:** evaluate Aximmetry for tracking and compositing, interactive effects, several cameras, event-ready hardware.

**Start with the simplest Unreal prototype. Add Pixel Streaming or Aximmetry only when a specific requirement justifies the complexity.**
