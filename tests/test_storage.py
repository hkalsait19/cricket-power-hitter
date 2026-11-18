import json

from cricket_game.storage import load_high_score, save_high_score


def test_missing_file_returns_zero(tmp_path):
    assert load_high_score(tmp_path / "missing.json") == 0


def test_save_and_load_high_score(tmp_path):
    path = tmp_path / "scores" / "highscore.json"
    save_high_score(42, path)
    assert load_high_score(path) == 42
    assert json.loads(path.read_text())["high_score"] == 42


def test_invalid_json_returns_zero(tmp_path):
    path = tmp_path / "broken.json"
    path.write_text("{not-json")
    assert load_high_score(path) == 0
