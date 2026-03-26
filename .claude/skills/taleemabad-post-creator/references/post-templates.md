# Post Layout Templates

## Platform Dimensions
| Platform | Size (1x) | Output Size (2x) | Canvas offset |
|----------|-----------|------------------|---------------|
| LinkedIn | 1200 × 628 px | 2400 × 1256 px | ox=0, oy=0 |
| Instagram | 1080 × 1080 px | 2160 × 2160 px | ox=1280, oy=0 |
| X/Twitter | 1200 × 675 px | 2400 × 1350 px | ox=2440, oy=0 |

Gap between posts on canvas: 80px (160px at 2x scale)

---

## Core Design Principles

These principles separate professional-looking social posts from generic AI output.
Apply them when choosing templates, placing elements, and writing configs.

### 1. One hero, everything else supports it
Pick **one** element to be the visual star — a large 3D letter, an icon, a bold word.
Make it significantly larger than everything else (at least 3–4× bigger than accent elements).
Avoid distributing equal weight across 6 elements — that's how you get visual noise.

**Wrong:** 6 small decorative elements spread evenly in all corners
**Right:** 1 oversized hero element + 2–3 small accents

### 2. Scale contrast creates hierarchy
When everything is a similar size, nothing has meaning.
Combine dramatically different scales: huge headline + tiny watermark, massive 3D letter + small logo.
The ratio should feel slightly too extreme — that's when it starts looking designed.

### 3. Bleed elements for energy
Let the hero element extend **beyond the post boundary** using `bleed-right` or `bleed-bottom` placement.
This creates the impression of a larger world beyond the frame — editorial, confident, dynamic.
A cropped element always feels more intentional than one that fits neatly inside.

### 4. Depth through layering (bg_overlay)
A flat solid background reads as cheap. Add a subtle dark or light overlay (10–20% opacity)
to give the background dimension. Use `"bg_overlay": {"color": "#000000", "opacity": 15}`
for a rich, slightly deepened feel — especially effective on green backgrounds.

### 5. Breathing room is not wasted space
Fight the urge to fill every corner. Strategic empty space makes the post feel premium.
The left text zone in Template B works best when text occupies 40–50% of the post width,
leaving the rest as either the hero element or open air.

### 6. Text hierarchy: lead with contrast
Headline should be dramatically larger than body text (at least 2× the font size).
Body text reads better at a slightly off-white color (e.g., `#D4F0DC` on green)
than pure white — softer and easier to read without losing contrast.

### 7. Rotation adds life
Static, axis-aligned elements look placed rather than designed.
Adding a slight rotation (`"rotation": 0.2` to `0.5`) to decorative elements
makes them feel spontaneous and energetic. The 3D assets especially benefit from this.

### 8. Fewer, stronger
3–4 decorative elements chosen with intention > 6 elements added by default.
Ask: does each element add energy and support the visual story, or is it just filling space?
If it's just filling space, remove it.

---

## Template A — Centered (Welcome, Brand, Motivational)

Best for: Posts where the logo and tagline ARE the message.

```
[Background — full post, brand blue #3C5AA5]
[bg_overlay — dark, 12-18% opacity for depth]
[Decorative bleed elements — 3-4 max, mix of large bleed + small corners]
  - blob/sparkle: bleed-right (large, oversized, right half)
  - accent shapes: top-left corner and bottom-right corner only
[Headline text — "Welcome to" / post topic — centered, Lilita font, white]
  y = oy + top_pad  (top_pad: LinkedIn=38, Instagram=90, X=40)
[Logo image — centered horizontally]
  logo_w: LinkedIn=360, Instagram=480, X=360
  y = headline_y + headline_height + 12
[Tagline image — centered horizontally]
  tag_w: LinkedIn=340, Instagram=460, X=340
  y = logo_y + logo_h + 14
[Domain watermark — taleemabad.com, light blue, small, centered]
  y = tagline_y + tagline_h + 10
```

Font sizes (headline):
- LinkedIn: 52px
- Instagram: 82px
- X/Twitter: 54px

**Config example with depth:**
```json
{
  "template": "centered",
  "bg_color": "#3C5AA5",
  "bg_overlay": {"color": "#000000", "opacity": 14},
  "decorative": [
    {"file": "blob-3d-light-blue.png",      "placement": "bleed-right",   "size_scale": 1.4, "rotation": 0.2},
    {"file": "sparkle-stars-3d-yellow.png", "placement": "top-left",      "size_scale": 1.2, "rotation": -0.3},
    {"file": "plus-3d-blue.png",            "placement": "corner-bl",     "size_scale": 0.9, "rotation": 0.5}
  ]
}
```

---

## Template B — Left-Heavy (Educational, Tips, Quotes)

Best for: Posts with a short headline + supporting visual on the right.

**The key principle:** The hero graphic should feel BOLD — not balanced. It should
take up 60–80% of the post height and use `bleed-right` to crop off the right edge.
The left text zone gets the headline, body, and logo with generous breathing room.

```
[Background — brand green #3CB45A or blue #3C5AA5]
[bg_overlay — dark, 12-18% opacity for richness]
[Hero element — RIGHT side, OVERSIZED, placement: "bleed-right"]
  size_scale: 1.2–1.6 (bigger than default)
  rotation: subtle angle 0.1–0.3 for energy
[Headline text — large, LEFT-aligned, white]
  x = ox + 70, y = oy + H*0.16, width = W*0.48
[Body text — smaller, LEFT-aligned, soft light color #D4F0DC]
  y = headline_y + (headline_font * 3.5)
[Logo — bottom-left, x = ox+50, y = oy+H-logo_h-40]
[Domain watermark — small, bottom-left area]
[2–3 small accent elements in corners — not all corners, leave some empty]
```

Font sizes (headline):
- LinkedIn: 64px
- Instagram: 80px
- X/Twitter: 64px

**Config example — Urdu tip post:**
```json
{
  "template": "left_heavy",
  "bg_color": "#3CB45A",
  "bg_overlay": {"color": "#000000", "opacity": 16},
  "decorative": [
    {"file": "urdu-letter-dal-3d-yellow.png", "placement": "bleed-right",  "size_scale": 1.3, "rotation": 0.15},
    {"file": "star-yellow-3d.png",            "placement": "top-left",     "size_scale": 1.1, "rotation": -0.4},
    {"file": "plus-3d-yellow.png",            "placement": "corner-bl",    "size_scale": 0.8, "rotation": 0.6}
  ]
}
```

---

## Template C — Bold Announcement

Best for: Launches, events, important news.

```
[Background — yellow #F0D200 or white]
[Color block — brand blue or green, left 60% panel]
  rectangle: x=ox, y=oy, w=W*0.6, h=H
[bg_overlay on full post — subtle dark, 8-12%]
[Headline — large, bold, white on blue panel]
[Sub-headline — smaller, dark on yellow panel]
[Logo — top-right on yellow panel]
[CTA button image — btn-download-now.png if relevant]
[Decorative: orange triangles at angles, yellow ovals bleeds]
```

Font sizes (headline):
- LinkedIn: 64px
- Instagram: 90px
- X/Twitter: 66px

---

## Template D — App Showcase

Best for: Promoting the mobile app.

```
[Background — brand blue #3C5AA5]
[bg_overlay — light, #69E169 (light green), 10% opacity for gradient simulation]
[Tablet mockup — right side, large, bleed-right or bleed-bottom]
  placement: "bleed-right", size_scale: 1.3
[Logo — top-left]
[Headline — left side, white, bold, large]
[Tagline — left side, smaller, light blue]
[Download button — btn-download-now.png, left side below headline]
[Decorative: 2-3 max, corners only]
```

---

## Decorative Element Strategy

### The 3-element formula (preferred)
Most posts work best with exactly 3 decorative elements:
1. **Hero** — one large element using `bleed-right` or `center-right`, `size_scale: 1.2–1.6`
2. **Top accent** — one element using `top-left` or `top-right`, slight rotation
3. **Bottom accent** — one small element using `corner-bl` or `corner-tr`, different rotation

### Rotation guide
| Effect | rotation value |
|--------|---------------|
| Very subtle | 0.1 to 0.2 |
| Noticeable tilt | 0.3 to 0.5 |
| Strong diagonal | 0.6 to 1.0 |
| Counter-clockwise | negative values (-0.3 to -0.8) |

Mix directions: if one element tilts right (+), have another tilt left (−).

### Size scale guide
| Use | size_scale |
|-----|-----------|
| Smaller accent | 0.7–0.9 |
| Default size | 1.0 |
| Slightly bolder | 1.1–1.3 |
| Hero/statement piece | 1.4–1.8 |

---

## Color Themes by Post Type

| Post Type | Background | bg_overlay | Accent | Text |
|-----------|------------|------------|--------|------|
| Welcome / Brand | `#3C5AA5` (brand blue) | `#000000` 14% | `#F0D200` yellow | `#FFFFFF` |
| Educational | `#3CB45A` (brand green) | `#000000` 16% | `#F0D200` yellow | `#FFFFFF` |
| Announcement | `#F0D200` (yellow) | `#3C5AA5` 20% | blue panel | `#333333` / `#FFFFFF` |
| App Promotion | `#3C5AA5` (brand blue) | `#69E169` 10% | light green | `#FFFFFF` |
| Motivational | `#2D5AB4` (deep blue) | `#000000` 20% | `#E1963C` orange | `#FFFFFF` |
| Multilingual | `#3C5AA5` (brand blue) | `#874B96` 12% | purple | `#FFFFFF` |

---

## Image Element Formula (Excalidraw)

```python
def img_el(fid, x, y, w, h, angle=0, opacity=100):
    return {
        'type': 'image', 'id': unique_id(),
        'x': x, 'y': y, 'width': w, 'height': h,
        'fileId': fid, 'status': 'saved',
        'angle': angle, 'opacity': opacity,
        'strokeColor': 'transparent', 'backgroundColor': 'transparent',
        'roughness': 0, 'groupIds': [], 'frameId': None,
        'boundElements': [], 'locked': False,
    }
```

## Text Element Formula (Excalidraw)

```python
def txt(text, x, y, width, font_size, color, family=7, align='left'):
    # family: 7=Lilita (bold/playful), 2=Helvetica (clean), 1=Virgil (sketchy)
    return {
        'type': 'text', 'id': unique_id(),
        'x': x, 'y': y, 'width': width, 'height': int(font_size * 1.4),
        'text': text, 'originalText': text,
        'fontSize': font_size, 'fontFamily': family,
        'textAlign': align, 'verticalAlign': 'top',
        'strokeColor': color, 'backgroundColor': 'transparent',
        'roughness': 0, 'opacity': 100, 'angle': 0,
        'lineHeight': 1.25, 'containerId': None,
        'groupIds': [], 'frameId': None, 'boundElements': [], 'locked': False,
    }
```

## Asset Aspect Ratios (for sizing)

| Asset | Native W | Native H | Ratio |
|-------|----------|----------|-------|
| Green BG@4x.png (logo) | 764 | 479 | 0.627 h/w |
| taleemabad-logo-green-shadow.png | 764 | 479 | 0.627 h/w |
| taleemabad-logo-v3.png | 622 | 392 | 0.630 h/w |
| taleemabad-logo-white-text.png | 1447 | 306 | 0.211 h/w |
| text-lets-fuel-learning.png | 946 | 504 | 0.533 h/w |
| taleemabad-tablet-mockup.png | varies | varies | check with PIL |
| taleemabad-student-icon.png | ~128 | ~128 | 1.0 |
| taleemabad-app-icon.png | ~232 | ~232 | 1.0 |
| btn-download-now.png | varies | varies | check with PIL |

Formula: `img_height = int(img_width * native_h / native_w)`
