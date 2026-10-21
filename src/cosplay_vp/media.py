"""Thin, testable wrappers around ffmpeg / ffprobe / COLMAP command lines.

Every function builds an argument list (never a shell string), runs it,
and returns a plain dict so it can be used from the MCP server, a script
or a notebook.
"""

from __future__ import annotations

import json
import shlex
import shutil
import subprocess
from fractions import Fraction
from pathlib import Path

class ToolMissing(RuntimeError):
    pass


def _need(binary: str, hint: str) -> str:
    path = shutil.which(binary)
    if not path:
        raise ToolMissing(f"'{binary}' was not found on PATH. {hint}")
    return path


def _run(args: list[str], timeout: int = 3600) -> subprocess.CompletedProcess:
    proc = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
    if proc.returncode != 0:
        tail = (proc.stderr or proc.stdout)[-2000:]
        raise RuntimeError(f"Command failed ({proc.returncode}): {' '.join(args[:6])} ...\n{tail}")
    return proc


def _ffmpeg() -> str:
    return _need("ffmpeg", "Install ffmpeg: https://ffmpeg.org/download.html")


def _alpha_output_args(output: str) -> list[str]:
    """Codec settings that keep an alpha channel, chosen from the output extension."""
    ext = Path(output).suffix.lower()
    if ext == ".mov":
        return ["-c:v", "prores_ks", "-profile:v", "4444", "-pix_fmt", "yuva444p10le"]
    if ext == ".webm":
        return ["-c:v", "libvpx-vp9", "-pix_fmt", "yuva420p", "-b:v", "0", "-crf", "20"]
    if ext == ".png":  # image sequence such as out/%05d.png
        return ["-pix_fmt", "rgba"]
    raise ValueError("Alpha output must be .mov (ProRes 4444), .webm (VP9) or a %05d.png sequence")


# ---------------------------------------------------------------- inspect

def probe(path: str) -> dict:
    """Resolution, frame rate, duration, codec and rotation of a clip."""
    ffprobe = _need("ffprobe", "ffprobe ships with ffmpeg.")
    out = _run([ffprobe, "-v", "error", "-print_format", "json", "-show_streams", "-show_format", path]).stdout
    data = json.loads(out)
    video = next((s for s in data.get("streams", []) if s.get("codec_type") == "video"), None)
    if not video:
        return {"path": path, "error": "no video stream"}
    fps = float(Fraction(video.get("avg_frame_rate") or video.get("r_frame_rate") or "0/1")) if video.get("avg_frame_rate") not in (None, "0/0") else None
    rotation = 0
    for sd in video.get("side_data_list", []) or []:
        if "rotation" in sd:
            rotation = int(sd["rotation"])
    rotation = int(video.get("tags", {}).get("rotate", rotation))
    duration = float(data.get("format", {}).get("duration", video.get("duration", 0)) or 0)
    warnings = []
    if fps and abs(fps - round(fps)) > 0.01 and abs(fps - 23.976) > 0.01 and abs(fps - 29.97) > 0.01:
        warnings.append("Unusual or variable frame rate: phone clips often are. Conform to a fixed rate before tracking.")
    if rotation:
        warnings.append(f"Clip carries a {rotation} degree rotation flag; ffmpeg applies it, some trackers do not.")
    return {
        "path": path,
        "width": video.get("width"),
        "height": video.get("height"),
        "fps": round(fps, 3) if fps else None,
        "duration_s": round(duration, 3),
        "frames_estimate": int(round(duration * fps)) if fps else None,
        "codec": video.get("codec_name"),
        "pix_fmt": video.get("pix_fmt"),
        "rotation": rotation,
        "has_alpha": any(k in (video.get("pix_fmt") or "") for k in ("yuva", "rgba", "argb", "bgra", "abgr", "gbrap", "ya8", "ya16")),
        "warnings": warnings,
    }


# ---------------------------------------------------------------- prep

def conform(input: str, output: str, fps: float = 24.0) -> dict:
    """Constant frame rate, rotation baked in, high-quality H.264. Run this first on phone footage."""
    _run([_ffmpeg(), "-y", "-i", input, "-vf", f"fps={fps}", "-c:v", "libx264", "-crf", "14",
          "-preset", "slow", "-pix_fmt", "yuv420p", "-c:a", "aac", output])
    return {"output": output, "fps": fps}


def extract_frames(input: str, out_dir: str, fps: float | None = None, start: float | None = None,
                   duration: float | None = None, ext: str = "jpg") -> dict:
    """Frames for COLMAP or matting. Names are 00001.jpg, 00002.jpg ... so frame numbers survive."""
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    args = [_ffmpeg(), "-y"]
    if start is not None:
        args += ["-ss", str(start)]
    args += ["-i", input]
    if duration is not None:
        args += ["-t", str(duration)]
    if fps:
        args += ["-vf", f"fps={fps}"]
    if ext == "jpg":
        args += ["-qscale:v", "2"]
    args += ["-start_number", "1", str(Path(out_dir) / f"%05d.{ext}")]
    _run(args)
    count = len(list(Path(out_dir).glob(f"*.{ext}")))
    return {"out_dir": out_dir, "frames": count}


# ---------------------------------------------------------------- keying and matting

def chroma_key(input: str, output: str, color: str = "0x00FF00", similarity: float = 0.12,
               blend: float = 0.06, despill: bool = True) -> dict:
    """Green or blue screen key to a clip with alpha. A fast first pass, not a final key."""
    vf = f"chromakey={color}:{similarity}:{blend}"
    if despill:
        kind = "blue" if color.lower() in ("0x0000ff", "#0000ff", "blue") else "green"
        vf += f",format=rgba,despill=type={kind}"
    _run([_ffmpeg(), "-y", "-i", input, "-vf", vf, *_alpha_output_args(output), output])
    return {"output": output, "filter": vf}


def matte_external(input: str, output: str, command_template: str) -> dict:
    """Run an AI matting tool you installed yourself (RVM, MatAnyone, ...).

    command_template uses {input} and {output}, for example:
      "python inference.py --input-source {input} --output-composition {output}"
    These models have their own licences (RVM: GPL-3.0, MatAnyone: NTU S-Lab
    License 1.0). They are not bundled; check the licence before commercial use.
    """
    args = [a.format(input=input, output=output) for a in shlex.split(command_template)]
    proc = _run(args, timeout=6 * 3600)
    return {"output": output, "command": args, "log_tail": proc.stdout[-800:]}


def composite_preview(foreground: str, background: str, output: str, height: int = 1080) -> dict:
    """Quick look: alpha foreground over a still or video background. Final comps happen in UE."""
    fc = (f"[1:v]scale=-2:{height}[bg];[0:v]scale=-2:{height}[fg];"
          f"[bg][fg]overlay=(W-w)/2:H-h:shortest=1,format=yuv420p")
    fps = probe(foreground).get("fps") or 24
    is_still = Path(background).suffix.lower() in (".png", ".jpg", ".jpeg", ".exr")
    bg_args = ["-loop", "1", "-framerate", str(fps), "-i", background] if is_still else ["-i", background]
    _run([_ffmpeg(), "-y", "-i", foreground, *bg_args, "-filter_complex", fc, "-c:v", "libx264", "-crf", "16", output])
    return {"output": output}


# ---------------------------------------------------------------- anime language

def on_twos(input: str, output: str, hold: int = 2, fps: float | None = None) -> dict:
    """Hold every frame for `hold` frames (anime 'on twos') while keeping the clip's frame rate."""
    src_fps = fps or probe(input)["fps"] or 24.0
    _run([_ffmpeg(), "-y", "-i", input, "-vf", f"fps={src_fps / hold},fps={src_fps}",
          "-c:v", "libx264", "-crf", "14", "-pix_fmt", "yuv420p", "-an", output])
    return {"output": output, "held_frames": hold, "fps": src_fps}


def impact_frames(input: str, output: str, frames: list[int], length: int = 2, mode: str = "invert") -> dict:
    """Flash 'impact frames' at the given frame numbers: invert colours or go full white."""
    if not frames:
        raise ValueError("Give at least one frame number")
    enable = "+".join(f"between(n,{f},{f + length - 1})" for f in frames)
    vf = f"negate=enable='{enable}'" if mode == "invert" else f"drawbox=c=white@1:t=fill:enable='{enable}'"
    _run([_ffmpeg(), "-y", "-i", input, "-vf", vf, "-c:v", "libx264", "-crf", "14", "-pix_fmt", "yuv420p", "-c:a", "copy", output])
    return {"output": output, "frames": frames, "length": length, "mode": mode}


# ---------------------------------------------------------------- delivery

def side_by_side(before: str, after: str, output: str, height: int = 1080) -> dict:
    """Raw plate next to the finished shot: the demo every pitch email links to."""
    fc = f"[0:v]scale=-2:{height},setsar=1[a];[1:v]scale=-2:{height},setsar=1[b];[a][b]hstack=inputs=2:shortest=1,format=yuv420p"
    _run([_ffmpeg(), "-y", "-i", before, "-i", after, "-filter_complex", fc, "-c:v", "libx264", "-crf", "18", "-an", output])
    return {"output": output}


def vertical(input: str, output: str, width: int = 1080, height: int = 1920) -> dict:
    """Fill-crop to 9:16 for TikTok, Reels and Shorts."""
    vf = f"scale={width}:{height}:force_original_aspect_ratio=increase,crop={width}:{height},setsar=1"
    _run([_ffmpeg(), "-y", "-i", input, "-vf", vf, "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", output])
    return {"output": output, "size": f"{width}x{height}"}


# ---------------------------------------------------------------- camera solve

def colmap_solve(image_dir: str, workspace: str, quality: str = "medium", single_camera: bool = True) -> dict:
    """Sparse COLMAP reconstruction of a frame folder, exported as TXT for colmap_to_ue."""
    colmap = _need("colmap", "Install COLMAP: https://colmap.github.io/install.html")
    ws = Path(workspace)
    ws.mkdir(parents=True, exist_ok=True)
    _run([colmap, "automatic_reconstructor", "--workspace_path", str(ws), "--image_path", image_dir,
          "--data_type", "video", "--quality", quality, "--single_camera", "1" if single_camera else "0",
          "--dense", "0"], timeout=12 * 3600)
    models = sorted((ws / "sparse").glob("*/cameras.bin"))
    if not models:
        return {"ok": False, "error": "COLMAP produced no model. Try more texture in frame, less motion blur, or more frames."}
    best = max(models, key=lambda p: (p.parent / "images.bin").stat().st_size).parent
    txt = ws / "sparse_txt"
    txt.mkdir(exist_ok=True)
    _run([colmap, "model_converter", "--input_path", str(best), "--output_path", str(txt), "--output_type", "TXT"])
    return {"ok": True, "model": str(best), "txt_dir": str(txt), "models_found": len(models),
            "note": "Several models means the solve broke into pieces; the largest was exported."}


# ---------------------------------------------------------------- booth

def latency_budget(stages_ms: dict[str, float], target_ms: float = 100.0) -> dict:
    """Add up per-stage latency for a live booth and compare with a target."""
    total = sum(stages_ms.values())
    worst = max(stages_ms, key=stages_ms.get) if stages_ms else None
    return {
        "total_ms": round(total, 1),
        "target_ms": target_ms,
        "within_target": total <= target_ms,
        "largest_stage": worst,
        "stages": stages_ms,
        "note": "Estimates are only a plan. Measure glass-to-glass by filming a stopwatch through the system.",
    }
