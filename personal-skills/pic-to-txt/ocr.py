#!/usr/bin/env python3
"""
pic-to-txt OCR companion script.

Usage:
    python3 ocr.py <folder> [--lang zh|en|auto]
    python3 ocr.py <folder> --lang zh   # Chinese → PaddleOCR
    python3 ocr.py <folder> --lang en   # English → EasyOCR
    python3 ocr.py <folder> --lang auto # heuristic detection

Output:
    - Writes raw OCR text to <folder>/_raw_ocr_output.txt
    - Prints to stdout for piping/LLM refinement

HEIC/HEIF (iPhone photos) are converted to temporary JPEGs first:
pillow-heif if installed, else `heif-convert`, else ImageMagick (`magick`/`convert`).
"""

import argparse
import glob
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HEIC_EXTS = {".heic", ".heif"}
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff", ".webp"} | HEIC_EXTS


def natural_sort_key(path: Path) -> list:
    """Sort filenames naturally: page2 < page10 < page100."""
    stem = path.stem
    return [int(c) if c.isdigit() else c.lower() for c in re.split(r"(\d+)", stem)]


def find_images(folder: str) -> list[Path]:
    """Find all image files in folder, sorted naturally."""
    folder_path = Path(folder)
    images = []
    for ext in IMAGE_EXTS:
        images.extend(folder_path.glob(f"*{ext}"))
        images.extend(folder_path.glob(f"*{ext.upper()}"))
    images.sort(key=natural_sort_key)
    return images


def detect_language(images: list[Path]) -> str:
    """Heuristic: check filenames and folder for Chinese indicators."""
    chinese_pattern = re.compile(r"[一-鿿]")
    for img in images:
        if chinese_pattern.search(img.stem):
            return "zh"
    # Check folder name
    folder_name = images[0].parent.name if images else ""
    if chinese_pattern.search(folder_name):
        return "zh"
    return "en"


def convert_heic(src: Path, dst: Path) -> None:
    """Convert one HEIC/HEIF photo to JPEG at dst, or exit with install advice."""
    try:
        from PIL import Image
        from pillow_heif import register_heif_opener

        register_heif_opener()
        Image.open(src).convert("RGB").save(dst, "JPEG", quality=95)
        return
    except ImportError:
        pass
    for tool in ("heif-convert", "magick", "convert"):
        if shutil.which(tool):
            done = subprocess.run([tool, str(src), str(dst)], capture_output=True)
            if done.returncode == 0 and dst.exists():
                return
    print(
        f"Error: cannot read HEIC photo {src.name}. Install one of:\n"
        "  pip install pillow-heif                      (recommended)\n"
        "  sudo apt install libheif-examples            (provides heif-convert)\n"
        "  ImageMagick built with HEIC support          (magick / convert)",
        file=sys.stderr,
    )
    sys.exit(1)


def prepare_images(images: list[Path], tmp_dir: Path) -> list[tuple[str, Path]]:
    """Return (original name, readable path) pairs; HEIC/HEIF become temp JPEGs."""
    pairs = []
    for i, img in enumerate(images):
        if img.suffix.lower() in HEIC_EXTS:
            jpg = tmp_dir / f"{i:04d}_{img.stem}.jpg"
            convert_heic(img, jpg)
            pairs.append((img.name, jpg))
        else:
            pairs.append((img.name, img))
    return pairs


def run_easyocr(images: list[tuple[str, Path]]) -> str:
    """Run EasyOCR on all images, return combined text."""
    import easyocr

    reader = easyocr.Reader(["en"], gpu=True)
    output_parts = []
    for name, img in images:
        result = reader.readtext(str(img))
        text = " ".join(item[1] for item in result)
        output_parts.append(f"--- {name} ---\n{text}")
    return "\n\n".join(output_parts)


def run_paddleocr(images: list[tuple[str, Path]]) -> str:
    """Run PaddleOCR on all images, return combined text."""
    from paddleocr import PaddleOCR

    ocr = PaddleOCR(use_angle_cls=True, lang="ch", show_log=False)
    output_parts = []
    for name, img in images:
        result = ocr.ocr(str(img), cls=True)
        if result[0]:
            text = " ".join(line[1][0] for line in result[0])
        else:
            text = ""
        output_parts.append(f"--- {name} ---\n{text}")
    return "\n\n".join(output_parts)


def main():
    parser = argparse.ArgumentParser(
        description="OCR image folder to text. Chinese → PaddleOCR, English → EasyOCR."
    )
    parser.add_argument("folder", help="Path to folder containing images")
    parser.add_argument(
        "--lang",
        choices=["zh", "en", "auto"],
        default="auto",
        help="Language: zh (PaddleOCR), en (EasyOCR), auto (heuristic)",
    )
    args = parser.parse_args()

    folder = args.folder
    if not os.path.isdir(folder):
        print(f"Error: folder not found: {folder}", file=sys.stderr)
        sys.exit(1)

    images = find_images(folder)
    if not images:
        print(f"Error: no image files found in {folder}", file=sys.stderr)
        sys.exit(1)

    lang = args.lang
    if lang == "auto":
        lang = detect_language(images)
        print(f"[lang] auto-detected: {'zh (PaddleOCR)' if lang == 'zh' else 'en (EasyOCR)'}", file=sys.stderr)

    print(f"[info] found {len(images)} images, using {'PaddleOCR' if lang == 'zh' else 'EasyOCR'}", file=sys.stderr)

    with tempfile.TemporaryDirectory(prefix="pic-to-txt-") as tmp:
        readable = prepare_images(images, Path(tmp))
        if lang == "zh":
            text = run_paddleocr(readable)
        else:
            text = run_easyocr(readable)

    # Save raw output
    raw_path = Path(folder) / "_raw_ocr_output.txt"
    raw_path.write_text(text, encoding="utf-8")
    print(f"[save] raw OCR text -> {raw_path}", file=sys.stderr)

    # Print to stdout for piping
    print(text)


if __name__ == "__main__":
    main()
