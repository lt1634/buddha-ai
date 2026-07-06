#!/usr/bin/env python3
"""Export carousel HTML slides to Instagram-sized PNGs via Chrome headless.

Usage:
    python3 export_carousel_png.py                              # default: carousel.html
    python3 export_carousel_png.py demos/carousel-2-relation.html --name relation
    python3 export_carousel_png.py path/to/carousel.html --out output_dir --name my-carousel
"""

from __future__ import annotations

import argparse
import re
import subprocess
import tempfile
from pathlib import Path

# --- Defaults ---
PROJECT = Path("/Users/newmac/NS/projects/buddha-ai")
DEFAULT_HTML = PROJECT / "carousel.html"
DEFAULT_OUT = PROJECT / "carousel-png"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

WIDTH, HEIGHT = 1080, 1350  # IG carousel 4:5

# Slide intrinsic dimensions from carousel CSS (.slide class)
SLIDE_WIDTH = 440
SLIDE_HEIGHT = 520
SCALE_PADDING = 0.92  # Leave 8% border around the slide inside the PNG


# ---------------------------------------------------------------------------
# HTML extraction helpers
# ---------------------------------------------------------------------------


def extract_styles(html: str) -> str:
    """Extract all <style> blocks from the HTML (handles multiple blocks)."""
    blocks = re.findall(r"<style>(.*?)</style>", html, re.DOTALL)
    return "\n".join(blocks)


def extract_slides(html: str) -> list[str]:
    """Extract slide HTML by counting <div> nesting — whitespace-agnostic.

    No brittle end-marker string; works even if indentation or wrapper
    structure changes.
    """
    marker = re.compile(r'<div class="slide slide-\d+" data-index="\d+">')
    div_open = re.compile(r"<div\b[^>]*>")
    div_close = re.compile(r"</div\s*>")

    slides: list[str] = []
    for m in marker.finditer(html):
        start = m.start()
        pos = m.end()
        depth = 1

        while depth > 0:
            open_m = div_open.search(html, pos)
            close_m = div_close.search(html, pos)

            if close_m is None:
                raise RuntimeError("Unmatched <div>: missing closing </div>")

            if open_m is None or close_m.start() < open_m.start():
                depth -= 1
                pos = close_m.end()
            else:
                depth += 1
                pos = open_m.end()

        slides.append(html[start:pos].rstrip())

    if len(slides) < 1:
        raise RuntimeError(f"No slides found in HTML")
    return slides


def build_export_html(styles: str, slide_html: str) -> str:
    """Wrap a slide in an export-only HTML page sized for Chrome screenshot."""
    scale = min(WIDTH / SLIDE_WIDTH, HEIGHT / SLIDE_HEIGHT) * SCALE_PADDING
    return f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<style>
{styles}
html, body {{
  margin: 0;
  padding: 0;
  width: {WIDTH}px;
  height: {HEIGHT}px;
  overflow: hidden;
  background: #121212;
}}
.export-frame {{
  width: {WIDTH}px;
  height: {HEIGHT}px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #121212;
}}
.export-frame .slide {{
  flex: none;
  width: {SLIDE_WIDTH}px;
  height: {SLIDE_HEIGHT}px;
  transform: scale({scale:.4f});
  transform-origin: center center;
  scroll-snap-align: unset;
}}
body > *:not(.export-frame) {{ display: none !important; }}
</style>
</head>
<body>
<div class="export-frame">
{slide_html.strip()}
</div>
</body>
</html>"""


# ---------------------------------------------------------------------------
# Chrome headless screenshot
# ---------------------------------------------------------------------------


def screenshot(html: str, out_path: Path) -> None:
    """Render HTML to PNG via Chrome headless."""
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
        f.write(html)
        tmp = Path(f.name)

    try:
        url = tmp.as_uri()
        cmd = [
            CHROME,
            "--headless=new",
            "--disable-gpu",
            "--hide-scrollbars",
            f"--window-size={WIDTH},{HEIGHT}",
            f"--screenshot={out_path}",
            url,
        ]
        subprocess.run(cmd, check=True, capture_output=True, text=True, timeout=60)
    finally:
        tmp.unlink(missing_ok=True)

    if not out_path.exists() or out_path.stat().st_size == 0:
        raise RuntimeError(f"Chrome did not produce a valid PNG: {out_path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(description="Export carousel HTML slides to Instagram PNGs")
    parser.add_argument("html_path", nargs="?", default=str(DEFAULT_HTML),
                        help="Path to carousel HTML file (default: %(default)s)")
    parser.add_argument("--name", default="carousel-1",
                        help="Carousel prefix for output filenames (default: %(default)s)")
    parser.add_argument("--out", default=str(DEFAULT_OUT),
                        help="Output directory (default: %(default)s)")
    args = parser.parse_args()

    html_path = Path(args.html_path).expanduser()
    out_dir = Path(args.out).expanduser()
    name = args.name

    if not Path(CHROME).exists():
        raise SystemExit(f"Chrome not found: {CHROME}")
    if not html_path.exists():
        raise SystemExit(f"HTML file not found: {html_path}")

    html = html_path.read_text(encoding="utf-8")
    styles = extract_styles(html)
    slides = extract_slides(html)
    out_dir.mkdir(parents=True, exist_ok=True)

    for i, slide in enumerate(slides, start=1):
        export_html = build_export_html(styles, slide)
        out = out_dir / f"{name}-slide-{i:02d}.png"
        screenshot(export_html, out)
        print(f"  Wrote {out} ({out.stat().st_size // 1024} KB)")

    print(f"\nDone: {len(slides)} PNGs in {out_dir}")


if __name__ == "__main__":
    main()
