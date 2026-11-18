<<<<<<< HEAD
# cricket-power-hitter
cricket-power-hitter game using python, git, github action, docker, k8s, etc
=======
# Cricket Power Hitter 🏏

A small 2D leather-ball cricket batting arcade game built with Python and Pygame.

## Features

- Six-ball over
- Defensive, ground and lofted shots
- Timing-based batting
- Four and six celebrations
- Runs, wickets and balls scoreboard
- Persistent local high score (`highscore.json`)

## Requirements

- Python 3.10+
- pip
- Pygame 2.6.1

## Run locally (macOS / Linux)

```bash
git clone https://github.com/YOUR_USERNAME/cricket-power-hitter.git
cd cricket-power-hitter

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python main.py
```

## Controls

| Key | Action |
|---|---|
| Enter | Start / next delivery |
| 1 | Defensive shot |
| 2 | Ground shot |
| 3 | Lofted shot |
| Left / Right | Aim shot |
| Space | Swing bat |
| R | Restart after over |
| Esc | Quit |

The ball is delivered automatically. Try to swing when it reaches the batsman.
A shot's result depends on timing, shot selection and a random outcome.

## Tests and lint

```bash
ruff check .
pytest -v
```

The game logic and score storage are tested independently of the graphical window.

## Docker

The Docker image is configured for **headless tests**, not for displaying the Pygame window.

```bash
docker build -t cricket-power-hitter:test .
docker run --rm cricket-power-hitter:test
```

To play the graphical game, run it locally with `python main.py`.

## GitHub Actions

`.github/workflows/ci.yml`:
1. Installs Python dependencies.
2. Runs Ruff.
3. Runs Pytest.
4. On pushes to `main` (and version tags), builds a headless test image and publishes it to GHCR.

The workflow uses the repository-provided `GITHUB_TOKEN`; no personal access token is needed for this package publishing workflow when repository package permissions allow it.

## Release tagging

```bash
git tag v1.0.0
git push origin v1.0.0
```

## Current scope

This is a first playable prototype. It uses simple vector-drawn 2D graphics and simulated shot outcomes. Later releases can add sprite artwork, bowling variations, improved ball physics, sound, multiple wickets and innings.
>>>>>>> 3ba0493 (Initial release - Cricket Power Hitter v1.0)
