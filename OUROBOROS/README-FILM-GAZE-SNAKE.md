# FILM GAZE SNAKE

A playable snake game that teaches Laura Mulvey's gaze theory through film examples.

## Concept

Collect film scene concepts while the snake grows. Each collected item represents a key moment from contemporary cinema that demonstrates Mulvey's theories about the male gaze, counter-gaze, and visual pleasure.

## How to Play

- **Controls**: Arrow keys or WASD to move
- **Pause**: Space or P key
- **Goal**: Collect all 12 film concepts without hitting walls or yourself

## Film Scenes Included

### With YouTube Clips (play automatically when collected):

1. **Blade Runner 2049: K's Opening** (hR8f5vFvX7k)
   - 👁 Active male gaze establishing control
   - Term: `<active male gaze>`

2. **Ex Machina: Ava's Glass Reveals** (D_I-w-lYI84)
   - 🪟 Voyeurism as investigation through glass
   - Term: `<voyeurism as investigation>`

3. **Barbie: Real World Gaze** (lJbW49H29-M)
   - 👀 Oppressive male gaze made visible
   - Term: `<oppressive male gaze>`

### All 12 Concepts:

1. Blade Runner 2049: K's Opening - Active male gaze
2. Blade Runner 2049: Joi & Mariette - Fetishistic scopophilia through AI
3. Ex Machina: Caleb's Arrival - Scopophilia as investigation
4. Ex Machina: Ava's Glass Reveals - Voyeurism as investigation
5. Her: Theodore's Opening - Loneliness and algorithm for desire
6. Her: Physical Proxy Scene - Limits of desire without physical form
7. Alita: Ido Finds Alita - Found object and male creator gaze
8. Alita: Hunter-Warrior Scene - Counter-gaze of female agency
9. Barbie: Opening Parody - Matriarchal world free from male gaze
10. Barbie: Real World Gaze - Oppressive male gaze made visible
11. A.I.: Gigolo Joe - Technologically perfected fetish object
12. A.I.: Dr. Know Scene - Algorithmic authority controlling information

## Visual Design

- **Snake**: Cyan (#0bc) with gradient effect
- **Food Items**: Color-coded by gaze type
  - Red (#ff4d6d) - Male gaze
  - Cyan (#2ce3ff) - Counter-gaze
  - Magenta (#f0f) - Fetishistic scopophilia
  - Blue (#00bfff) - Creator/paternal gaze
  - Yellow (#ffd166) - Algorithmic control

## Features

- **Live Video Overlay**: YouTube clips play semi-transparently over the game for 8 seconds
- **Sidebar Collection**: Track all collected concepts with descriptions
- **Gaze Level**: Increases every 3 concepts collected
- **Score**: 100 points per concept

## Integration

Part of the EOS (Ekphrasis Operating System) suite:
- `/CODEX/codex-uni.html` - Source theory and data
- `/OUROBOROS/film-gaze-snake.html` - This playable snake game
- `/dream-machine.html` - Psychoanalytic agent simulation

## Educational Use

Use this game to:
- Learn Mulvey's gaze theory interactively
- See practical film examples of theoretical concepts
- Understand how contemporary cinema engages with or subverts the male gaze
- Connect film analysis to actual movie scenes

## Technical

- Pure HTML/CSS/JavaScript
- Canvas-based rendering
- YouTube iframe API for video playback
- Responsive design (scales to viewport)
