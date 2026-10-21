# 09 Open questions and benchmarks

**Status:** Open. These need practical tests; contributions with real numbers are welcome.

## Questions

1. What is the lowest achievable end-to-end latency with cloud GPU rendering?
2. What is the best way to send live camera video into cloud-hosted Unreal Engine?
3. Can green screen compositing be done entirely inside Unreal Engine for a live booth, without OBS?
4. How reliably can Aximmetry work with a remote rendering pipeline?
5. What GPU and network bandwidth does each architecture need?
6. Is a local GPU workstation cheaper than cloud rendering over a multi-day event?
7. Can a portable booth stay reliable on event Wi-Fi or a dedicated 5G link?
8. Which AI matting model gives the best hair edges on wigs and lace at 1080p, and at what speed?
9. How many frames per second does COLMAP need for a reliable solve of a 5-second handheld phone shot?

## How to report a benchmark

Open an issue or pull request adding a row to `benchmarks/results.csv` (create it if missing) with:

| Field | Example |
|---|---|
| date | 2026-11-02 |
| question | 1 |
| setup | Booth v0, RTX 4070 laptop, 1080p50 capture card, OBS 31 |
| method | Stopwatch filmed through system, 20 samples |
| result | median 112 ms, p95 140 ms |
| notes | Window capture; NDI added 30 ms |

Give the method. A number without a method can't be compared.
