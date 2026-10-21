"""Command-line entry points for people who don't use an AI agent."""

from __future__ import annotations

import argparse
import json

from . import colmap_ue


def colmap2ue() -> None:
    p = argparse.ArgumentParser(description="COLMAP TXT model -> Unreal camera keys (CSV or JSON)")
    p.add_argument("sparse_txt_dir", help="Folder with cameras.txt and images.txt")
    p.add_argument("output", help="camera.csv or camera.json")
    p.add_argument("--scale", type=float, default=100.0, help="UE cm per COLMAP unit (default 100)")
    a = p.parse_args()
    print(json.dumps(colmap_ue.convert_folder(a.sparse_txt_dir, a.output, a.scale), indent=2))


if __name__ == "__main__":
    colmap2ue()
