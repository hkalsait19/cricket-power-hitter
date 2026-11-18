import random

from .settings import BALLS_PER_OVER


class CricketGame:
    """Small, graphics-independent six-ball batting game."""

    SHOTS = {"1": "defensive", "2": "ground", "3": "lofted"}

    def __init__(self, high_score=0):
        self.high_score = max(0, int(high_score))
        self.reset()

    def reset(self):
        self.runs = 0
        self.wickets = 0
        self.balls = 0
        self.last_result = "Press ENTER to start your over"
        self.game_over = False
        self.started = False
        self.last_boundary = None
        self.last_shot = "ground"

    @property
    def balls_remaining(self):
        return max(0, BALLS_PER_OVER - self.balls)

    @property
    def score_text(self):
        return f"{self.runs}/{self.wickets}"

    def play_ball(self, timing, shot="lofted", direction="right", rng=None):
        """
        Resolve one delivery.

        timing: 0..1, with 0.5 being ideal contact.
        shot: defensive, ground, or lofted.
        direction: left or right.
        rng: optional random.Random instance for deterministic tests.
        """
        if self.game_over:
            raise RuntimeError("The over is complete. Press R to play again.")
        if not 0.0 <= timing <= 1.0:
            raise ValueError("Timing must be between 0.0 and 1.0.")
        if shot not in {"defensive", "ground", "lofted"}:
            raise ValueError("Unknown shot type.")
        if direction not in {"left", "right"}:
            raise ValueError("Direction must be left or right.")

        rng = rng or random.Random()
        self.started = True
        self.last_shot = shot
        self.balls += 1
        self.last_boundary = None

        accuracy = 1.0 - abs(timing - 0.5) * 2.0
        roll = rng.random()

        # Poor contact can result in a miss or a wicket.
        if accuracy < 0.22:
            if roll < 0.48:
                result, runs = "WICKET!", 0
                self.wickets += 1
            else:
                result, runs = "DOT BALL", 0
        elif shot == "defensive":
            if accuracy > 0.78 and roll < 0.35:
                result, runs = "1 RUN", 1
            else:
                result, runs = "DEFENDED – DOT BALL", 0
        elif shot == "ground":
            if accuracy > 0.82 and roll < 0.28:
                result, runs = "FOUR!", 4
                self.last_boundary = 4
            elif roll < 0.62:
                result, runs = "2 RUNS", 2
            elif roll < 0.88:
                result, runs = "1 RUN", 1
            else:
                result, runs = "DOT BALL", 0
        else:  # lofted
            if accuracy > 0.82 and roll < 0.48:
                result, runs = "SIX!", 6
                self.last_boundary = 6
            elif accuracy > 0.58 and roll < 0.70:
                result, runs = "FOUR!", 4
                self.last_boundary = 4
            elif roll < 0.83:
                result, runs = "2 RUNS", 2
            elif roll < 0.94:
                result, runs = "1 RUN", 1
            elif roll < 0.98:
                result, runs = "DOT BALL", 0
            else:
                result, runs = "WICKET!", 0
                self.wickets += 1

        self.runs += runs
        self.last_result = result
        self.high_score = max(self.high_score, self.runs)

        if self.balls >= BALLS_PER_OVER or self.wickets >= 1:
            self.game_over = True

        return {"result": result, "runs": runs, "wicket": result == "WICKET!"}
