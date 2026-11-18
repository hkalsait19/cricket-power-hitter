import json
from pathlib import Path


def load_high_score(path="highscore.json"):
    """Return the saved high score, or zero when no valid save exists."""
    save_path = Path(path)
    try:
        data = json.loads(save_path.read_text(encoding="utf-8"))
        return max(0, int(data.get("high_score", 0)))
    except (FileNotFoundError, json.JSONDecodeError, OSError, TypeError, ValueError):
        return 0


def save_high_score(score, path="highscore.json"):
    """Persist a non-negative high score as JSON."""
    save_path = Path(path)
    save_path.parent.mkdir(parents=True, exist_ok=True)
    save_path.write_text(
        json.dumps({"high_score": max(0, int(score))}, indent=2),
        encoding="utf-8",
    )
