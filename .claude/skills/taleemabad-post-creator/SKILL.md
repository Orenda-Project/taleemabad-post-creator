---
name: taleemabad-post-creator
description: >
  Create branded social media posts for Taleemabad — high-DPI 2x resolution output:
  LinkedIn 2400×1256, Instagram 2160×2160, X/Twitter 2400×1350 (sharp on all screens).
  Uses UI UX Pro Max design intelligence + Excalidraw. Use this skill whenever the user asks
  to create, design, generate, or update a social media post, graphic, banner, or
  visual — even if they just describe the topic without saying "post" or "design".
  The skill handles design system generation, layout composition, all three platform sizes,
  Excalidraw canvas composition, and saving final PNG files to the Posts/ folder.
---

# Taleemabad Social Post Creator (UI UX Pro Max Edition)

This skill turns a plain description into three polished, on-brand social media
post images (LinkedIn, Instagram, X/Twitter) using **UI UX Pro Max design intelligence**
and the Excalidraw MCP. Assets from the library are **optional** — the design is driven
by generated visual styles, gradients, shapes, and typography, not fixed templates.

---

## Prerequisites

Before starting, verify:
1. **Excalidraw canvas is running** — call `mcp__excalidraw__describe_scene`. If it
   returns a connection error, tell the user to run:
   ```bash
   cd ~/mcp_excalidraw && docker-compose up
   ```
   and open `http://localhost:3000` in a browser.

2. **Python is available** — needed for UI UX Pro Max search and crop scripts.
   ```bash
   python3 --version
   ```

3. **Assets folder** — check for `{project_root}/Assets/` (logos live here). Only logos
   are required; decorative assets are now optional.

---

## Step 1 — Understand the Post

Infer from the user's message or ask:

| Question | Why it matters |
|----------|----------------|
| **What is the post about?** | Topic drives the design system generation |
| **Tone?** (celebratory / educational / urgent / warm / professional) | Drives style selection |
| **Any specific text?** | Headline and optional body copy |
| **Visual direction preference?** | e.g. "modern", "bold", "clean", "vibrant" — optional |
| **Output folder?** | Default is `{project_root}/Posts/` |

If the user's message already answers these, don't ask — just proceed.

---

## Step 2 — Generate Design System with UI UX Pro Max

**This replaces the old fixed template table.** Use UI UX Pro Max to generate a complete
design system tailored to the post topic and tone.

### Run the design system generator:
```bash
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "{topic} {tone} social media post" \
  --design-system -p "Taleemabad" -f markdown
```

Example for an educational post:
```bash
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "educational EdTech learning Pakistan social media" \
  --design-system -p "Taleemabad" -f markdown
```

### From the output, extract and adapt:
| UI UX Pro Max Output | How to use for Taleemabad posts |
|----------------------|----------------------------------|
| **Style** | Use as the visual treatment (glassmorphism, bento, bold, claymorphism, etc.) |
| **Colors** | Use as accent/gradient — but keep Taleemabad blue `#3C5AA5` or green `#3CB45A` as primary |
| **Typography mood** | Drives font weight and layout hierarchy in Excalidraw text elements |
| **Key Effects** | Apply as Excalidraw element styling (shadows, gradients, rounded corners) |
| **Pattern** | Use as layout guide (hero-centric, left-heavy, bento grid, etc.) |
| **Anti-patterns** | Avoid these in the design |

### Taleemabad brand anchors (always keep these):
- **Primary colors**: Blue `#3C5AA5`, Green `#3CB45A`, Yellow `#F0D200`
- **Logo**: Always include — choose from Assets/ based on background
- **Website**: `taleemabad.com` watermark on every post
- **Accent colors**: Take from UI UX Pro Max recommendations

---

## Step 3 — Design the Layout in Excalidraw (No Script Required)

Instead of running `build_scene.py`, **build the post directly in Excalidraw** using
the MCP tools. This gives full creative freedom to apply any visual style from UI UX Pro Max.

### Canvas setup — place 3 posts side by side:

Use these base dimensions (1x, Excalidraw units — the export script will handle 2x):

| Platform | Width | Height | Canvas X position |
|----------|-------|--------|-------------------|
| LinkedIn | 1200  | 628    | 0                 |
| Instagram| 1080  | 1080   | 1300              |
| X/Twitter| 1200  | 675    | 2500              |

### Build each post using mcp__excalidraw__batch_create_elements:

**1. Background rectangle** (always first):
```json
{
  "type": "rectangle",
  "x": 0, "y": 0,
  "width": 1200, "height": 628,
  "backgroundColor": "#3C5AA5",
  "strokeColor": "transparent",
  "fillStyle": "solid",
  "roughness": 0,
  "roundness": null
}
```

For gradient-style backgrounds (glassmorphism, aurora, etc.), layer 2-3 rectangles
with different colors and low opacity (use `opacity: 30-60`) to simulate gradient depth.

**2. Apply the UI UX Pro Max style as visual elements:**

- **Glassmorphism** → frosted rectangle overlays (`opacity: 20-40`, white stroke)
- **Bold/Neubrutalism** → thick border rectangles, hard shadows offset by 4-6px
- **Bento Grid** → subdivide the post into card sections with rounded rectangles
- **Claymorphism** → large rounded shapes (`roundness` high) with soft shadows
- **Minimalism** → heavy typography, lots of whitespace, 1-2 accent shapes only
- **Aurora/Vibrant** → overlapping ellipses with soft colors at low opacity as background layer

**3. Decorative shapes (generated, not from Assets/):**
Use Excalidraw native shapes — ellipses, diamonds, stars — instead of PNG assets.
Style them using the UI UX Pro Max color palette. Examples:
```json
{"type": "ellipse", "backgroundColor": "#F0D200", "opacity": 40, "width": 300, "height": 300}
{"type": "diamond", "backgroundColor": "#3CB45A", "opacity": 60, "width": 200, "height": 200}
```

**4. Text elements — hierarchy driven by UI UX Pro Max typography:**
- Headline: Bold, large (48-72px equivalent), white or high-contrast
- Body: Regular weight, 24-32px, soft color (not pure white — use `#D4F0DC` on green, `#B4D4F0` on blue)
- Watermark: `taleemabad.com` — small, bottom corner, 50% opacity

**5. Logo (optional, not mandatory):**
Only add the logo image if the design needs it. Place it top-left or bottom-left.
Never centered unless the logo IS the hero of the post.

### Design quality rules (from UI UX Pro Max):
- **One hero focal point** — everything else supports it
- **3-level hierarchy**: dominant → secondary → supporting
- **Breathing room** — leave 20-30% of the canvas empty
- **Contrast ratio** — text must be 4.5:1 minimum against background
- **Depth through layers** — stack elements at different opacities
- **No emoji icons** — use geometric shapes or text only
- **Consistent corner radius** — pick one value (0, 8, 16, or 30) and use it everywhere

---

## Step 4 — Verify with Screenshot

```python
mcp__excalidraw__get_canvas_screenshot()
```

Check:
- All 3 posts visible side by side
- Text is readable and hierarchy is clear
- Design style is consistent across all 3 sizes
- Logo and `taleemabad.com` are present
- Nothing important is cut off at edges

If it doesn't look good — **redesign it**. Adjust colors, shapes, layout. The goal is
a post the user actually likes, not one that passes a checklist.

---

## Step 5 — Export & Crop

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

This saves **2x high-DPI images**:
- `{posts_dir}/{post-slug}-linkedin.png` — **2400x1256px**
- `{posts_dir}/{post-slug}-instagram.png` — **2160x2160px**
- `{posts_dir}/{post-slug}-x_twitter.png` — **2400x1350px**

---

## Step 6 — Quality Check

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
sys.exit(0 if ok else 1)
"
```

Then show previews of all 3 images using the Read tool and tell the user:
- Where files were saved
- What design style was applied (from UI UX Pro Max) and why
- What colors and effects were used

---

## Design Style Quick Reference

Use this when the user doesn't specify a direction — pick based on post tone:

| Post Tone | Recommended Style | Background Treatment |
|-----------|-------------------|----------------------|
| Educational / Informative | **Bento Grid** or **Minimalism** | Clean blue, card sections |
| Celebratory / Launch | **Vibrant & Block-based** or **Aurora** | Bold colors, layered shapes |
| Professional / B2B | **Swiss Modernism** or **Flat Design** | Clean, high contrast |
| Warm / Community | **Claymorphism** or **Soft UI** | Rounded, pastel accents |
| Urgent / CTA | **Neubrutalism** | High contrast, thick borders |
| Premium / Achievement | **Glassmorphism** | Dark base, frosted overlays |

---

## Reference Files

- `references/assets-catalog.md` — logos and optional decorative assets (use sparingly)
- `references/post-templates.md` — legacy templates (reference only, not required)
- `scripts/crop_posts.py` — crops full canvas export into platform PNGs
- `.claude/skills/ui-ux-pro-max/scripts/search.py` — design system generator
