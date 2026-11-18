import random
import pytest

from cricket_game.game import CricketGame


def test_initial_scoreboard():
    game = CricketGame(high_score=12)
    assert game.score_text == "0/0"
    assert game.balls_remaining == 6
    assert game.high_score == 12


def test_lofted_six_on_perfect_timing():
    game = CricketGame()
    result = game.play_ball(0.5, "lofted", rng=random.Random(1))
    assert result["runs"] == 6
    assert result["result"] == "SIX!"
    assert game.runs == 6
    assert game.last_boundary == 6


def test_defensive_shot_is_safe_dot_with_controlled_rng():
    game = CricketGame()
    result = game.play_ball(0.5, "defensive", rng=random.Random(1))
    assert result["runs"] in (0, 1)
    assert game.balls == 1


def test_bad_timing_can_produce_wicket():
    game = CricketGame()
    result = game.play_ball(0.0, "lofted", rng=random.Random(1))
    assert result["wicket"] is True
    assert game.wickets == 1
    assert game.game_over is True


def test_invalid_timing_rejected():
    game = CricketGame()
    with pytest.raises(ValueError):
        game.play_ball(1.5)


def test_invalid_shot_rejected():
    game = CricketGame()
    with pytest.raises(ValueError):
        game.play_ball(0.5, "helicopter")


def test_six_balls_complete_over():
    game = CricketGame()
    rng = random.Random(10)
    for _ in range(6):
        if game.game_over:
            break
        game.play_ball(0.5, "defensive", rng=rng)
    assert game.balls == 6
    assert game.game_over is True


def test_cannot_play_after_game_over():
    game = CricketGame()
    game.game_over = True
    with pytest.raises(RuntimeError):
        game.play_ball(0.5)


def test_direction_validation():
    game = CricketGame()
    with pytest.raises(ValueError):
        game.play_ball(0.5, direction="middle")
