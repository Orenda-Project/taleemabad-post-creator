# Taleemabad Social Post Creator

An AI-powered social media post design kit for Taleemabad. Uses **Claude Code** + **Excalidraw** (via Docker) to generate on-brand posts for LinkedIn, Instagram, and X/Twitter — at Retina quality (2x) — from a single text prompt.

> **No Photoshop. No design skills. Just describe the post and Claude builds it.**

---

## What It Produces

Three platform-ready PNGs per post, automatically cropped and sized:

| Platform | Output Size | Notes |
|----------|-------------|-------|
| LinkedIn | 2400 × 1256 px | 2× standard (Retina-sharp) |
| Instagram | 2160 × 2160 px | 2× standard square |
| X / Twitter | 2400 × 1350 px | 2× standard |

All files saved to `Posts/` with 144 DPI metadata.

---

## Prerequisites

| Tool | Version | Install |
|------|---------|---------|
| [Claude Code](https://claude.ai/code) | Latest | `npm install -g @anthropic-ai/claude-code` |
| [Docker](https://docs.docker.com/get-docker/) | 20+ | docker.com |
| Docker Compose | 2+ | Included with Docker Desktop |
| Python 3 | 3.8+ | python.org |
| Pillow (Python) | Any | `pip install Pillow` |

---

## Step 1 — Clone the Repository

```bash
git clone https://github.com/Orenda-Project/taleemabad-work.git
cd taleemabad-work
```

---

## Step 2 — Start the Excalidraw Canvas Server

This project uses a local Excalidraw server (via Docker) as a canvas. Claude renders post elements onto it, then exports a high-res PNG.

```bash
# Clone the MCP Excalidraw server (one-time setup)
git clone https://github.com/azorawel/mcp-excalidraw ~/mcp_excalidraw
cd ~/mcp_excalidraw

# Start the server
docker-compose up -d
```

Then open **http://localhost:3000** in your browser — you should see a blank Excalidraw canvas.

> **Keep this tab open** while using the post creator. Excalidraw renders the posts live in the browser, and Claude exports them from there.

To stop the server:
```bash
cd ~/mcp_excalidraw && docker-compose down
```

### Verify the server is running

```bash
curl -s http://localhost:3000 | grep -o "Excalidraw" | head -1
# Should print: Excalidraw
```

---

## Step 3 — Configure Claude Code

The skill is already included in `.claude/skills/taleemabad-post-creator/`. You just need Claude Code to point to this project directory.

```bash
cd taleemabad-work
claude  # starts Claude Code in this project
```

Claude will automatically detect the skill and the `/create-post` command.

---

## Step 4 — Create a Post

In Claude Code, run:

```
/create-post <describe your post topic>
```

**Examples:**

```
/create-post Welcome post for our new school year

/create-post Educational tip about reading Urdu stories

/create-post Announcement: Taleemabad app is now on Android

/create-post Our HR team is using AI to create content — share your thoughts
```

Claude will:
1. Choose a template and color scheme
2. Select appropriate brand assets from `Assets/`
3. Build the scene on the Excalidraw canvas
4. Export and crop all 3 platform images
5. Run a quality gate check (resolution + file size)
6. Show you the final images inline

---

## Project Structure

```
taleemabad-work/
│
├── Assets/                          # 60+ brand assets (logos, 3D shapes, letters)
│   ├── Green BG@4x.png              # Primary Taleemabad logo
│   ├── taleemabad-logo-v3.png       # Logo with "Smart Learning Program" tag
│   ├── sparkle-stars-3d-yellow.png  # Celebration / energy element
│   ├── urdu-letter-dal-3d-yellow.png
│   └── ...
│
├── .claude/
│   ├── commands/
│   │   └── create-post.md           # /create-post slash command definition
│   └── skills/
│       └── taleemabad-post-creator/
│           ├── SKILL.md             # Full skill instructions (design principles, workflow)
│           ├── references/
│           │   ├── assets-catalog.md    # Every asset with usage notes
│           │   └── post-templates.md    # Layout templates + design principles
│           └── scripts/
│               ├── build_scene.py   # Generates Excalidraw JSON from post_config.json
│               └── crop_posts.py    # Crops full canvas export into platform PNGs
│
├── Color Palette/
│   ├── colors.css                   # CSS variables for all brand colors
│   ├── colors.json                  # JSON color tokens
│   └── color-palette.html           # Visual preview of the palette
│
├── Posts/                           # Generated post images (git-ignored)
│
└── README.md
```

---

## How It Works (Technical)

```
User prompt
    │
    ▼
Claude reads SKILL.md + asset catalog + templates
    │
    ▼
Writes Posts/post_config.json
    │
    ▼
build_scene.py  ──────────────────────────────────────────►  Posts/scene.json
  • Builds all 3 platform posts at 2× canvas coordinates        (Excalidraw JSON)
  • Embeds assets as base64                                        │
  • Applies bg_overlay, rotation, size_scale                       │
                                                                   ▼
                                                        Excalidraw MCP
                                                        (Docker on :3000)
                                                          imports scene
                                                                   │
                                                                   ▼
                                                        export_to_image()
                                                          → full_canvas.png
                                                          (~7400 × 2200 px)
                                                                   │
                                                                   ▼
crop_posts.py  ────────────────────────────────────────────────────┘
  • Calculates scale from export dimensions
  • Crops each platform region
  • Resizes with LANCZOS to exact 2× dimensions
  • Saves with 144 DPI metadata
    │
    ▼
Posts/
  {slug}-linkedin.png    2400×1256
  {slug}-instagram.png   2160×2160
  {slug}-x_twitter.png   2400×1350
```

---

## Post Configuration Reference

The post config (`Posts/post_config.json`) drives what `build_scene.py` renders:

```json
{
  "template": "centered | left_heavy",
  "headline": "Your Headline\nSecond Line",
  "body_text": "Supporting text here",
  "bg_color": "#3C5AA5",
  "bg_overlay": {
    "color": "#000000",
    "opacity": 14
  },
  "text_color": "#FFFFFF",
  "assets_dir": "/absolute/path/to/Assets",
  "logo": "Green BG@4x.png",
  "tagline_image": "text-lets-fuel-learning.png",
  "decorative": [
    {
      "file": "sparkle-stars-3d-yellow.png",
      "placement": "bleed-right",
      "size_scale": 1.2,
      "rotation": 0.2
    },
    {
      "file": "star-yellow-3d.png",
      "placement": "top-left",
      "size_scale": 1.0,
      "rotation": -0.35
    }
  ]
}
```

### Templates

| Template | Best for | Background |
|----------|----------|------------|
| `centered` | Welcome, brand, motivational | Brand blue `#3C5AA5` |
| `left_heavy` | Tips, facts, educational | Brand green `#3CB45A` |

### Placement Options

| Value | Effect |
|-------|--------|
| `top-left` / `top-right` | Bleed outside top corners |
| `bottom-left` / `bottom-right` | Bleed outside bottom corners |
| `corner-tr` / `corner-bl` | Small accent inside corners |
| `center-right` | Hero graphic contained inside right half |
| `bleed-right` | **Oversized hero, extends beyond right edge** |
| `bleed-bottom` | Large element bleeding off bottom |

### Brand Colors

| Name | Hex |
|------|-----|
| Brand Blue | `#3C5AA5` |
| Deep Blue | `#2D5AB4` |
| Brand Green | `#3CB45A` |
| Yellow | `#F0D200` |
| Orange | `#E1963C` |
| Purple | `#874B96` |

---

## Design Principles

The skill follows these rules on every post (see `references/post-templates.md` for full detail):

1. **One hero element** — choose one focal element and make it large (`bleed-right`, `size_scale: 1.2+`)
2. **Always use `bg_overlay`** — a dark overlay at 12–18% opacity adds depth to any flat background
3. **3 decorative elements max** — 1 hero + 1 top accent + 1 bottom accent. Leave some corners empty.
4. **Rotate every decorative element** — mix clockwise and counter-clockwise angles (0.2–0.5 radians)
5. **Soft body text** — `#D4F0DC` on green, `#B4D4F0` on blue (not pure white)

---

## Troubleshooting

**Excalidraw canvas not responding**
```bash
cd ~/mcp_excalidraw
docker-compose down && docker-compose up -d
# Then refresh http://localhost:3000
```

**`command not found: python`**
```bash
# Use python3 explicitly, or create an alias:
alias python=python3
```

**Images look blurry**
The build scripts use `SCALE = 2` — if you see 1× output (1200×628 for LinkedIn), check that you're running the scripts from this repo (not an older copy).

**Posts/ folder is empty after running**
Make sure `full_canvas.png` was exported before `crop_posts.py` ran. Re-run from Step 4 in the skill.

---

## Contributing

Assets live in `Assets/`. To add a new brand asset:
1. Drop the PNG into `Assets/`
2. Add an entry to `.claude/skills/taleemabad-post-creator/references/assets-catalog.md`
3. It becomes immediately available to the skill

---

## License

Internal Taleemabad brand kit — not for redistribution.
