#!/usr/bin/env python3
"""
Crop the full Excalidraw export into individual platform posts.

Output dimensions are 2x standard for high-DPI / Retina quality:
  LinkedIn:  2400 x 1256 px  (standard: 1200x628)
  Instagram: 2160 x 2160 px  (standard: 1080x1080)
  X/Twitter: 2400 x 1350 px  (standard: 1200x675)

Auto-detects actual content bounds from the exported image so that
Excalidraw's variable padding never causes white borders in crops.

Usage:
    python crop_posts.py --input full_canvas.png --output-dir ./Posts
"""
import argparse
import os
from pathlib import Path
from PIL import Image

# Canvas layout — must match positions used when building in Excalidraw
# (x offset of each post's left edge, in canvas units)
_BASE_PLATFORMS = [
    ('linkedin',  1200,  628,    0),
    ('instagram', 1080, 1080, 1280),
    ('x_twitter', 1200,  675, 2440),
]

# Total canvas width in canvas units (rightmost post right edge)
CANVAS_TOTAL_W = 2440 + 1200  # = 3640
CANVAS_TOTAL_H = 1080          # tallest post (Instagram)

# Output at 2x standard dimensions for Retina quality
SCALE = 2
PLATFORMS = [(n, W * SCALE, H * SCALE, ox) for n, W, H, ox in _BASE_PLATFORMS]


def detect_content_bounds(img):
    """
    Auto-detect the true pixel bounds of the canvas content
    by scanning for non-white pixels. Returns (left, top, right, bottom).
    Excalidraw adds variable padding — this makes crops exact regardless.
    """
    WHITE = (255, 255, 255)
    rgb = img.convert('RGB')
    w, h = rgb.size

    # Scan left edge
    left = 0
    for x in range(w):
        for y in range(h):
            if rgb.getpixel((x, y)) != WHITE:
                left = x
                break
        else:
            continue
        break

    # Scan right edge
    right = w - 1
    for x in range(w - 1, -1, -1):
        for y in range(h):
            if rgb.getpixel((x, y)) != WHITE:
                right = x
                break
        else:
            continue
        break

    # Scan top edge
    top = 0
    for y in range(h):
        for x in range(w):
            if rgb.getpixel((x, y)) != WHITE:
                top = y
                break
        else:
            continue
        break

    # Scan bottom edge
    bottom = h - 1
    for y in range(h - 1, -1, -1):
        for x in range(w):
            if rgb.getpixel((x, y)) != WHITE:
                bottom = y
                break
        else:
            continue
        break

    return left, top, right, bottom


def detect_content_bounds_fast(img):
    """
    Faster version: sample columns/rows at intervals rather than every pixel.
    Finds the bounding box of non-white content.
    """
    WHITE = 255
    rgb = img.convert('RGB')
    w, h = rgb.size
    pixels = rgb.load()

    def is_white_col(x):
        step = max(1, h // 50)
        return all(
            pixels[x, y][0] >= WHITE - 2 and
            pixels[x, y][1] >= WHITE - 2 and
            pixels[x, y][2] >= WHITE - 2
            for y in range(0, h, step)
        )

    def is_white_row(y):
        step = max(1, w // 50)
        return all(
            pixels[x, y][0] >= WHITE - 2 and
            pixels[x, y][1] >= WHITE - 2 and
            pixels[x, y][2] >= WHITE - 2
            for x in range(0, w, step)
        )

    left = next((x for x in range(w) if not is_white_col(x)), 0)
    right = next((x for x in range(w - 1, -1, -1) if not is_white_col(x)), w - 1)
    top = next((y for y in range(h) if not is_white_row(y)), 0)
    bottom = next((y for y in range(h - 1, -1, -1) if not is_white_row(y)), h - 1)

    return left, top, right, bottom


def crop_posts(input_path, output_dir, prefix='post', cleanup_input=True):
    full = Image.open(input_path)
    EW, EH = full.size

    print(f'Exported canvas size: {EW}x{EH}')

    # Auto-detect true content bounds (strips Excalidraw's padding exactly)
    left, top, right, bottom = detect_content_bounds_fast(full)
    content_w = right - left + 1
    content_h = bottom - top + 1
    print(f'Detected content bounds: left={left} top={top} right={right} bottom={bottom}')
    print(f'Content area: {content_w}x{content_h}px')

    # Scale factor: how many image pixels per canvas unit
    # Use width for scale since it spans all 3 posts (more reliable than height)
    px_per_unit = content_w / CANVAS_TOTAL_W
    print(f'Scale: {px_per_unit:.4f} px/unit')

    os.makedirs(output_dir, exist_ok=True)
    saved = []

    for name, W, H, ox in PLATFORMS:
        # Canvas coordinates → image pixel coordinates
        x1 = left + int(ox * px_per_unit)
        y1 = top
        x2 = left + int((ox + W // SCALE) * px_per_unit)
        y2 = top + int((H // SCALE) * px_per_unit)

        # Clamp to image bounds
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(EW, x2), min(EH, y2)

        print(f'{name}: cropping ({x1},{y1}) → ({x2},{y2})')
        cropped = full.crop((x1, y1, x2, y2))

        # Resize to exact 2x output dimensions with LANCZOS (highest quality)
        final = cropped.resize((W, H), Image.LANCZOS)
        out_path = Path(output_dir) / f'{prefix}-{name}.png'
        final.save(str(out_path), 'PNG', dpi=(144, 144), optimize=True)
        size_kb = os.path.getsize(str(out_path)) // 1024
        saved.append(str(out_path))
        print(f'Saved: {out_path} ({W}x{H}) — {size_kb} KB')

    if cleanup_input and Path(input_path).exists():
        os.remove(input_path)

    return saved


def main():
    parser = argparse.ArgumentParser(description='Crop Excalidraw export into platform posts')
    parser.add_argument('--input',      required=True, help='Full canvas PNG from Excalidraw export')
    parser.add_argument('--output-dir', required=True, help='Directory to save cropped posts')
    parser.add_argument('--prefix',     default='post', help='Filename prefix (default: post)')
    parser.add_argument('--keep-input', action='store_true', help='Keep the full canvas PNG after cropping')
    args = parser.parse_args()

    saved = crop_posts(
        args.input,
        args.output_dir,
        prefix=args.prefix,
        cleanup_input=not args.keep_input
    )
    print(f'\n{len(saved)} posts saved to {args.output_dir}/')
    print('All images at 2x resolution (2400x1256, 2160x2160, 2400x1350) — Retina ready')


if __name__ == '__main__':
    main()
