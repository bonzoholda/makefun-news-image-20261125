#!/usr/bin/env python3
"""Copy the finished front page into the program's output directory.

The entry image is produced by tools/draw_entry.py and lives next to this
file as entry.png. This script only copies it byte for byte to
/output/entry.png, as the competition runner expects. No network access.
"""

import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"
TARGET = Path("/output/entry.png")


def main():
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE, TARGET)
    print(f"copied {SOURCE} -> {TARGET} ({TARGET.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
