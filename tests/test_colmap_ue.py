"""Round-trip tests: build COLMAP data from a known UE camera, convert back, compare."""

import math

import pytest

from cosplay_vp import colmap_ue as cu


def _matrix_to_quat(R):
    tr = R[0][0] + R[1][1] + R[2][2]
    if tr > 0:
        s = math.sqrt(tr + 1.0) * 2
        return (0.25 * s, (R[2][1] - R[1][2]) / s, (R[0][2] - R[2][0]) / s, (R[1][0] - R[0][1]) / s)
    if R[0][0] > R[1][1] and R[0][0] > R[2][2]:
        s = math.sqrt(1.0 + R[0][0] - R[1][1] - R[2][2]) * 2
        return ((R[2][1] - R[1][2]) / s, 0.25 * s, (R[0][1] + R[1][0]) / s, (R[0][2] + R[2][0]) / s)
    if R[1][1] > R[2][2]:
        s = math.sqrt(1.0 + R[1][1] - R[0][0] - R[2][2]) * 2
        return ((R[0][2] - R[2][0]) / s, (R[0][1] + R[1][0]) / s, 0.25 * s, (R[1][2] + R[2][1]) / s)
    s = math.sqrt(1.0 + R[2][2] - R[0][0] - R[1][1]) * 2
    return ((R[1][0] - R[0][1]) / s, (R[0][2] + R[2][0]) / s, (R[1][2] + R[2][1]) / s, 0.25 * s)


def colmap_image_from_ue(loc_cm, pitch, yaw, roll, scale=100.0, name="00001.jpg"):
    fwd, right, up = cu.ue_axes_from_rotator(pitch, yaw, roll)
    # camera axes expressed in COLMAP world: x=right, y=down, z=forward
    x = cu.ue_to_colmap_vec(right)
    y = cu.ue_to_colmap_vec(tuple(-u for u in up))
    z = cu.ue_to_colmap_vec(fwd)
    R = [list(x), list(y), list(z)]  # world-to-camera rows
    C = cu.ue_to_colmap_vec(tuple(v / scale for v in loc_cm))
    t = tuple(-(R[i][0] * C[0] + R[i][1] * C[1] + R[i][2] * C[2]) for i in range(3))
    return cu.ColmapImage(1, _matrix_to_quat(R), t, 1, name)


CASES = [
    ((0, 0, 150), 0, 0, 0),
    ((120, -340, 165), -8, 35, 0),
    ((-500, 220, 90), 12, -120, 6),
    ((10, 10, 300), -45, 170, -15),
    ((0, 0, 100), 30, 90, 25),
]


@pytest.mark.parametrize("loc,pitch,yaw,roll", CASES)
def test_round_trip(loc, pitch, yaw, roll):
    cam = cu.ColmapCamera(1, "PINHOLE", 1920, 1080, [1500.0, 1500.0, 960.0, 540.0])
    key = cu.convert([colmap_image_from_ue(loc, pitch, yaw, roll)], {1: cam})[0]
    assert (key.x, key.y, key.z) == pytest.approx(loc, abs=1e-6)
    assert key.pitch == pytest.approx(pitch, abs=1e-6)
    assert key.yaw == pytest.approx(yaw, abs=1e-6)
    assert key.roll == pytest.approx(roll, abs=1e-6)


def test_fov_and_focal():
    cam = cu.ColmapCamera(1, "SIMPLE_RADIAL", 1920, 1080, [1662.77, 960, 540, 0.01])
    key = cu.convert([colmap_image_from_ue((0, 0, 0), 0, 0, 0)], {1: cam})[0]
    assert key.hfov_deg == pytest.approx(60.0, abs=0.01)
    assert key.focal_mm_36 == pytest.approx(36 * 1662.77 / 1920)


def test_handedness_flip():
    m = [[0, 0, 1], [1, 0, 0], [0, -1, 0]]
    det = (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
           - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
           + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))
    assert det == -1


def test_read_txt_and_convert(tmp_path):
    (tmp_path / "cameras.txt").write_text("# Camera list\n1 PINHOLE 1920 1080 1500 1500 960 540\n")
    lines = ["# Image list"]
    for i, (loc, p, y, r) in enumerate(CASES, start=1):
        img = colmap_image_from_ue(loc, p, y, r, name=f"{i:05d}.jpg")
        lines.append(f"{i} {' '.join(map(str, img.q))} {' '.join(map(str, img.t))} 1 {img.name}")
        lines.append("")  # empty 2D-points line, which real files can have
    (tmp_path / "images.txt").write_text("\n".join(lines) + "\n")
    out = tmp_path / "cam.csv"
    summary = cu.convert_folder(tmp_path, out)
    assert summary["cameras_solved"] == len(CASES)
    assert summary["missing_count"] == 0
    assert out.read_text().splitlines()[0].startswith("frame,name,x,y,z,pitch,yaw,roll")
