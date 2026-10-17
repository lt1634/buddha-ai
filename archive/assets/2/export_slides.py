#!/usr/bin/env python3
"""Export carousel HTML slides to individual IG-sized PNGs via Chrome headless.

Strategy for crisp text:
- Render at higher device scale factor (e.g. 2x) to get a 2160×2700 screenshot
- Downscale to 1080×1350 with Lanczos for sharper text edges
"""

import re, sys, os, tempfile, subprocess, pathlib

from PIL import Image

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
CANVAS_W, CANVAS_H = 1080, 1350  # IG carousel 4:5
# Export look: centered card on dark background (closer to assets/1),
# while still rendering at high DPR and fitting text.
SLIDE_W, SLIDE_H = 940, 1200
DEVICE_SCALE = 2  # render at 2x then downscale for crispness

def extract_slides(html: str) -> list[str]:
    """Extract slide divs using div-nesting stack counting."""
    marker = re.compile(r'<div\s+class="slide\s+slide-\d+"[^>]*>')
    slides = []
    div_open = re.compile(r'<div\b[^>]*>')
    div_close = re.compile(r'</div\s*>')
    
    for m in marker.finditer(html):
        start = m.start()
        pos = m.end()
        depth = 1
        while depth > 0:
            open_m = div_open.search(html, pos)
            close_m = div_close.search(html, pos)
            if close_m is None:
                raise RuntimeError("Unmatched <div>")
            if open_m is None or close_m.start() < open_m.start():
                depth -= 1
                pos = close_m.end()
            else:
                depth += 1
                pos = open_m.end()
        slides.append(html[start:pos].rstrip())
    return slides


def extract_styles(html: str) -> str:
    """Extract all <style> blocks."""
    return '\n'.join(re.findall(r'<style>.*?</style>', html, re.DOTALL))


def build_export_html(style_block: str, slide_html: str, canvas_w: int, canvas_h: int) -> str:
    """Wrap a single slide in an isolated export page."""

    return f"""<!DOCTYPE html>
<html lang="zh-Hant"><head>
<meta charset="UTF-8">
{style_block}
<style>
  html, body {{
    margin: 0; padding: 0;
    background: #121212;
    width: {canvas_w}px; height: {canvas_h}px;
    overflow: hidden;
  }}
  body {{ display: block; }}

  /* Centered “card” frame (like assets/1) */
  .export-stage {{
    width: {canvas_w}px;
    height: {canvas_h}px;
    display: flex;
    align-items: center;
    justify-content: center;
  }}

  /* Force slide to card size (no transform scaling) */
  .slide {{
    width: {SLIDE_W}px !important;
    height: {SLIDE_H}px !important;
    border-radius: 48px !important;
    box-shadow: 0 18px 50px rgba(0,0,0,0.55), 0 8px 18px rgba(0,0,0,0.25) !important;
    scroll-snap-align: unset !important;
    margin: 0 !important;
  }}

  /* Neutralize motion */
  * {{ animation: none !important; transition: none !important; }}

  /* Avoid accidental clipping by transforms */
  .slide-content {{ overflow: visible !important; }}

  /* Basic typography helpers */
  .fit-text {{ display: block; }}

  /* Footer labels (人際觀照 etc.) — base CSS is 11px, too small on export card */
  .slide-footer {{
    font-size: 32px !important;
    color: #7a6f5c !important;
    padding-top: 20px !important;
  }}
  .slide-footer span:first-child,
  .slide-footer span:only-child {{
    font-size: 32px !important;
    color: #7a6f5c !important;
    letter-spacing: 2px !important;
    font-weight: 500 !important;
  }}
  .slide-footer span:last-child:not(:only-child) {{
    font-size: 48px !important;
    color: #bca882 !important;
    font-weight: 700 !important;
  }}
</style>

<script>
  // Auto-fit text to a box: binary-search font size to avoid overflow.
  function fitOne(el, minPx, maxPx) {{
    if (!el) return;
    const parent = el.parentElement;
    if (!parent) return;

    const fits = (px) => {{
      el.style.fontSize = px + "px";
      // Force layout
      void el.offsetHeight;
      // Use scrollHeight/Width to detect overflow in its own box.
      return el.scrollHeight <= el.clientHeight + 1 && el.scrollWidth <= el.clientWidth + 1;
    }};

    // Ensure the element is constrained; if not, constrain to its current box.
    if (!el.style.maxWidth) el.style.maxWidth = "100%";

    let lo = minPx, hi = maxPx, best = minPx;
    while (lo <= hi) {{
      const mid = Math.floor((lo + hi) / 2);
      if (fits(mid)) {{
        best = mid;
        lo = mid + 1;
      }} else {{
        hi = mid - 1;
      }}
    }}
    el.style.fontSize = best + "px";
  }}

  function applyFits() {{
    // Per-carousel heuristics: tune min/max so “短句唔會細，長句唔會 cut”
    // Title-style
    document.querySelectorAll(".main-title").forEach(el => {{
      el.classList.add("fit-text");
      fitOne(el, 56, 88);
    }});
    // Slide 1 subtitle (「唔係…而係…」) — keep readable
    document.querySelectorAll(".subtitle-text").forEach(el => {{
      el.classList.add("fit-text");
      fitOne(el, 34, 48);
      el.style.fontWeight = "400";
    }});
    // Small tags (e.g. Slide 5 「可以親近」) — ensure readable
    document.querySelectorAll(".action-tag").forEach(el => {{
      el.classList.add("fit-text");
      fitOne(el, 30, 44);
      el.style.fontWeight = "500";
    }});
    // Section heading chips (e.g. 「慈悲 vs 執著」) — must be readable
    document.querySelectorAll(".concept-tag").forEach(el => {{
      el.classList.add("fit-text");
      fitOne(el, 34, 52);
      el.style.fontWeight = "500";
    }});
    // Slide 2 四攝法四粒字（布施/愛語/利行/同事）
    document.querySelectorAll(".paramita-item").forEach(el => {{
      el.classList.add("fit-text");
      fitOne(el, 30, 40);
      el.style.fontWeight = "500";
    }});
    // Slide 4 慈悲 / 執著 label
    document.querySelectorAll(".comparison-label").forEach(el => {{
      el.classList.add("fit-text");
      fitOne(el, 30, 42);
      el.style.fontWeight = "600";
    }});
    // Big quote blocks
    document.querySelectorAll(".quote-text").forEach(el => {{
      el.classList.add("fit-text");
      fitOne(el, 32, 46);
    }});
    // Ending / long paragraph
    document.querySelectorAll(".ending-text").forEach(el => {{
      el.classList.add("fit-text");
      fitOne(el, 28, 40);
    }});
    // Action title
    document.querySelectorAll(".action-title").forEach(el => {{
      el.classList.add("fit-text");
      fitOne(el, 30, 44);
    }});
    // Comparison blocks
    document.querySelectorAll(".comparison-desc").forEach(el => {{
      el.classList.add("fit-text");
      fitOne(el, 26, 36);
    }});
  }}

  window.addEventListener("load", async () => {{
    try {{
      if (document.fonts && document.fonts.ready) {{
        await Promise.race([
          document.fonts.ready,
          new Promise(r => setTimeout(r, 1500))
        ]);
      }}
    }} catch (e) {{}}
    // Run twice: fonts can shift metrics.
    applyFits();
    requestAnimationFrame(() => applyFits());
  }});
</script>
</head><body>
<div class="export-stage">
{slide_html}
</div>
</body></html>"""


def chrome_screenshot(html_path: str, out_path: str, w: int, h: int, device_scale: int = 2):
    """Run Chrome headless to screenshot a single HTML file.

    Writes a crisp 1080×1350 PNG by rendering at higher device scale and downscaling.
    """
    tmp_out = out_path + ".tmp.png"
    cmd = [
        CHROME,
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        "--no-sandbox",
        f"--force-device-scale-factor={device_scale}",
        "--virtual-time-budget=3000",
        f"--window-size={w},{h}",
        f"--screenshot={tmp_out}",
        f"file://{os.path.abspath(html_path)}",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    if not os.path.exists(tmp_out) or os.path.getsize(tmp_out) == 0:
        raise RuntimeError(f"Chrome failed for {html_path}\nstdout: {result.stdout}\nstderr: {result.stderr}")

    # Downscale to target resolution (w×h). If Chrome already produced w×h, keep it.
    with Image.open(tmp_out) as im:
        if im.size != (w, h):
            im = im.convert("RGB").resize((w, h), resample=Image.LANCZOS)
            im.save(out_path, format="PNG", optimize=True)
        else:
            os.replace(tmp_out, out_path)

    if os.path.exists(tmp_out):
        try:
            os.remove(tmp_out)
        except OSError:
            pass


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("html_path", help="Carousel HTML file")
    parser.add_argument("--name", default="carousel-2", help="Output prefix")
    parser.add_argument("--out", default=".", help="Output directory")
    args = parser.parse_args()
    
    html = pathlib.Path(args.html_path).read_text()
    styles = extract_styles(html)
    slides = extract_slides(html)
    
    print(f"Found {len(slides)} slides")
    
    out_dir = pathlib.Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        for i, slide in enumerate(slides, 1):
            export_html = build_export_html(styles, slide, CANVAS_W, CANVAS_H)
            tmp_file = os.path.join(tmpdir, f"slide-{i}.html")
            out_file = out_dir / f"{args.name}-slide-{i:02d}.png"
            
            pathlib.Path(tmp_file).write_text(export_html)
            print(f"Rendering slide {i}/{len(slides)} → {out_file.name}")
            chrome_screenshot(tmp_file, str(out_file), CANVAS_W, CANVAS_H, device_scale=DEVICE_SCALE)
            
            size_kb = out_file.stat().st_size / 1024
            print(f"  ✓ {size_kb:.0f} KB")
    
    print(f"\nDone! {len(slides)} PNGs in {out_dir}")


if __name__ == "__main__":
    main()
