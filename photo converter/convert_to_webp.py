"""Convert images within a directory tree to WebP format with a fixed resolution.

Usage:
    python convert_to_webp.py /path/to/root_directory [--width WIDTH --height HEIGHT]

By default, the script resizes every supported image it finds to 1_280x720 pixels
and writes the converted image next to the source file with the same base name but
<<<<<<< HEAD
with a ``.webp`` extension.
=======
with a ``.webp`` extension
>>>>>>> f846ee4 (add photo converter script, requirements)
"""

from __future__ import annotations

import argparse
import logging
from pathlib import Path
<<<<<<< HEAD
from typing import Iterable, Tuple
=======
from typing import Iterable, Tuple, Optional
>>>>>>> f846ee4 (add photo converter script, requirements)

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


<<<<<<< HEAD
def convert_image(path: Path, size: Tuple[int, int], overwrite: bool = True) -> bool:
    """Convert *path* to WebP with *size* (width, height).
=======
def convert_image(
    path: Path,
    size: Optional[Tuple[int, int]] = None,
    overwrite: bool = True,
    max_width: int = 0,
    max_height: int = 0,
    quality: int = 85,
) -> bool:
    """Convert *path* to WebP.

    If *size* is provided, resize to that exact (width, height).
    Else, if *max_width*/*max_height* provided (>0), downscale proportionally to fit within bounds.
    Else, keep original size.
>>>>>>> f846ee4 (add photo converter script, requirements)

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
<<<<<<< HEAD
        resized = img.resize(size, Image.Resampling.LANCZOS)
        resized.save(output_path, "WEBP")
=======
        # Compatibility with older Pillow versions where Image.Resampling does not exist
        try:
            resample_filter = Image.Resampling.LANCZOS  # Pillow >= 9.1.0
        except AttributeError:
            resample_filter = getattr(Image, "LANCZOS", Image.ANTIALIAS)  # Older Pillow

        if size is not None:
            img = img.resize(size, resample=resample_filter)
        elif max_width > 0 or max_height > 0:
            w, h = img.size
            target_w = max_width or w
            target_h = max_height or h
            scale = min(target_w / w, target_h / h, 1.0)
            if scale < 1.0:
                new_size = (int(w * scale), int(h * scale))
                img = img.resize(new_size, resample=resample_filter)

        img.save(output_path, "WEBP", quality=quality)
>>>>>>> f846ee4 (add photo converter script, requirements)

    return True


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Convert images in a folder tree to WebP.")
    parser.add_argument(
        "root",
        type=Path,
        help="Root directory containing folders with images.",
    )
<<<<<<< HEAD
    parser.add_argument(
        "--width",
        type=int,
        default=1_280,
        help="Target width for the output images (default: 1280).",
=======
    # Optional exact resize
    parser.add_argument(
        "--width",
        type=int,
        default=None,
        help="Exact resize width for output images (optional).",
>>>>>>> f846ee4 (add photo converter script, requirements)
    )
    parser.add_argument(
        "--height",
        type=int,
<<<<<<< HEAD
        default=720,
        help="Target height for the output images (default: 720).",
=======
        default=None,
        help="Exact resize height for output images (optional).",
    )
    # Preferred proportional downscale (no upscale)
    parser.add_argument(
        "--max-width",
        type=int,
        default=0,
        help="Max width to fit within (keeps aspect ratio, no upscale).",
    )
    parser.add_argument(
        "--max-height",
        type=int,
        default=0,
        help="Max height to fit within (keeps aspect ratio, no upscale).",
    )
    parser.add_argument(
        "--quality",
        type=int,
        default=85,
        help="WEBP quality (1-100, default: 85).",
    )
    parser.add_argument(
        "--max-filesize-mb",
        type=float,
        default=1.0,
        help="Flag originals larger than this size (in MB) as too large (default: 1.0).",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("oversized_images.txt"),
        help="Path to write the oversized images report (default: oversized_images.txt).",
>>>>>>> f846ee4 (add photo converter script, requirements)
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

<<<<<<< HEAD
    size = (args.width, args.height)

    logging.info("Converting images in %s to WebP with size %sx%s", args.root, args.width, args.height)
=======
    size = (args.width, args.height) if (args.width and args.height) else None

    logging.info(
        "Converting images in %s to WebP (%s, max %sx%s, quality=%s)",
        args.root,
        f"exact {size[0]}x{size[1]}" if size else "no exact resize",
        args.max_width or "-",
        args.max_height or "-",
        args.quality,
    )
>>>>>>> f846ee4 (add photo converter script, requirements)

    image_paths = list(iter_image_files(args.root))
    if not image_paths:
        logging.warning("No supported image files found under %s", args.root)
        return

<<<<<<< HEAD
    for path in image_paths:
        try:
            converted = convert_image(path, size, overwrite=not args.no_overwrite)
=======
    oversized: list[str] = []
    threshold_bytes = int(args.max_filesize_mb * 1024 * 1024)

    for path in image_paths:
        try:
            # Flag large originals
            try:
                if path.stat().st_size > threshold_bytes:
                    oversized.append(f"{path}  ({path.stat().st_size/1048576:.2f} MB)")
            except Exception:
                pass

            converted = convert_image(
                path,
                size=size,
                overwrite=not args.no_overwrite,
                max_width=args.max_width,
                max_height=args.max_height,
                quality=args.quality,
            )
>>>>>>> f846ee4 (add photo converter script, requirements)
            if converted:
                logging.info("Converted %s", path)
        except Exception as exc:  # pylint: disable=broad-except
            logging.error("Failed to convert %s: %s", path, exc)

<<<<<<< HEAD
=======
    if oversized:
        try:
            args.report.write_text("\n".join(oversized), encoding="utf-8")
            logging.info("Wrote oversized report: %s (%d items)", args.report, len(oversized))
        except Exception as exc:
            logging.error("Failed writing report %s: %s", args.report, exc)

>>>>>>> f846ee4 (add photo converter script, requirements)

if __name__ == "__main__":
    main()
