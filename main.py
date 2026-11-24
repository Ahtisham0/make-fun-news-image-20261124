#!/usr/bin/env python3
"""Entry program for make.fun news-image-20261124.

Copies the front-page image (entry.png, shipped beside this file)
to the grader's output directory as entry.png.

Stdlib only, no network. The output directory is taken from the
MAKEFUN_OUTPUT_DIR environment variable (the local stand-in for
/output) and defaults to /output.
"""

import hashlib
import os
import shutil
import sys
from pathlib import Path

# PNG files always start with these eight magic bytes.
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def source_path() -> Path:
    """The image shipped in this repository, next to this program."""
    return Path(__file__).resolve().parent / "entry.png"


def output_dir() -> Path:
    """Where the image must be written (default /output)."""
    return Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def verify_png(data: bytes) -> None:
    """Refuse to copy anything that is not a whole PNG file."""
    if not data.startswith(PNG_MAGIC):
        raise SystemExit("entry.png is not a PNG file")
    if len(data) > 1_048_576:
        raise SystemExit("entry.png is over the 1 MiB limit")


def main() -> int:
    src = source_path()
    data = src.read_bytes()
    verify_png(data)

    out_dir = output_dir()
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / "entry.png"
    shutil.copyfile(src, dest)

    # Confirm the copy is byte-identical to the shipped image.
    copied = dest.read_bytes()
    assert copied == data, "copied file differs from entry.png"
    digest = hashlib.sha256(copied).hexdigest()
    print(f"wrote {dest} ({len(copied)} bytes, sha256 {digest})")
    return 0


if __name__ == "__main__":
    sys.exit(main())

