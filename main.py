#!/usr/bin/env python3
"""make.fun news-image-20261125 entry.

Writes one image — a newspaper front page summing up Wednesday
25 November 2026 — to /output/entry.png.

The image is drawn in code (see tools/draw_entry.py) and held in this
repository as entry.png; this program copies it byte-for-byte to the
output path. No network, no randomness: two runs write identical bytes.
"""

import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print("wrote", dst, os.path.getsize(dst), "bytes")


if __name__ == "__main__":
    sys.exit(main())
