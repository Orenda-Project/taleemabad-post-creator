---
name: taleemabad-post-creator
description: >
  Create branded social media posts for Taleemabad — high-DPI 2x resolution output:
  LinkedIn 2400×1256, Instagram 2160×2160, X/Twitter 2400×1350 (sharp on all screens).
  Uses the brand asset library and Excalidraw. Use this skill whenever the user asks
  to create, design, generate, or update a social media post, graphic, banner, or
  visual — even if they just describe the topic without saying "post" or "design".
  The skill handles asset selection, layout choice, all three platform sizes,
  Excalidraw canvas composition, and saving final PNG files to the Posts/ folder.
---

# Taleemabad Social Post Creator

This skill turns a plain description into three polished, on-brand social media
post images (LinkedIn, Instagram, X/Twitter) using the project's asset library
and the Excalidraw MCP.

## Prerequisites

Before starting, verify:
1. **Excalidraw canvas is running** — call `mcp__excalidraw__describe_scene`. If it
   returns a connection error, tell the user to run:
   ```bash
   cd ~/mcp_excalidraw && docker-compose up
   ```
   and open `http://localhost:3000` in a browser.

2. **Assets folder exists** — check for `{project_root}/Assets/`. The project root
   is the directory containing the `Assets/` folder and `README.md`.

---

## Step 1 — Understand the Post

Ask the user (or infer from their message) these things:

| Question | Why it matters |
|----------|----------------|
| **What is the post about?** | Drives headline, template, asset selection |
| **Tone?** (celebratory / educational / urgent / warm) | Drives color theme |
| **Any specific text?** | Headline and optional body copy |
| **Any specific assets to include?** | User may have preferences |
| **Output folder?** | Default is `{project_root}/Posts/` |

If the user's message already answers these, don't ask — just proceed.

---

## Step 2 — Choose Template, Assets & Design Direction

Read `references/assets-catalog.md` to understand the full asset library.
Read `references/post-templates.md` for layout options, color themes, and **design principles**.

### Template selection guide
| Post type | Template | Background |
|-----------|----------|------------|
| Welcome, brand, "hello world" | **A — Centered** | Brand blue `#3C5AA5` |
| Tip, fact, quote, educational | **B — Left-heavy** | Brand green `#3CB45A` |
| Launch, event, big news | **A — Centered** (bold) | Yellow `#F0D200` + text `#333333` |
| App download, product promo | **A — Centered** | Brand blue `#3C5AA5` |
| Motivational | **A — Centered** | Deep blue `#2D5AB4` |

### Design principles (apply to every post)

**1. Choose one hero element and make it BOLD**
Every post needs one focal point. For Template B (educational), this is always the large
3D letter or icon. Use `placement: "bleed-right"` with `size_scale: 1.2–1.4` so it
extends beyond the post edge — this looks editorial and confident, not clip-art.

**2. Always use bg_overlay for depth**
A flat solid background looks cheap. Every post should include:
```json
"bg_overlay": {"color": "#000000", "opacity": 14}
```
This adds subtle richness to any background color. Increase to 18–20% for deeper effect.

**3. Use 3 decorative elements max — not 4–6**
3 elements chosen with intention > 6 elements placed by default.
The formula: 1 hero (bleed-right) + 1 top accent + 1 bottom accent.
Leave at least 2 corners completely empty — that breathing room reads as intentional design.

**4. Add rotation to every decorative element**
Static axis-aligned elements look placed, not designed. Give each element a slight rotation:
```json
{"file": "star-yellow-3d.png", "placement": "top-left", "rotation": -0.35, "size_scale": 1.1}
```
Mix directions (positive = clockwise, negative = counter-clockwise).

**5. Body text color: soft, not pure white**
On green backgrounds: `#D4F0DC` (soft light green) reads better than `#FFFFFF`.
On blue backgrounds: `#B4D4F0` (soft light blue). Pure white only for headlines.

### Asset selection
Pick assets that match the post's **energy and topic**:
- Celebrations → stars, sparkles, plus shapes
- Education → letter assets, student icon
- Urgency / launch → orange/purple triangles, diamond shapes
- App / product → tablet mockup, download button, app icon
- Multilingual → Urdu letter assets (`urdu-letter-dal-3d-yellow.png`, `urdu-letter-ze-3d-green.png`)

---

## Step 3 — Build the Scene Config

Create a `post_config.json` in the project's `Posts/` folder (create it if it doesn't exist).

**Centered post example (brand/welcome):**
```json
{
  "template": "centered",
  "headline": "Welcome to",
  "body_text": "",
  "bg_color": "#3C5AA5",
  "bg_overlay": {"color": "#000000", "opacity": 14},
  "text_color": "#FFFFFF",
  "assets_dir": "/absolute/path/to/Assets",
  "logo": "Green BG@4x.png",
  "tagline_image": "text-lets-fuel-learning.png",
  "decorative": [
    {"file": "blob-3d-light-blue.png",      "placement": "bleed-right",   "size_scale": 1.3, "rotation": 0.2},
    {"file": "sparkle-stars-3d-yellow.png", "placement": "top-left",      "size_scale": 1.1, "rotation": -0.35},
    {"file": "plus-3d-blue.png",            "placement": "corner-bl",     "size_scale": 0.9, "rotation": 0.5}
  ]
}
```

**Educational/tip post example (left-heavy):**
```json
{
  "template": "left_heavy",
  "headline": "Learn Urdu\nFaster!",
  "body_text": "Read stories aloud daily —\nbuilds vocabulary & confidence!",
  "bg_color": "#3CB45A",
  "bg_overlay": {"color": "#000000", "opacity": 16},
  "text_color": "#FFFFFF",
  "assets_dir": "/absolute/path/to/Assets",
  "logo": "taleemabad-logo-v3.png",
  "decorative": [
    {"file": "urdu-letter-dal-3d-yellow.png", "placement": "bleed-right",  "size_scale": 1.3, "rotation": 0.15},
    {"file": "star-yellow-3d.png",            "placement": "top-left",     "size_scale": 1.1, "rotation": -0.4},
    {"file": "plus-3d-yellow.png",            "placement": "corner-bl",    "size_scale": 0.8, "rotation": 0.6}
  ]
}
```

**Placement options:**
| Placement | Description |
|-----------|-------------|
| `top-left` / `top-right` | Bleed outside top corners |
| `bottom-left` / `bottom-right` | Bleed outside bottom corners |
| `corner-tr` / `corner-bl` | Small accent inside corners |
| `center-right` | Hero graphic, right half, contained inside post |
| `bleed-right` | **OVERSIZED hero**, right side, extends beyond post edge — dramatic |
| `bleed-bottom` | Large element bleeding off the bottom |

**Per-element options:**
- `"rotation"`: radians — `0.2` to `0.5` (slight tilt), `-0.4` (counter-clockwise). Mix +/−.
- `"size_scale"`: `1.0`=default, `1.2–1.5`=hero, `0.8`=small accent

---

## Step 4 — Generate the Scene

Run the build script:

```bash
python {skill_dir}/scripts/build_scene.py \
  --config {posts_dir}/post_config.json \
  --output {posts_dir}/scene.json
```

Where `{skill_dir}` is the directory containing this SKILL.md.

Then import into Excalidraw:

```python
# Via MCP tool:
mcp__excalidraw__import_scene(filePath="{posts_dir}/scene.json", mode="replace")
```

---

## Step 5 — Verify with Screenshot

Call `mcp__excalidraw__get_canvas_screenshot()` and visually check:
- All 3 posts are visible side by side
- Text is readable and centered
- Logo and tagline are clearly visible
- Decorative elements are at the edges without covering key content
- Nothing is cut off

If something looks wrong, adjust `post_config.json` and re-run Step 4.

**Common fixes:**
- Text cut off → reduce font size or `top_pad` in template
- Logo too big/small → adjust `logo_w` values in the config or script
- Decorative element overlaps text → change its `placement` or remove it

---

## Step 6 — Export & Crop

Export the full canvas:

```python
mcp__excalidraw__export_to_image(
    format="png",
    filePath="{posts_dir}/full_canvas.png",
    background=True
)
```

Then crop into individual posts:

```bash
python {skill_dir}/scripts/crop_posts.py \
  --input {posts_dir}/full_canvas.png \
  --output-dir {posts_dir} \
  --prefix {post-slug}
```

This saves **2x high-DPI images** (Retina-ready, sharp on all screens):
- `{posts_dir}/{post-slug}-linkedin.png` — **2400×1256px** (2× LinkedIn standard)
- `{posts_dir}/{post-slug}-instagram.png` — **2160×2160px** (2× Instagram standard)
- `{posts_dir}/{post-slug}-x_twitter.png` — **2400×1350px** (2× X/Twitter standard)

And automatically deletes the temporary `full_canvas.png`.

**Why 2x?** Social media platforms render images on Retina/4K displays. 1x images (1200×628) look blurry on modern phones and monitors. 2x images look sharp everywhere and are accepted by all platforms.

---

## Step 7 — Verify Quality & Confirm with User

Run this quality check before showing the user:

```bash
python3 -c "
from PIL import Image
import os, sys
posts_dir = '{posts_dir}'
prefix = '{post-slug}'
specs = [
    (prefix+'-linkedin.png',   2400, 1256),
    (prefix+'-instagram.png',  2160, 2160),
    (prefix+'-x_twitter.png',  2400, 1350),
]
ok = True
for fname, exp_w, exp_h in specs:
    path = os.path.join(posts_dir, fname)
    img = Image.open(path)
    w, h = img.size
    size_kb = os.path.getsize(path) // 1024
    status = 'OK' if (w == exp_w and h == exp_h and size_kb > 300) else 'FAIL'
    print(f'[{status}] {fname}: {w}x{h} px, {size_kb} KB')
    if status == 'FAIL':
        ok = False
        if w != exp_w or h != exp_h:
            print(f'       Expected {exp_w}x{exp_h}')
        if size_kb <= 300:
            print(f'       File too small ({size_kb} KB) — may indicate low quality export')
sys.exit(0 if ok else 1)
"
```

If any check fails:
- Wrong dimensions → verify `build_scene.py` SCALE=2 and re-run Steps 4–6
- File too small → Excalidraw may have exported at low resolution; try re-exporting

Then show a preview of all 3 saved images using the Read tool (renders inline).
Tell the user:
- Where the files were saved
- The exact 2x dimensions of each
- Any design choices you made (template, colors, assets) and why

---

## Quality Checklist

Before finishing, verify each post has:
- [ ] **Resolution**: 2400×1256 (LinkedIn), 2160×2160 (Instagram), 2400×1350 (X/Twitter)
- [ ] **File size**: Each PNG > 300 KB (indicates sufficient pixel detail)
- [ ] **DPI**: 144 dpi metadata set (2× standard 72dpi)
- [ ] Brand colors used correctly (no off-brand colors)
- [ ] Logo is clearly visible and not pixelated
- [ ] Headline text is sharp and readable (white on blue/green, dark on yellow)
- [ ] 4–6 decorative elements adding visual energy without clutter
- [ ] `taleemabad.com` watermark present
- [ ] Content doesn't bleed into the post boundary (text/logo safely inside)
- [ ] Decorative elements only bleed at edges, not over center content

---

## Reference Files

- `references/assets-catalog.md` — full asset list with descriptions and use cases
- `references/post-templates.md` — layout templates, color themes, element formulas, aspect ratios
- `scripts/build_scene.py` — generates Excalidraw scene JSON from config
- `scripts/crop_posts.py` — crops the full canvas export into platform-specific PNGs
