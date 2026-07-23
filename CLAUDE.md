# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A 3D ball-jumping game (球球跳跃) built with Three.js. The ball rolls forward on colored planks, bouncing to a beat-synced audio track. The player moves the ball left/right with mouse/touch to land on matching-color planks. After enough successful jumps, a black hole spawns — reaching it wins the level.

## Commands

```bash
npm install              # Install dependencies (first time only)
npm run dev              # Start Vite dev server on localhost:5173
npm run build            # Build + inline JS into single-file dist/index.html
npm run preview          # Preview the built dist/ output
```

`npm run build` runs `vite build` then `python inline-build.py`, which reads the Vite-generated `<script src="...">` tag from `dist/index.html`, inlines the JS content, removes the `assets/` directory, and moves the script to the end of `<body>`. The result is a self-contained HTML file that works when opened directly or served from any static server.

To test the production build locally: `cd dist && npx serve . -p 8080` (or double-click `dist/start.bat` on Windows).

## Architecture

**The entire game is a single file: [index.html](index.html) (~2500 lines).** It contains all HTML/CSS overlays, the Three.js scene setup, game logic, audio system, particle effects, and UI handling in one `<script type="module">` block. There are no separate JS/TS source files — the source of truth for development is `index.html`. During dev mode (`npm run dev`), Vite serves this HTML directly with HMR. The dev server resolves `import * as THREE from 'three'` from node_modules. The camera is fixed; there are no camera controls.

### Key Systems (all in index.html)

- **Level config** (`levels[]` array, lines 469-475): Each level defines allowed plank types, combo target, base speed (`velZ`), progressive speed growth (`progRate`/`progCap`), and boost mechanics (`boostStep`/`boostCap`).
- **Plank/track system**: 4 plank types — Type 1 (full-width single color), Type 2 (3 colored segments side-by-side), Type 3 (2 segments), Type 4 (white boost plank). Planks scroll toward the player (`plankGroup.position.z += velZ`) and are recycled when behind the camera. `ensureSegments()` generates new planks ahead, optionally synced to beat timings.
- **Audio beat sync** (`initAudio()`, `detectBeats()`): Loads `future_ST.m4a` via XHR (for file:// compatibility), performs onset detection on the waveform (energy differential + adaptive threshold), slices audio around each beat, and plays percussive synth + slice on each bounce.
- **Speed system** (`getEffectiveVelZ()`): Base speed × progressive factor (scales with distance traveled, capped) + accumulated boost (from Type 4 planks, decays over time). The BOOST indicator only activates when `boostAccum > 0.01` (i.e., from Type 4 planks, not from progressive speed).
- **Death/respawn**: Two death modes — color mismatch on Type 2/3 planks (explosion particles) or falling off track edge (fall animation). The first 2 segments are always Type 1 (safe), and `invincibleUntilZ` grants immunity until the 3rd segment. After death, the "Continue" button plays a 10-second video ad (`future_ST.mp4`) before respawning with 2.5s invincibility.
- **Black hole**: Spawns when `comboCount` reaches the level's `comboToWin`. Uses a custom GLSL shader (event horizon, photon ring, accretion disc). Has gravitational pull on the ball; entering it wins the level.
- **Level progression**: Uses `localStorage` key `ball-game-progress` to track `maxUnlockedLevel`. Beating a level unlocks the next. The level select screen shows 5 cards with lock overlays.
- **Mobile adaptations**: `isMobile` flag gates particle counts, geometry segments, shadow maps, and pixel ratio. Touch events (`touchstart`/`touchmove`) control ball position.
- **Controls**: Mouse movement, touch drag, or keyboard ←/→ (A/D) moves the ball; Esc/P toggles pause (`paused`, shows `#pause-overlay`, pauses BGM); M or the `#mute-btn` button toggles mute (persisted in `localStorage` key `ball-game-muted`). All per-frame motion in `animate()` is frame-rate independent via a shared `dt` (seconds) and `dt60` (60fps-equivalent factor).

### Particle/VFX Systems

Each is a `THREE.Points` buffer geometry with manual lifecycle management:

- **Explosion particles** (`explosionCount`): Ball death effect
- **Debris particles** (`debrisMax`): Sparks on plank contact
- **Trail particles** (`trailMax`): Speed trail during boost
- **Boost surge particles** (`bstPartMax`): Ambient particles when boosted
- **Ripple rings** (`ripplePool`): Shader-based expanding rings on bounce
- **Ripple particles** (`rippleParticleMax`): Soft glowing dots accompanying ripples
- **Black hole particles** (`bhParticleCount`): Orbiting accretion particles

All particle counts are halved (roughly 1/3 to 1/2) on mobile.

### Build Output

`dist/` contains:

- `index.html` — Self-contained game (all JS inlined, ~520KB)
- `bgm.mp3` — Background music
- `future_ST.m4a` — Beat analysis audio source
- `future_ST.mp4` — Ad video
- `start.bat` — Windows launcher (runs `npx serve . -p 8080`)

### Key Constraints

- The game must work when opened as a `file://` URL (double-click the HTML file). This is why XHR is used instead of `fetch` for audio loading, and why the build inlines all JS.
- WeChat browser compatibility requires ES2015 target, no WebGL 2-exclusive features, and `failIfMajorPerformanceCaveat: false`.
- `isMobile` must be declared before any code that uses it (notably before `starCount`).
- Plank geometries/materials are shared resources (`plankGeoFull`/`plankGeoT2`/`plankGeoT3`, `plankMatByColor`/`plankMatBoost`, `arrowGeoT2`/`arrowGeoT3`, `arrowMatByColor`). Never dispose them when recycling planks or clearing the track in `restartGame()`/`showLevelSelect()` — only `plankGroup.remove(child)`. Only black hole meshes/materials are disposed there.
- The game does not use TypeScript in practice despite `tsconfig.json` existing — all code is plain JS in `<script type="module">`.

## Git Workflow

**Never `git commit --amend` a commit that has already been pushed or tagged.** `9a42549` is `main`'s baseline on `origin` and is what the `v1.0.0` tag points to. Amending it rewrites that commit into a sibling (same parent, new hash), which makes local `main` diverge from `origin/main` (`ahead 1, behind 1`) and would orphan the tag if force-pushed. This divergence has happened twice on this repo — both times from an accidental amend folding a new edit into the pushed CHANGELOG commit.

Rules:

- To add a new change on top of a pushed/tagged commit, make a **new commit** (`git commit`), never `git commit --amend`.
- Only amend commits that exist **solely locally** and have never been pushed.
- After any classifier "unavailable" error on a mutating git command, do **not** blindly retry — first verify with read-only commands (`git status -sb`, `git log --oneline -3`, `git reflog -5`) whether it already ran. Retries can execute twice.
- Commit each functional change immediately — don't accumulate multiple uncommitted edits.
- After committing, attempt to push. If the network fails (common when reaching GitHub from mainland China — `port 443` timeout / connection reset), tell the user and preserve the local state; never abandon the commit or `--force` your way around it.

Auto-push: a `post-commit` hook (`scripts/auto-push.sh`) automatically pushes after every commit, retrying every 10s until success (never `--force`, only `origin main`). It uses a `.git/auto-push.lock` mkdir lock so concurrent triggers don't duplicate pushes. Note that `.git/hooks/` is not versioned — reinstall the hook after a fresh clone. To disable, delete `.git/hooks/post-commit`.

Recovery if a pushed commit was accidentally amended (local shows `ahead 1, behind 1`):

```bash
git reset --mixed origin/main   # rewind to the pushed baseline; keeps your edit in the working tree
git add <files> && git commit -m "..."   # re-commit the edit as its own commit
git push origin main            # fast-forward, no --force, tag untouched
```

`reset --mixed` is non-destructive (files stay in the working tree). Never `--force` push to fix this — it would rewrite the tagged, deployed history on `origin`.
