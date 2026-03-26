#!/usr/bin/env python3
"""
Taleemabad Social Post Scene Builder
Generates an Excalidraw scene JSON with all 3 platform sizes side by side.

Usage:
    python build_scene.py --config post_config.json --output scene.json

Config format:
{
  "template": "centered|left_heavy|announcement|app_showcase",
  "headline": "Welcome to",
  "body_text": "",             // optional sub-text
  "bg_color": "#3C5AA5",      // background color
  "bg_overlay": {             // optional: semi-transparent tint for depth
    "color": "#000000",       //   color of overlay (dark or light)
    "opacity": 15             //   0-100, keep 10-25 for subtle depth
  },
  "text_color": "#FFFFFF",
  "assets_dir": "/path/to/Assets",
  "logo": "Green BG@4x.png",
  "tagline_image": "text-lets-fuel-learning.png",  // optional
  "decorative": [
    {
      "file": "sparkle-stars-3d-yellow.png",
      "placement": "bottom-right",    // see placements below
      "rotation": 0.0,                // optional: radians, e.g. 0.3 for 17°
      "size_scale": 1.0               // optional: 1.0=default, 1.5=50% larger, 2.0=double
    }
  ]
}

Placement options:
  "top-left"      — bleed outside top-left corner
  "top-right"     — bleed outside top-right corner
  "bottom-left"   — bleed outside bottom-left corner
  "bottom-right"  — bleed outside bottom-right corner
  "corner-tr"     — small accent inside top-right
  "corner-bl"     — small accent inside bottom-left
  "center-right"  — hero graphic, right half, partially inside post (default W*0.45)
  "bleed-right"   — OVERSIZED hero, right edge, extends BEYOND post boundary for drama
  "bleed-bottom"  — large element bleeding off the bottom edge

Output images are 2x standard dimensions for high-DPI quality:
  LinkedIn:  2400 x 1256 px
  Instagram: 2160 x 2160 px
  X/Twitter: 2400 x 1350 px
"""
import argparse
import base64
import json
import math
from pathlib import Path
from PIL import Image

# Build at 2x canvas scale for high-DPI output.
# Excalidraw renders canvas coordinates at ~1px per unit, so a 2x canvas
# gives a 2x resolution export — sharper text, smoother edges, Retina-ready.
SCALE = 2

# Platform configs: (name, width, height, canvas_offset_x)
_BASE_PLATFORMS = [
    ('linkedin',  1200,  628,    0),
    ('instagram', 1080, 1080, 1280),
    ('x_twitter', 1200,  675, 2440),
]
PLATFORMS = [(n, W * SCALE, H * SCALE, ox * SCALE) for n, W, H, ox in _BASE_PLATFORMS]
CANVAS_GAP = 80 * SCALE

# Font families
LILITA    = 7   # bold, playful — headlines
HELVETICA = 2   # clean, modern — domain/caption
VIRGIL    = 1   # handwritten Excalidraw default

_id_counter = [0]

def unique_id():
    _id_counter[0] += 1
    return f'el{_id_counter[0]:04d}'

def b64_asset(assets_dir, filename):
    path = Path(assets_dir) / filename
    with open(path, 'rb') as f:
        return 'data:image/png;base64,' + base64.b64encode(f.read()).decode()

def asset_size(assets_dir, filename):
    path = Path(assets_dir) / filename
    img = Image.open(path)
    return img.size  # (width, height)

def make_bg(x, y, w, h, color, opacity=100):
    return {
        'type': 'rectangle', 'id': unique_id(),
        'x': x, 'y': y, 'width': w, 'height': h,
        'backgroundColor': color, 'strokeColor': 'transparent',
        'roughness': 0, 'strokeWidth': 0, 'fillStyle': 'solid',
        'opacity': opacity, 'angle': 0, 'groupIds': [], 'frameId': None,
        'roundness': None, 'boundElements': [], 'locked': False,
    }

def make_img(file_id, x, y, w, h, angle=0, opacity=100):
    return {
        'type': 'image', 'id': unique_id(),
        'x': x, 'y': y, 'width': w, 'height': h,
        'fileId': file_id, 'status': 'saved',
        'angle': angle, 'opacity': opacity,
        'strokeColor': 'transparent', 'backgroundColor': 'transparent',
        'roughness': 0, 'groupIds': [], 'frameId': None,
        'boundElements': [], 'locked': False,
    }

def make_txt(text, center_x, y, half_width, font_size, color, family=LILITA, align='center'):
    x = center_x - half_width if align == 'center' else center_x
    return {
        'type': 'text', 'id': unique_id(),
        'x': x, 'y': y,
        'width': half_width * 2, 'height': int(font_size * 1.4),
        'text': text, 'originalText': text,
        'fontSize': font_size, 'fontFamily': family,
        'textAlign': align, 'verticalAlign': 'top',
        'strokeColor': color, 'backgroundColor': 'transparent',
        'roughness': 0, 'opacity': 100, 'angle': 0,
        'lineHeight': 1.25, 'containerId': None,
        'groupIds': [], 'frameId': None, 'boundElements': [], 'locked': False,
    }

def place_decor(placement, ox, oy, W, H, file_id, rotation=0, size_scale=1.0):
    """Place a decorative asset using a named placement.

    rotation: angle in radians (e.g. 0.3 ≈ 17°, -0.5 ≈ -29°)
    size_scale: multiplier on default size (1.5 = 50% bigger, 2.0 = double)

    The 'bleed-right' and 'bleed-bottom' placements create oversized hero
    elements that extend beyond the post boundary — this is a powerful design
    technique that creates dynamism and visual energy.
    """
    s = SCALE

    # Base placements (all coords/sizes in scaled canvas units)
    placements = {
        # Edge bleed — elements partially outside the post
        'top-left':    (ox - 35*s,    oy - 25*s,     150*s, 120*s),
        'top-right':   (ox+W - 95*s,  oy - 25*s,     130*s, 110*s),
        'bottom-left': (ox - 38*s,    oy+H - 115*s,  120*s, 120*s),
        'bottom-right':(ox+W - 170*s, oy+H - 110*s,  175*s, 115*s),
        # Small accents inside corners
        'corner-tr':   (ox+W - 165*s, oy + 22*s,      80*s,  80*s),
        'corner-bl':   (ox + 28*s,    oy+H - 100*s,   65*s,  65*s),
        # Center-right hero (contained, ~45% of post width)
        'center-right':(ox + int(W*0.52), oy + int(H*0.08), int(W*0.45), int(W*0.45)),
        # OVERSIZED hero bleeding off right edge — dramatic, editorial feel
        # Element is ~70% of post height, anchored center-right, half bleeds out
        'bleed-right': (ox + int(W*0.55), oy + int(H*0.05), int(H*0.85), int(H*0.85)),
        # Large element bleeding off the bottom — creates depth under text
        'bleed-bottom':(ox + int(W*0.45), oy + int(H*0.35), int(H*0.8), int(H*0.8)),
    }

    x, y, w, h = placements.get(placement, (ox + 50*s, oy + 50*s, 100*s, 100*s))

    # Apply size_scale: grow from the element's center
    if size_scale != 1.0:
        cx, cy = x + w / 2, y + h / 2
        w, h = int(w * size_scale), int(h * size_scale)
        x, y = int(cx - w / 2), int(cy - h / 2)

    # Opacity: bleed elements slightly more transparent for depth
    opacity = 85 if 'bleed' in placement else 90

    return make_img(file_id, x, y, w, h, angle=rotation, opacity=opacity)


def build_centered(cfg, ox, oy, W, H, file_ids):
    """Template A: centered logo + tagline."""
    els = []
    cx = ox + W // 2
    s = SCALE

    if W == 1080 * s:     # Instagram (square)
        wel_fs, logo_w, tag_w, top_pad = 82*s, 480*s, 460*s, 90*s
    elif H < 640 * s:     # LinkedIn landscape
        wel_fs, logo_w, tag_w, top_pad = 52*s, 360*s, 340*s, 38*s
    else:                 # X/Twitter
        wel_fs, logo_w, tag_w, top_pad = 54*s, 360*s, 340*s, 40*s

    if cfg.get('headline'):
        els.append(make_txt(cfg['headline'], cx, oy + top_pad, 400*s, wel_fs, cfg['text_color']))

    logo_fid = file_ids.get('logo')
    if logo_fid:
        aw, ah = cfg['asset_sizes'].get(cfg['logo'], (764, 479))
        logo_h = int(logo_w * ah / aw)
        logo_x = cx - logo_w // 2
        logo_y = oy + top_pad + int(wel_fs * 1.4) + 12*s
        els.append(make_img(logo_fid, logo_x, logo_y, logo_w, logo_h))

        tag_fid = file_ids.get('tagline')
        if tag_fid:
            tw, th = cfg['asset_sizes'].get(cfg.get('tagline_image', ''), (946, 504))
            tag_h = int(tag_w * th / tw)
            els.append(make_img(tag_fid, cx - tag_w // 2, logo_y + logo_h + 14*s, tag_w, tag_h))
            dom_y = logo_y + logo_h + 14*s + tag_h + 10*s
        else:
            dom_y = logo_y + logo_h + 20*s
    else:
        dom_y = oy + H - 40*s

    if cfg.get('body_text'):
        body_fs = max(22*s, wel_fs // 2)
        els.append(make_txt(cfg['body_text'], cx, dom_y, 400*s, body_fs, cfg['text_color'], HELVETICA))
        dom_y += int(body_fs * 1.6)

    dom_fs = max(18*s, int(wel_fs * 0.40))
    els.append(make_txt('taleemabad.com', cx, dom_y, 300*s, dom_fs, '#B4E1F0', HELVETICA))

    return els


def build_left_heavy(cfg, ox, oy, W, H, file_ids):
    """Template B: large graphic right, text left.

    Design intent: the hero element on the right should feel BOLD, not balanced.
    Text hierarchy: large headline → smaller body → small logo/watermark.
    The text block sits in the left 50% with breathing room on all sides.
    """
    els = []
    s = SCALE

    if W == 1080 * s:
        hl_fs, body_fs = 80*s, 34*s
    else:
        hl_fs, body_fs = 64*s, 28*s

    # Headline — positioned in upper-left third, not dead center vertically
    headline_x = ox + 70*s
    hl_y = oy + int(H * 0.16)
    hl_width = int(W * 0.48)
    hl_el = {
        'type': 'text', 'id': unique_id(),
        'x': headline_x, 'y': hl_y, 'width': hl_width, 'height': int(hl_fs * 3.2),
        'text': cfg.get('headline', ''), 'originalText': cfg.get('headline', ''),
        'fontSize': hl_fs, 'fontFamily': LILITA,
        'textAlign': 'left', 'verticalAlign': 'top',
        'strokeColor': cfg['text_color'], 'backgroundColor': 'transparent',
        'roughness': 0, 'opacity': 100, 'angle': 0,
        'lineHeight': 1.2, 'containerId': None,
        'groupIds': [], 'frameId': None, 'boundElements': [], 'locked': False,
    }
    els.append(hl_el)

    # Body text — breathing gap below headline
    if cfg.get('body_text'):
        body_y = hl_y + int(hl_fs * 3.5)
        body_el = dict(hl_el)
        body_el['id'] = unique_id()
        body_el['y'] = body_y
        body_el['text'] = cfg['body_text']
        body_el['originalText'] = cfg['body_text']
        body_el['fontSize'] = body_fs
        body_el['height'] = int(body_fs * 4.5)
        body_el['strokeColor'] = '#D4F0DC'  # soft light green, not pure white — easier to read
        body_el['lineHeight'] = 1.45
        els.append(body_el)

    # Logo — bottom left, sized for the post width
    logo_fid = file_ids.get('logo')
    if logo_fid:
        logo_w = int(W * 0.26)
        aw, ah = cfg['asset_sizes'].get(cfg['logo'], (764, 479))
        logo_h = int(logo_w * ah / aw)
        els.append(make_img(logo_fid, ox + 50*s, oy + H - logo_h - 40*s, logo_w, logo_h))

    # Domain watermark — small, aligned with logo
    dom_fs = 16 * s
    els.append(make_txt('taleemabad.com', ox + int(W * 0.24), oy + H - 28*s, 220*s, dom_fs, '#A8D8B4', HELVETICA))

    return els


def build_scene(cfg):
    """Build the full Excalidraw scene for all 3 platforms."""
    assets_dir = cfg['assets_dir']
    elements = []
    files = {}

    asset_sizes = {}
    def register(key, filename):
        if not filename:
            return None
        fid = f'file_{key}'
        files[fid] = {
            'id': fid,
            'dataURL': b64_asset(assets_dir, filename),
            'mimeType': 'image/png',
        }
        asset_sizes[filename] = asset_size(assets_dir, filename)
        return fid

    cfg['asset_sizes'] = asset_sizes
    file_ids = {}
    file_ids['logo']    = register('logo', cfg.get('logo'))
    file_ids['tagline'] = register('tagline', cfg.get('tagline_image'))

    for i, d in enumerate(cfg.get('decorative', [])):
        key = f'decor_{i}_{Path(d["file"]).stem}'
        file_ids[key] = register(key, d['file'])
        d['_fid'] = file_ids[key]

    template = cfg.get('template', 'centered')

    for name, W, H, ox in PLATFORMS:
        oy = 0

        # 1. Base background
        elements.append(make_bg(ox, oy, W, H, cfg['bg_color']))

        # 2. Optional background overlay — adds depth/dimension to solid backgrounds.
        #    A dark overlay at 12-20% opacity makes the background feel rich, not flat.
        #    A light overlay at 10-15% opacity creates a subtle highlight zone.
        overlay = cfg.get('bg_overlay')
        if overlay:
            elements.append(make_bg(ox, oy, W, H, overlay['color'], overlay.get('opacity', 15)))

        # 3. Decorative assets (placed BEHIND text content so hero element doesn't
        #    obscure the headline — order matters in Excalidraw z-stacking)
        for d in cfg.get('decorative', []):
            fid = d.get('_fid')
            if fid:
                elements.append(place_decor(
                    d['placement'], ox, oy, W, H, fid,
                    rotation=d.get('rotation', 0),
                    size_scale=d.get('size_scale', 1.0),
                ))

        # 4. Text content (rendered on top of decorative elements)
        if template == 'left_heavy':
            content_els = build_left_heavy(cfg, ox, oy, W, H, file_ids)
        else:
            content_els = build_centered(cfg, ox, oy, W, H, file_ids)

        elements.extend(content_els)

    return {
        'type': 'excalidraw',
        'version': 2,
        'elements': elements,
        'files': files,
    }


def main():
    parser = argparse.ArgumentParser(description='Build Excalidraw social post scene')
    parser.add_argument('--config', required=True, help='Path to post_config.json')
    parser.add_argument('--output', required=True, help='Output scene.json path')
    args = parser.parse_args()

    with open(args.config) as f:
        cfg = json.load(f)

    scene = build_scene(cfg)

    with open(args.output, 'w') as f:
        json.dump(scene, f)

    n_elements = len(scene['elements'])
    n_files = len(scene['files'])
    size_kb = len(json.dumps(scene)) // 1024
    print(f'Scene built at {SCALE}x scale: {n_elements} elements, {n_files} files, {size_kb}KB → {args.output}')
    print(f'Output dimensions: LinkedIn 2400x1256, Instagram 2160x2160, X/Twitter 2400x1350')


if __name__ == '__main__':
    main()
