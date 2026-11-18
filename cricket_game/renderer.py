import math
import pygame

from .settings import (
    WIDTH, HEIGHT, BACKGROUND, GRASS_DARK, PITCH, WHITE, BLACK, GOLD, RED
)


class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.title_font = pygame.font.SysFont("arial", 38, bold=True)
        self.big_font = pygame.font.SysFont("arial", 54, bold=True)
        self.font = pygame.font.SysFont("arial", 24, bold=True)
        self.small_font = pygame.font.SysFont("arial", 17)

    def text(self, message, font, color, center):
        surface = font.render(str(message), True, color)
        self.screen.blit(surface, surface.get_rect(center=center))

    def draw(self, game, phase, ball_x, ball_y, swing, celebration_time):
        self.screen.fill(BACKGROUND)

        # Outfield stripes and boundary.
        for y in range(210, HEIGHT, 65):
            pygame.draw.rect(self.screen, GRASS_DARK, (0, y, WIDTH, 32))
        pygame.draw.rect(self.screen, WHITE, (28, 195, WIDTH - 56, HEIGHT - 225), 3)

        # Pitch.
        pygame.draw.rect(self.screen, PITCH, (365, 240, 270, 310), border_radius=12)
        pygame.draw.rect(self.screen, WHITE, (365, 240, 270, 310), 2)

        # Creases and wickets.
        for x in (425, 575):
            pygame.draw.line(self.screen, WHITE, (x - 35, 485), (x + 35, 485), 4)
            for dx in (-12, 0, 12):
                pygame.draw.line(self.screen, WHITE, (x + dx, 466), (x + dx, 485), 5)

        # Bowler.
        pygame.draw.circle(self.screen, (232, 184, 145), (500, 285), 13)
        pygame.draw.line(self.screen, (30, 55, 140), (500, 300), (500, 350), 13)
        pygame.draw.line(self.screen, BLACK, (500, 345), (480, 375), 7)
        pygame.draw.line(self.screen, BLACK, (500, 345), (520, 375), 7)

        # Batsman.
        pygame.draw.circle(self.screen, (232, 184, 145), (500, 430), 15)
        pygame.draw.line(self.screen, (30, 65, 160), (500, 446), (500, 492), 17)
        pygame.draw.line(self.screen, BLACK, (495, 490), (482, 525), 8)
        pygame.draw.line(self.screen, BLACK, (505, 490), (518, 525), 8)
        pygame.draw.line(self.screen, (232, 184, 145), (490, 452), (470, 470), 7)

        # Bat swings during contact.
        angle = (-0.8 + swing * 1.8) if swing > 0 else -0.45
        bat_end = (int(510 + math.cos(angle) * 65), int(460 - math.sin(angle) * 65))
        pygame.draw.line(self.screen, (222, 190, 125), (510, 460), bat_end, 12)
        pygame.draw.line(self.screen, WHITE, (bat_end[0] - 5, bat_end[1]), (bat_end[0] + 5, bat_end[1]), 3)

        # Ball.
        if phase == "delivery":
            pygame.draw.circle(self.screen, RED, (int(ball_x), int(ball_y)), 9)
            pygame.draw.arc(self.screen, WHITE, (ball_x - 6, ball_y - 6, 12, 12), 0.3, 2.5, 2)

        # Scoreboard.
        pygame.draw.rect(self.screen, (15, 35, 30), (20, 18, WIDTH - 40, 145), border_radius=14)
        pygame.draw.rect(self.screen, GOLD, (20, 18, WIDTH - 40, 145), 2, border_radius=14)
        self.text("CRICKET POWER HITTER", self.title_font, GOLD, (WIDTH // 2, 48))
        self.text(f"SCORE  {game.runs}/{game.wickets}", self.font, WHITE, (190, 105))
        self.text(f"BALLS  {game.balls}/6", self.font, WHITE, (480, 105))
        self.text(f"HIGH SCORE  {game.high_score}", self.font, GOLD, (790, 105))

        if phase == "ready":
            self.text("PRESS ENTER TO START", self.font, WHITE, (WIDTH // 2, 590))
        elif phase == "delivery":
            self.text("SPACE: SWING   1: DEFEND   2: GROUND   3: LOFT", self.small_font, WHITE, (WIDTH // 2, 590))
            self.text("← / → AIM", self.small_font, WHITE, (WIDTH // 2, 615))
        elif phase == "result":
            if game.last_boundary in (4, 6):
                label = "FOUR!" if game.last_boundary == 4 else "SIX!"
                pulse = 1.0 + 0.08 * math.sin(celebration_time * 12)
                font = pygame.font.SysFont("arial", int(68 * pulse), bold=True)
                self.text(label, font, GOLD, (WIDTH // 2, 335))
            else:
                self.text(game.last_result, self.big_font, WHITE, (WIDTH // 2, 340))
            self.text("Press ENTER for next ball", self.font, WHITE, (WIDTH // 2, 590))
        elif phase == "over":
            self.text("OVER COMPLETE!", self.big_font, GOLD, (WIDTH // 2, 330))
            self.text(f"FINAL SCORE: {game.score_text}", self.font, WHITE, (WIDTH // 2, 395))
            self.text("Press R to play again  |  ESC to quit", self.font, WHITE, (WIDTH // 2, 590))

        pygame.display.flip()
