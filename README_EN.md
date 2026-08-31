# anime-image-restyle — Anime Style Transfer Skill

[English](README_EN.md) | [中文](README.md)

A skill package for any AI assistant that supports skills — Claude Code, WorkBuddy, OpenClaw, Cursor, and others.

**In one line**: the user uploads a photo, names a style, and the AI returns a finished illustration in that anime style.

```
[upload photo] convert to watercolor
[upload photo] guofeng-gongbi heavy color, 9:16, faithful
[upload photo] cyberpunk, simplified background, strong
```

![version](https://img.shields.io/badge/version-1.1.0-blue)
![license](https://img.shields.io/badge/license-MIT-green)
![dependencies](https://img.shields.io/badge/dependencies-none-brightgreen)

---

## 1. Prerequisites (required)

This is **not** a pure prompt skill. The host AI must have:

1. **Image-to-image generation** — the ability to accept *one input image + a text instruction* and return a new image.
   Environments limited to text-to-image cannot run the core workflow.
2. **Local file read access** — to load `references/*.md` and the source image.
3. **Python 3** *(optional)* — only needed when the user asks to keep the original aspect ratio, to detect landscape vs. portrait.

`scripts/probe_image.py` uses only the Python standard library. No `pip install` required.

---

## 2. Install

The repository root **is** the skill. Clone it and copy the whole folder into your skills directory.

### From GitHub

```bash
git clone https://github.com/OWNER/anime-image-restyle-skill.git
```

### Or download a release zip

Grab `anime-image-restyle-v1.1.0.zip` from the [Releases](https://github.com/OWNER/anime-image-restyle-skill/releases) page and unzip it. The archive contains only the runtime skill files — `SKILL.md`, both READMEs, `LICENSE`, `references/`, and `scripts/probe_image.py` — with no `.github/`, `CHANGELOG.md`, or packaging script.

### Claude Code / Claude family

```bash
# user level (available to all projects)
cp -r anime-image-restyle-skill ~/.claude/skills/anime-image-restyle

# project level (committed with the repo, shared with the team)
mkdir -p .claude/skills && cp -r anime-image-restyle-skill .claude/skills/anime-image-restyle
```

### WorkBuddy / CodeBuddy

```bash
cp -r anime-image-restyle-skill ~/.workbuddy/skills/anime-image-restyle
```

### OpenClaw

```bash
cp -r anime-image-restyle-skill ~/.openclaw/skills/anime-image-restyle
```

### Cursor / environments using `AGENTS.md`

If the target has no skills directory, paste the body of `SKILL.md` into your project's `AGENTS.md` (or system prompt) and keep `references/` reachable at a relative path.

Restart the host or start a new session afterwards so it re-indexes skills.

---

## 3. Repository layout

```
anime-image-restyle-skill/
├── SKILL.md                      # main entry — the AI reads only this file first
├── README.md                     # Chinese docs
├── README_EN.md                  # this file
├── LICENSE                       # MIT
├── CHANGELOG.md
├── .github/
│   └── workflows/release.yml     # builds + uploads the zip on tag push
├── references/
│   ├── style-registry.md         # 9 style families, 87 style keys
│   └── prompt-lexicon.md         # English prompt phrase bank, organized by slot
└── scripts/
    ├── probe_image.py            # stdlib-only image dimension probe
    └── package.py                # packs the runtime files into a distributable zip
```

The split exists to **save tokens**: `SKILL.md` embeds 24 high-frequency colloquial aliases, so a match never touches the registry. Only uncommon styles trigger a read of `style-registry.md`.

---

## 4. How it works

| Step | What happens |
|---|---|
| 1 | Locate the source image (this turn's attachment → absolute path written by the user → most recent image in the session) |
| 2 | Resolve the style (colloquial alias table → nine-family registry → if ambiguous, ask the user to pick a rendering system) |
| 3 | Assemble an **English** prompt from the template, drawing phrases from `prompt-lexicon.md` |
| 4 | Call the image-to-image tool (aspect ratio and fidelity mapped by tier) |
| 5 | Deliver the result + a one-line summary + append a ledger row |

The **default behavior** is *encapsulated style transfer*: only the rendering language changes — linework, color, material, lighting. Identity, facial features, hairstyle silhouette, subject count, pose, expression, camera, composition, spatial layout, key objects, and text placement are all preserved. Content only changes when the user explicitly asks for "recompose / new scene / new outfit / new pose".

---

## 5. Defaults (used when the user says nothing)

| Field | Accepted values | Default |
|---|---|---|
| mode | faithful / standard / recompose | faithful |
| frame | original / 1:1 / 3:4 / 2:3 / 9:16 / 16:9 | original |
| scene | keep background / simplify background / new scene | keep background |
| light | keep lighting / style default / custom | style default |
| intensity | subtle / medium / strong | medium |

Aspect ratio maps to three output sizes only: 1:1 → `1024x1024`, portrait → `1024x1536`, landscape → `1536x1024`. If your target environment supports other sizes, extend the mapping table in section 4 of `SKILL.md`.

---

## 6. Output and ledger

- Results land in `<workspace>/outputs/anime-restyle/<style-key>-<MMDDHHMM>/`
- Falls back to `~/.anime-restyle/outputs/...` when no workspace is available
- Each generation appends a row to `ledger.md` in the output root: `time | source filename | key | intensity/frame | output path`

The package contains **no machine-specific absolute paths** — it runs anywhere as-is.

---

## 7. Style system at a glance

Nine families, 87 keys total:

| Family | Representative keys |
|---|---|
| A Cel shading & eras | `cel-tv-clean`, `cel-90s-film`, `cel-80s-ova`, `cel-00s-vn` |
| B Character design & manga | `shonen-dynamic`, `shoujo-ethereal`, `chibi-2head`, `manga-bw-screentone` |
| C Painterly & illustration | `semi-paint-anime`, `painterly-fantasy`, `anime-watercolor`, `colored-pencil` |
| D Japanese cinematic mood | `sky-luminous-cinema`, `handpainted-nature-fable`, `urban-rain-romance` |
| E East Asian & guofeng | `guofeng-cel`, `gongbi-heavy-color`, `xieyi-ink`, `dunhuang-mural`, `xianxia-ethereal` |
| F Sci-fi, mecha, future | `cyber-rain-neon`, `mecha-hard-surface`, `solarpunk`, `steampunk-brass` |
| G Dark, horror, apocalypse | `gothic-lace`, `yokai-kaidan`, `post-apocalypse`, `urban-noir` |
| H 3D, game, pixel | `anime-3d-cel`, `game-gacha-render`, `pixel-16bit`, `voxel-anime` |
| I Scene & lens modifiers | `portrait-card`, `key-visual`, `vertical-cover`, `sticker-cutout` (stacks onto any main style) |

Saying just "anime style" defaults to `cel-tv-clean`.

---

## 8. Design red lines

- **No living artist names or specific work titles as style anchors.** When the user mentions a person or a work, extract only its visual characteristics, map them to an original descriptive key, and **never claim to reproduce it**. Entries like "Ghibli style" in the alias table are entry points only — the key they resolve to is an original description.
- **Revisions must re-render from the same source image.** Never stack a second conversion on top of an already converted image — artifacts accumulate.
- Only one primary rendering system at a time (cel shading / painterly / watercolor / ink wash / 3D / pixel / B&W manga). If the user requests two conflicting ones, make them choose.

---

## 9. Quick verification

After installing, drop in a photo and say "anime style". You should see:

1. The AI reply "Matched: Modern TV cel shading (`cel-tv-clean`)" plus a one-line keep/change summary;
2. One finished image;
3. A hint that the other eight families are available.

Then try "convert to `cel-90s-film`, 9:16" to verify the aspect-ratio and uncommon-key paths.

---

## 10. Packaging a release

```bash
python scripts/package.py
# -> dist/anime-image-restyle-v1.1.0.zip
```

The script reads the version from the `SKILL.md` frontmatter and includes only runtime files. Pushing a `v*` tag triggers `.github/workflows/release.yml`, which builds the zip and attaches it to the GitHub Release automatically.

---

## 11. Contributing

Issues and PRs are welcome. If you add a style key, please keep it an **original descriptive key** — never a living artist's name or a specific work title — and update both `references/style-registry.md` and, if it is a common colloquial term, the alias table in `SKILL.md`.

---

## 12. License

[MIT](LICENSE). The skill structure and prompt templates may be freely modified and redistributed. All style keys are original descriptive terms and do not reference any specific work or living artist.
