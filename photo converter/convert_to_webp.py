"""Convert images within a directory tree to WebP format with a fixed resolution.

Usage:
    python convert_to_webp.py /path/to/root_directory [--width WIDTH --height HEIGHT]

By default, the script resizes every supported image it finds to 1_280x720 pixels
and writes the converted image next to the source file with the same base name but
with a ``.webp`` extension.
"""

from __future__ import annotations

import argparse
import logging
from pathlib import Path
from typing import Iterable, Tuple

from PIL import Image


# Supported input formats that Pillow can decode reliably.
SUPPORTED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".gif",
    ".tif",
    ".tiff",
    ".webp",  # already WebP but we still resize to the requested dimensions
}


def iter_image_files(root: Path) -> Iterable[Path]:
    """Yield image files within *root* recursively."""
    for path in root.rglob("*"):
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS:
            yield path


def convert_image(path: Path, size: Tuple[int, int], overwrite: bool = True) -> bool:
    """Convert *path* to WebP with *size* (width, height).

    Returns ``True`` when a conversion occurred. When ``overwrite`` is ``False``
    and the target WebP already exists the function returns ``False`` without
    modifying the filesystem.
    """
    output_path = path.with_suffix(".webp")

    if not overwrite and output_path.exists():
        logging.info("Skipping existing file: %s", output_path)
        return False

    with Image.open(path) as img:
        img = img.convert("RGB")
        resized = img.resize(size, Image.Resampling.LANCZOS)
        resized.save(output_path, "WEBP")

    return True


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Convert images in a folder tree to WebP.")
    parser.add_argument(
        "root",
        type=Path,
        help="Root directory containing folders with images.",
    )
    parser.add_argument(
        "--width",
        type=int,
        default=1_280,
        help="Target width for the output images (default: 1280).",
    )
    parser.add_argument(
        "--height",
        type=int,
        default=720,
        help="Target height for the output images (default: 720).",
    )
    parser.add_argument(
        "--no-overwrite",
        action="store_true",
        help="Do not overwrite existing WebP files.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging output.",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if not args.root.exists():
        raise SystemExit(f"The specified directory does not exist: {args.root}")
    if not args.root.is_dir():
        raise SystemExit(f"The specified path is not a directory: {args.root}")

    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO, format="%(message)s")

    size = (args.width, args.height)

    logging.info("Converting images in %s to WebP with size %sx%s", args.root, args.width, args.height)

    image_paths = list(iter_image_files(args.root))
    if not image_paths:
        logging.warning("No supported image files found under %s", args.root)
        return

    for path in image_paths:
        try:
            converted = convert_image(path, size, overwrite=not args.no_overwrite)
            if converted:
                logging.info("Converted %s", path)
        except Exception as exc:  # pylint: disable=broad-except
            logging.error("Failed to convert %s: %s", path, exc)


if __name__ == "__main__":
    main()
