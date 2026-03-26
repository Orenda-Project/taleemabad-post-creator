#!/usr/bin/env python3
"""
Crop the full Excalidraw export into individual platform posts.

Output dimensions are 2x standard for high-DPI / Retina quality:
  LinkedIn:  2400 x 1256 px  (standard: 1200x628)
  Instagram: 2160 x 2160 px  (standard: 1080x1080)
  X/Twitter: 2400 x 1350 px  (standard: 1200x675)

These are universally accepted by all social media platforms and render
crisply on Retina/4K displays. The 2x source canvas from build_scene.py
means we're downsampling rather than upsampling — maximum sharpness.

Usage:
    python crop_posts.py --input full_canvas.png --output-dir ./Posts
"""
import argparse
import os
from pathlib import Path
from PIL import Image

# Must match build_scene.py PLATFORMS layout (at SCALE=2)
SCALE = 2

_BASE_PLATFORMS = [
    ('linkedin',  1200,  628,    0),
    ('instagram', 1080, 1080, 1280),
    ('x_twitter', 1200,  675, 2440),
]
# Output at 2x standard dimensions for Retina quality
PLATFORMS = [(n, W * SCALE, H * SCALE, ox * SCALE) for n, W, H, ox in _BASE_PLATFORMS]

CANVAS_GAP = 80 * SCALE

# Content spans: decorative elements bleed outside post edges (scaled)
CANVAS_MIN_X = -38 * SCALE
CANVAS_MIN_Y = -25 * SCALE
CANVAS_MAX_X = (2440 + 1200 + 50) * SCALE   # last post end + small buffer
# Excalidraw adds a fixed padding (~30px) on each side of the export,
# independent of the canvas content scale.
CANVAS_PADDING = 30


def crop_posts(input_path, output_dir, prefix='post', cleanup_input=True):
    full = Image.open(input_path)
    EW, EH = full.size

    canvas_content_w = CANVAS_MAX_X - CANVAS_MIN_X
    scale = (EW - 2 * CANVAS_PADDING) / canvas_content_w

    def to_px(cx, cy):
        px = CANVAS_PADDING + (cx - CANVAS_MIN_X) * scale
        py = CANVAS_PADDING + (cy - CANVAS_MIN_Y) * scale
        return int(px), int(py)

    os.makedirs(output_dir, exist_ok=True)
    saved = []

    for name, W, H, ox in PLATFORMS:
        x1, y1 = to_px(ox, 0)
        x2, y2 = to_px(ox + W, H)
        cropped = full.crop((x1, y1, x2, y2))
        # Resize to exact output dimensions with LANCZOS (highest quality filter)
        final = cropped.resize((W, H), Image.LANCZOS)
        out_path = Path(output_dir) / f'{prefix}-{name}.png'
        # Save with maximum PNG quality and 144 DPI metadata (2x of 72dpi standard)
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
    parser.add_argument('--keep-input', action='store_true', help='Keep the full canvas PNG')
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
