"""Convert a COLMAP camera solve into Unreal Engine camera keys.

COLMAP stores, for each image, a world-to-camera rotation (quaternion
QW QX QY QZ) and translation (TX TY TZ):  X_cam = R * X_world + t.
Camera axes in COLMAP: +X right, +Y down, +Z forward (right-handed).

Unreal Engine: +X forward, +Y right, +Z up (left-handed), centimetres.

We map a COLMAP world vector v to UE as   (X, Y, Z) = (v.z, v.x, -v.y).
That matrix has determinant -1, so it also flips handedness, which is
what we need going from right-handed COLMAP to left-handed UE.

COLMAP's world has no gravity and an arbitrary scale. Fix both before
trusting a shot: run `colmap model_orientation_aligner`, or align in
Blender, and set `scale` from a measured distance in the plate.
Always prove the track with a test cube before rendering.
"""

from __future__ import annotations

import csv
import json
import math
import re
from dataclasses import asdict, dataclass
from pathlib import Path

Vec = tuple[float, float, float]


# ---------------------------------------------------------------- maths

def quat_to_matrix(qw: float, qx: float, qy: float, qz: float) -> list[list[float]]:
    """Unit quaternion (Hamilton, w first, as COLMAP writes it) to a 3x3 rotation."""
    n = math.sqrt(qw * qw + qx * qx + qy * qy + qz * qz)
    qw, qx, qy, qz = qw / n, qx / n, qy / n, qz / n
    return [
        [1 - 2 * (qy * qy + qz * qz), 2 * (qx * qy - qz * qw), 2 * (qx * qz + qy * qw)],
        [2 * (qx * qy + qz * qw), 1 - 2 * (qx * qx + qz * qz), 2 * (qy * qz - qx * qw)],
        [2 * (qx * qz - qy * qw), 2 * (qy * qz + qx * qw), 1 - 2 * (qx * qx + qy * qy)],
    ]


def colmap_to_ue_vec(v: Vec) -> Vec:
    return (v[2], v[0], -v[1])


def ue_to_colmap_vec(v: Vec) -> Vec:
    return (v[1], -v[2], v[0])


def _dot(a: Vec, b: Vec) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def ue_rotator_from_axes(forward: Vec, up: Vec) -> tuple[float, float, float]:
    """Pitch, yaw, roll in degrees, matching FRotationMatrix in UE's source."""
    yaw = math.atan2(forward[1], forward[0])
    pitch = math.atan2(forward[2], math.hypot(forward[0], forward[1]))
    sp, cp, sy, cy = math.sin(pitch), math.cos(pitch), math.sin(yaw), math.cos(yaw)
    right0 = (-sy, cy, 0.0)           # Y axis of the matrix at roll 0
    up0 = (-sp * cy, -sp * sy, cp)    # Z axis of the matrix at roll 0
    roll = math.atan2(_dot(up, right0), _dot(up, up0))
    return math.degrees(pitch), math.degrees(yaw), math.degrees(roll)


def ue_axes_from_rotator(pitch: float, yaw: float, roll: float) -> tuple[Vec, Vec, Vec]:
    """Forward, right, up axes of a UE FRotator (degrees). Used by the tests."""
    p, y, r = map(math.radians, (pitch, yaw, roll))
    sp, cp, sy, cy, sr, cr = math.sin(p), math.cos(p), math.sin(y), math.cos(y), math.sin(r), math.cos(r)
    fwd = (cp * cy, cp * sy, sp)
    right = (sr * sp * cy - cr * sy, sr * sp * sy + cr * cy, -sr * cp)
    up = (-(cr * sp * cy + sr * sy), cy * sr - cr * sp * sy, cr * cp)
    return fwd, right, up


# ---------------------------------------------------------------- parsing

@dataclass
class ColmapCamera:
    camera_id: int
    model: str
    width: int
    height: int
    params: list[float]

    @property
    def fx(self) -> float:
        return self.params[0]


@dataclass
class ColmapImage:
    image_id: int
    q: tuple[float, float, float, float]
    t: Vec
    camera_id: int
    name: str


def read_cameras_txt(path: str | Path) -> dict[int, ColmapCamera]:
    cams: dict[int, ColmapCamera] = {}
    for line in Path(path).read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        cams[int(parts[0])] = ColmapCamera(
            int(parts[0]), parts[1], int(parts[2]), int(parts[3]), [float(p) for p in parts[4:]]
        )
    return cams


def read_images_txt(path: str | Path) -> list[ColmapImage]:
    """images.txt has two lines per image; the second (2D points) may be empty."""
    lines = [ln for ln in Path(path).read_text().splitlines() if not ln.startswith("#")]
    images: list[ColmapImage] = []
    for i in range(0, len(lines), 2):
        parts = lines[i].split()
        if len(parts) < 10:
            continue
        images.append(ColmapImage(
            int(parts[0]),
            (float(parts[1]), float(parts[2]), float(parts[3]), float(parts[4])),
            (float(parts[5]), float(parts[6]), float(parts[7])),
            int(parts[8]),
            " ".join(parts[9:]),
        ))
    return images


# ---------------------------------------------------------------- conversion

@dataclass
class UeCameraKey:
    frame: int
    name: str
    x: float
    y: float
    z: float
    pitch: float
    yaw: float
    roll: float
    hfov_deg: float
    focal_mm_36: float  # focal length on a 36 mm wide filmback


def _frame_number(name: str, fallback: int) -> int:
    nums = re.findall(r"\d+", Path(name).stem)
    return int(nums[-1]) if nums else fallback


def convert(images: list[ColmapImage], cameras: dict[int, ColmapCamera], scale: float = 100.0) -> list[UeCameraKey]:
    """scale = UE centimetres per COLMAP unit (100 if one COLMAP unit is one metre)."""
    keys: list[UeCameraKey] = []
    for idx, img in enumerate(sorted(images, key=lambda im: im.name)):
        R = quat_to_matrix(*img.q)
        t = img.t
        # camera centre C = -R^T t
        c = tuple(-(R[0][k] * t[0] + R[1][k] * t[1] + R[2][k] * t[2]) for k in range(3))
        forward = (R[2][0], R[2][1], R[2][2])        # R^T * (0,0,1)
        up = (-R[1][0], -R[1][1], -R[1][2])          # R^T * (0,-1,0)
        pos = colmap_to_ue_vec(c)
        pitch, yaw, roll = ue_rotator_from_axes(colmap_to_ue_vec(forward), colmap_to_ue_vec(up))
        cam = cameras[img.camera_id]
        hfov = math.degrees(2 * math.atan(cam.width / (2 * cam.fx)))
        keys.append(UeCameraKey(
            frame=_frame_number(img.name, idx),
            name=img.name,
            x=pos[0] * scale, y=pos[1] * scale, z=pos[2] * scale,
            pitch=pitch, yaw=yaw, roll=roll,
            hfov_deg=hfov,
            focal_mm_36=36.0 * cam.fx / cam.width,
        ))
    keys.sort(key=lambda k: k.frame)
    return keys


def convert_folder(sparse_txt_dir: str | Path, out_path: str | Path, scale: float = 100.0) -> dict:
    """Read cameras.txt + images.txt, write .csv or .json. Returns a summary."""
    d = Path(sparse_txt_dir)
    keys = convert(read_images_txt(d / "images.txt"), read_cameras_txt(d / "cameras.txt"), scale)
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.suffix.lower() == ".json":
        out.write_text(json.dumps([asdict(k) for k in keys], indent=2))
    else:
        with out.open("w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(asdict(keys[0]).keys()) if keys else ["frame"])
            w.writeheader()
            for k in keys:
                w.writerow(asdict(k))
    frames = [k.frame for k in keys]
    gaps = sorted(set(range(min(frames), max(frames) + 1)) - set(frames)) if frames else []
    return {
        "output": str(out),
        "cameras_solved": len(keys),
        "first_frame": min(frames) if frames else None,
        "last_frame": max(frames) if frames else None,
        "missing_frames": gaps[:50],
        "missing_count": len(gaps),
        "note": "Scale and gravity are arbitrary in COLMAP. Prove the track with a test cube in UE.",
    }
