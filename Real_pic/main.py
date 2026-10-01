"""Download a real wallpaper and run the complete DIP project on it."""
from __future__ import annotations

import argparse
import sys
from io import BytesIO
from pathlib import Path
from urllib.request import Request, urlopen

from PIL import Image, ImageOps

ROOT = Path(__file__).parent
SOURCE = ROOT / "real_wallpaper.jpg"
OUTPUTS = ROOT / "outputs"
WALLPAPER_URL = (
    "https://images.unsplash.com/photo-1500534623283-312aade485b7"
    "?auto=format&fit=crop&w=1920&h=1080&q=90"
)


def download_wallpaper(force: bool = False) -> Path:
    if SOURCE.exists() and not force:
        print("Using cached wallpaper:", SOURCE)
        return SOURCE

    print("Downloading real wallpaper from the internet...")
    request = Request(WALLPAPER_URL, headers={"User-Agent": "DIP-Lab/1.0"})
    with urlopen(request, timeout=45) as response:
        image_data = response.read()

    image = ImageOps.exif_transpose(Image.open(BytesIO(image_data))).convert("RGB")
    image.thumbnail((1920, 1080), Image.Resampling.LANCZOS)
    image.save(SOURCE, format="JPEG", quality=95)
    print("Real wallpaper saved:", SOURCE)
    return SOURCE


def run_processing(source: Path, show_images: bool) -> None:
    project_root = ROOT.parent / "vscode_project"
    sys.path.insert(0, str(project_root))
    import main as processing

    processing.OUT = OUTPUTS
    processing.SHOW_IMAGES = show_images
    original_arguments = sys.argv
    try:
        sys.argv = ["main.py", "--image", str(source)]
        if not show_images:
            sys.argv.append("--no-show")
        processing.main()
    finally:
        sys.argv = original_arguments


def main() -> None:
    parser = argparse.ArgumentParser(description="Run DIP operations on a downloaded real wallpaper.")
    parser.add_argument("--refresh", action="store_true", help="download the wallpaper again")
    parser.add_argument("--no-show", action="store_true", help="save outputs without opening figures")
    args = parser.parse_args()

    OUTPUTS.mkdir(exist_ok=True)
    source = download_wallpaper(force=args.refresh)
    with Image.open(source) as image:
        print("Wallpaper size:", image.size, "| mode:", image.mode)
    run_processing(source, show_images=not args.no_show)
    print("All real-wallpaper outputs are in:", OUTPUTS)


if __name__ == "__main__":
    main()
