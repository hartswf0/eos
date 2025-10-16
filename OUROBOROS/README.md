# Timeline Snake — Narrative Reentry Engine

**TTL: 1** | **Status: Production Ready** | **Platform: Web (Mobile-First)**

## Overview

Timeline Snake is a procedurally-generated documentary narrative game that transforms the classic Snake gameplay into a tool for collecting and sequencing video fragments. Players consume documentary clips that become embedded as living videos in the snake's body, creating a visual timeline that can be exported as structured data.

## Origin

This game was generated from a **LATENT_GENOME** specification using the **INFLATOR_PROMPT** pattern. It represents a new approach to documentary interaction where:

- **Play = Collection**: Movement through space collects narrative fragments
- **Body = Timeline**: The snake's body becomes a living video sequence
- **Death = Export**: Game over triggers timeline export in multiple formats

## Core Mechanics

### Gameplay Loop
1. **Slither**: Navigate the snake using arrow keys/WASD or swipe gestures
2. **Consume**: Collect red fragment squares containing documentary clips
3. **Embody**: Videos embed in snake body segments with visible icons
4. **Sequence**: Build a narrative timeline through collection order
5. **Preview**: Click timeline cards to watch fragments in fullscreen
6. **Export**: On game over, export timeline as OTI JSON + Storymap markdown
7. **Restart**: Begin a new collection with reshuffled fragments

### Risk System
- **Wall Collision**: Hitting boundaries ends collection
- **Self Collision**: Snake eating itself terminates timeline
- **Speed Increase**: Every 3 fragments increases difficulty
- **Fragment Limit**: Maximum 20 videos (all clips collected = victory)

## Documentary Fragments

20 fragments from **"Filter Bubbles: A Documentary Story"** (YouTube ID: BQ2n6SN7gOY):

- **Media Apparatus** (◯, ◡): Opening/closing frames on media systems
- **Core Concepts** (◐, ◒): Individual self and grand narratives
- **Systemic Control** (◓, ◕, ◚, ◠, ◢): Power structures and surveillance
- **Systemic Events** (◔, ◘): Historical turning points
- **Personal Apparatus** (◗): Individual experience
- **Emotional States** (◙): Subjective conditions
- **Systemic Impact** (◛): Consequences of systems
- **Scientific Theory** (◜, ◝): Chaos and complexity frameworks
- **Technological Apparatus** (◞, ◟): Neural networks and algorithms

Each fragment tagged with narrative beat position (opening image, catalyst, midpoint, dark night, resolution, coda, etc.)

## Technical Stack

### Frontend
- **Pure HTML5**: Single-file architecture, no external dependencies
- **Canvas 2D**: Game rendering with 20x20 grid
- **Web Audio API**: Square wave synthesis for turn/collect/death sounds
- **Vibration API**: Haptic feedback patterns
- **YouTube IFrame API**: Embedded video fragments with timecode control

### Export Formats

**OTI (Open Timeline Interchange) v1.0**:
```json
{
  "version": "1.0",
  "title": "Auto-generated from collected titles",
  "source": {"youtube_id": "BQ2n6SN7gOY"},
  "fragments": [...],
  "metadata": {
    "collection_order": [...],
    "score": 15,
    "timestamp": "2025-10-15T..."
  }
}
```

**Storymap Markdown**:
```markdown
# Timeline Title

## Source
YouTube ID: BQ2n6SN7gOY

## Timeline (15 fragments collected)

### opening image — Family of Man Exhibition 1950s
**Icon**: ◯  
**Tag**: Media_Apparatus  
**Time**: 27s - 53s  
**Description**: Opening image establishing media apparatus

---
```

## Mobile Contract

### Touch Controls
- **Swipe Detection**: Minimum 40px distance, direction based on largest delta
- **Audio Unlock**: Tap-to-play gate for mobile browsers
- **Prevent Scroll**: touchmove preventDefault() to avoid page scroll
- **Responsive Scaling**: Canvas and videos scale proportionally

### Performance
- **Max Videos**: 20 iframes (hard limit)
- **Tick Rate**: 200ms base, decreases to 50ms minimum
- **Video Opacity**: 0.7 with screen blend mode
- **Frame Budget**: Stable 60fps with requestAnimationFrame for video positioning

### Autoplay Compliance
- `autoplay=1&mute=1&loop=1&playsinline=1`: iOS/Android compatibility
- `allow="autoplay; encrypted-media"`: iframe permission model
- User interaction gates: Audio context creation on first touch

## Design Philosophy

### Aesthetic
- **Terminal Green** (#00ff41): Primary color, Bauhaus minimalism
- **Pure Black** (#0a0a0a): Background, maximum contrast
- **Pink Accent** (#ff1493): Fragment highlights
- **Yellow Markers** (#ffff00): Video indicators on snake body

### Typography
- **Courier New**: Monospace, uppercase headers
- **Icon Overlay**: Unicode geometric shapes on canvas and body segments

### Layout
- **Desktop (≥768px)**: Game left, timeline sidebar right
- **Mobile (<768px)**: Game top, timeline bottom
- **Modal Preview**: Fullscreen iframe player with metadata

## ES5 Compliance

Built with **strict ES5 JavaScript** for maximum compatibility:
- `var` declarations only (no `let`/`const`)
- Function declarations (no arrow functions)
- String concatenation (no template literals)
- Manual iteration (no array destructuring)
- Compatibility with IE11+ and all mobile browsers

## File Structure

```
OUROBOROS/
├── CONFIG_GENOME.json    # Full game configuration (clips, palette, audio)
├── ENGINE_POML           # Procedural specification (state machine, systems)
├── index.html            # Complete playable game (single file)
└── README.md             # This document
```

## Usage

### Local Play
```bash
open index.html  # macOS
# or
python3 -m http.server 8000
# Navigate to http://localhost:8000
```

### Controls
- **Arrow Keys / WASD**: Directional movement
- **Space / P**: Pause/Resume
- **R / Enter**: Restart (on game over)
- **Touch Swipe**: Mobile directional input
- **Direction Pad**: On-screen buttons

### Export Workflow
1. Play until game over (wall/self collision) or collect all 20 fragments
2. Optionally enter custom title in text input
3. Click "EXPORT TIMELINE" button
4. Download `timeline-snake-export-[timestamp].txt`
5. File contains both OTI JSON and Storymap markdown

## Scoring Rubric (Self-Evaluation)

- **Novelty**: 4/5 — Video-in-snake-body mechanic is fresh
- **Clarity**: 5/5 — Fragment collection goal immediately clear
- **Feel**: 4/5 — Videos integrate smoothly, slight lag with 20+ videos
- **Performance**: 4/5 — Stable FPS on mobile, screen blend mode efficient

**Total: 17/20** ✓ Eligible for child genome generation

## Mutation Rules (TTL Decay)

If spawning a TTL=0 child genome:

### Keep (Core Identity)
- Verbs: slither, consume, embody
- Loop structure: sense → act → score → risk
- Export functionality: OTI + storymap
- Documentary source material

### Vary (Genetic Drift)
- **Visual Motifs**: Try emoji, abstract glyphs, or ASCII art instead of geometric shapes
- **Field Density**: Spawn 2-3 fragments simultaneously instead of 1
- **Body Rules**: Vary video size (50%-150% of tile), opacity (0.5-0.9), blend mode (multiply, overlay)
- **Palette**: High-contrast alternatives (white-on-black, cyan-on-purple, etc.)
- **Grid Size**: 15x15 or 25x25 instead of 20x20

### Temperature
0.5 (moderate variation, maintain recognizability)

## Safety & Privacy

### Content
- Documentary analysis only (no personal data)
- YouTube embeds from single approved video ID
- Kid-safe narrative fragments

### Privacy
- **No localStorage**: In-memory state only
- **No cookies**: Zero tracking or persistence
- **No analytics**: No external service calls
- **No user data**: Export happens client-side only

## License

Generated artifact from POML prompt system. Documentary source: "Filter Bubbles: A Documentary Story" (YouTube). Game mechanics: Public domain Snake variant.

---

**Generated**: 2025-10-15  
**Engine**: Timeline Snake v1.0  
**TTL**: 1 (can spawn 1 child genome)  
**Format**: Single-file HTML5 game  
**Target**: Mobile-first web browsers
