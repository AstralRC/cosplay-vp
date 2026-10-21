"""Run the ffmpeg tools on a synthetic green-screen clip. Skipped if ffmpeg is missing."""

import shutil
import subprocess

import pytest

from cosplay_vp import media

pytestmark = pytest.mark.skipif(not shutil.which("ffmpeg"), reason="ffmpeg not installed")


@pytest.fixture(scope="module")
def clips(tmp_path_factory):
    d = tmp_path_factory.mktemp("clips")
    green = d / "green.mp4"
    # a moving red box on pure green, 2 s at 24 fps
    subprocess.run([
        "ffmpeg", "-y", "-f", "lavfi", "-i", "color=c=0x00FF00:s=640x360:r=24:d=2",
        "-vf", "drawbox=x='t*120':y=100:w=120:h=160:c=red:t=fill",
        "-pix_fmt", "yuv420p", str(green)], check=True, capture_output=True)
    bg = d / "bg.png"
    subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "testsrc=s=640x360", "-frames:v", "1", str(bg)],
                   check=True, capture_output=True)
    return d, green, bg


def test_probe(clips):
    _, green, _ = clips
    info = media.probe(str(green))
    assert (info["width"], info["height"]) == (640, 360)
    assert info["fps"] == 24
    assert not info["has_alpha"]


def test_key_composite_and_fx(clips):
    d, green, bg = clips
    keyed = d / "keyed.mov"
    media.chroma_key(str(green), str(keyed))
    assert media.probe(str(keyed))["has_alpha"]
    comp = d / "comp.mp4"
    media.composite_preview(str(keyed), str(bg), str(comp), height=360)
    assert comp.stat().st_size > 0
    twos = d / "twos.mp4"
    media.on_twos(str(comp), str(twos))
    assert media.probe(str(twos))["fps"] == 24
    hit = d / "hit.mp4"
    media.impact_frames(str(twos), str(hit), frames=[10, 30])
    sbs = d / "sbs.mp4"
    media.side_by_side(str(green), str(hit), str(sbs), height=360)
    assert media.probe(str(sbs))["width"] == 1280
    vert = d / "vert.mp4"
    media.vertical(str(sbs), str(vert), 540, 960)
    assert (media.probe(str(vert))["width"], media.probe(str(vert))["height"]) == (540, 960)


def test_extract_frames(clips):
    d, green, _ = clips
    res = media.extract_frames(str(green), str(d / "frames"), fps=12)
    assert res["frames"] == 24
    assert (d / "frames" / "00001.jpg").exists()


def test_latency_budget():
    r = media.latency_budget({"camera": 33, "key": 8, "render": 16, "display": 30}, target_ms=100)
    assert r["total_ms"] == 87 and r["within_target"] and r["largest_stage"] == "camera"


def test_missing_tool_message(monkeypatch):
    monkeypatch.setattr(media.shutil, "which", lambda _: None)
    with pytest.raises(media.ToolMissing):
        media.colmap_solve("x", "y")
