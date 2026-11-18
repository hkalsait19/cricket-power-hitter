import random
import pygame

from cricket_game.game import CricketGame
from cricket_game.renderer import Renderer
from cricket_game.settings import WIDTH, HEIGHT, FPS, TITLE
from cricket_game.storage import load_high_score, save_high_score


def main():
    pygame.init()
    pygame.display.set_caption(TITLE)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    renderer = Renderer(screen)

    game = CricketGame(load_high_score())
    phase = "ready"
    ball_x, ball_y = 500.0, 250.0
    ball_started = 0
    swing_until = 0
    celebration_started = 0
    shot = "lofted"
    direction = "right"
    running = True

    def update_high_score():
        save_high_score(game.high_score)

    while running:
        now = pygame.time.get_ticks()
        swing = 1.0 if now < swing_until else 0.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                elif phase == "ready" and event.key == pygame.K_RETURN:
                    phase = "delivery"
                    ball_x, ball_y = 500.0, 250.0
                    ball_started = now

                elif phase == "delivery":
                    if event.key == pygame.K_1:
                        shot = "defensive"
                    elif event.key == pygame.K_2:
                        shot = "ground"
                    elif event.key == pygame.K_3:
                        shot = "lofted"
                    elif event.key == pygame.K_LEFT:
                        direction = "left"
                    elif event.key == pygame.K_RIGHT:
                        direction = "right"
                    elif event.key == pygame.K_SPACE and now >= swing_until:
                        swing_until = now + 280
                        timing = max(0.0, min(1.0, 1.0 - abs(now - (ball_started + 1650)) / 1000))  # Increased timing window
                        try:
                            game.play_ball(timing, shot, direction, random.Random())
                        except (ValueError, RuntimeError):
                            pass
                        phase = "result"
                        celebration_started = now
                        update_high_score()

                elif phase == "result" and event.key == pygame.K_RETURN:
                    if game.game_over:
                        phase = "over"
                    else:
                        phase = "delivery"
                        ball_x, ball_y = 500.0, 250.0
                        ball_started = now

                elif phase == "over" and event.key == pygame.K_r:
                    game.reset()
                    shot = "lofted"
                    direction = "right"
                    phase = "ready"

        if phase == "delivery":
            elapsed = now - ball_started
            progress = min(1.0, elapsed / 1800.0)
            ball_x = 500 + (500 - 500) * progress
            ball_y = 250 + 185 * progress
            if progress >= 1.0:
                # An unattended delivery is recorded as a dot ball.
                game.balls += 1
                game.last_result = "DOT BALL – TOO LATE!"
                game.last_boundary = None
                if game.balls >= 6:
                    game.game_over = True
                phase = "result"
                celebration_started = now

        if phase == "result" and now - celebration_started > 1700:
            if game.game_over:
                phase = "over"
            else:
                phase = "delivery"
                ball_x, ball_y = 500.0, 250.0
                ball_started = now

        renderer.draw(
            game, phase, ball_x, ball_y, swing,
            (now - celebration_started) / 1000.0,
        )
        clock.tick(FPS)

    update_high_score()
    pygame.quit()

## updated few controls here:
def load_sounds():
    sounds = {
        "six": pygame.mixer.Sound("sounds/six.wav"),
        "four": pygame.mixer.Sound("sounds/four.wav"),
        "wicket": pygame.mixer.Sound("sounds/wicket.wav"),
        "miss": pygame.mixer.Sound("sounds/miss.wav"),
    }
    return sounds

sounds = load_sounds()

# Play sounds based on the result
if game.last_result == "SIX!":
    sounds["six"].play()
elif game.last_result == "FOUR!":
    sounds["four"].play()
elif "WICKET" in game.last_result:
    sounds["wicket"].play()
elif "MISS" in game.last_result:
    sounds["miss"].play()

if __name__ == "__main__":
    main()
