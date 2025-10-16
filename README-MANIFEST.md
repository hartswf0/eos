# EOS HTML MANIFEST

Complete catalog of all HTML files in the EOS repository, organized by category and linked from the main index.

## Access

**Via Index**: Open `index.html` → Click **MANIFEST** tab (default view)

**Standalone JSON**: See `html_manifest.json` for machine-readable version

## Categories

### 1. Core Systems (2 files)
- **index.html** - Main portal and game collection browser
- **dream-machine.html** - Psychoanalytic agent simulation with Mulvey gaze controls

### 2. CODEX (Film Theory) (7 files)
Film gaze theory interfaces implementing Laura Mulvey's "Visual Pleasure and Narrative Cinema"

- **codex_universal.html** - Dynamic loader for JSON + inline codices ⭐ RECOMMENDED
- **codex-uni.html** - Complete Mulvey + Film examples (standalone)
- **codex-plt.html** - Platform codex version
- **codex-please.html** - Experimental variant
- **codex_hypertext.html** - Hypertext navigation version
- **codex_scroll.html** - Scrolling interface
- **codex_viewer.html** - Viewer interface

### 3. OUROBOROS (Snake Games) (3 files)
Educational snake games for exploring film theory and documentary timelines

- **index.html** - Original Curtis documentary timeline snake
- **film-gaze-snake.html** - First Mulvey gaze theory snake (with emojis)
- **gaze-explorer.html** - Video-first exploration interface ⭐ CURRENT

### 4. Ekphrasis Games (POML Generated) (12 files)
Six procedurally-generated games with genetic TTL (Time To Live) decay system

Each game has:
- **Parent (TTL:2)** - Can spawn children, full features
- **Child (TTL:1)** - Simplified rules, archetypal patterns

Games:
1. **Lumen Loom** - Light weaving mechanics
2. **Tide Turner** - Water flow dynamics
3. **Bloom Orbit** - Growth and orbital patterns
4. **Aurora Chimes** - Light and sound harmonics
5. **Sky Lantern Relay** - Aerial navigation
6. **Echo Meadow** - Sound reflection mechanics

## Statistics

- **Total HTML Files**: 24
- **Categories**: 4
- **Core Systems**: 2
- **Theory Interfaces**: 7
- **Snake Games**: 3
- **Procedural Games**: 12

## Usage

All links in the manifest open in new tabs for easy exploration and comparison.

### Navigation Flow

```
index.html (MANIFEST tab)
  ↓
Click any link → Opens in new tab
  ↓
Explore content
  ↓
Return to manifest to navigate elsewhere
```

### For Developers

The manifest is embedded as `HTML_MANIFEST` constant in `index.html` at line ~579.

To add new files:
1. Edit `HTML_MANIFEST` object in `index.html`
2. Update `html_manifest.json` for machine-readable access
3. Update this README

## Integration

The manifest integrates with:
- **index.html** - Main portal (MANIFEST tab)
- **html_manifest.json** - Machine-readable catalog
- **collection_manifest.json** - Game-specific metadata

## File Organization

```
/
├── index.html ..................... Main portal
├── dream-machine.html ............. Psychoanalytic simulation
├── html_manifest.json ............. This catalog (JSON)
├── CODEX/
│   ├── codex_universal.html ....... Universal loader ⭐
│   ├── codex-uni.html ............. Unified codex
│   └── [5 other codex variants]
├── OUROBOROS/
│   ├── index.html ................. Timeline snake
│   ├── film-gaze-snake.html ....... Gaze snake (emojis)
│   └── gaze-explorer.html ......... Gaze explorer ⭐
└── operating-system/games/
    ├── lumen-loom/
    ├── tide-turner/
    ├── bloom-orbit/
    ├── aurora-chimes/
    ├── sky-lantern-relay/
    └── echo-meadow/
```

## Recommended Starting Points

1. **Explore Theory**: `CODEX/codex_universal.html`
2. **Play & Learn**: `OUROBOROS/gaze-explorer.html`
3. **Simulation**: `dream-machine.html`
4. **Game Collection**: `index.html` → LIST tab

---

**Last Updated**: 2025-10-16  
**Maintained By**: EOS System
