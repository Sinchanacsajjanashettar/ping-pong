import pygame
from .paddle import Paddle
from .ball import Ball

WHITE = (255, 255, 255)

class GameEngine:
    def __init__(self, width, height, winning_score=5, use_sounds=True):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        # Sounds
        self.paddle_hit_sound = None
        self.wall_hit_sound = None
        self.score_sound = None

        if use_sounds:
            try:
                pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
                self.paddle_hit_sound = pygame.mixer.Sound("sounds/paddle_hit.wav")
                self.wall_hit_sound = pygame.mixer.Sound("sounds/wall_hit.wav")
                self.score_sound = pygame.mixer.Sound("sounds/score.wav")
                self.paddle_hit_sound.set_volume(1.0)
                self.wall_hit_sound.set_volume(1.0)
                self.score_sound.set_volume(1.0)
            except pygame.error as e:
                print("Warning: Could not load sounds:", e)

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height,
                         paddle_hit_sound=self.paddle_hit_sound,
                         wall_hit_sound=self.wall_hit_sound)

        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.SysFont("Arial", 30)
        self.winning_score = winning_score
        self.game_over = False

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def update(self):
        if self.game_over:
            return

        self.ball.move()
        self.ball.check_collision(self.player, self.ai)
        self.ai.auto_track(self.ball, self.height)

        if self.ball.x <= 0:
            self.ai_score += 1
            if self.score_sound:
                self.score_sound.play()
            self.ball.reset()
        elif self.ball.x >= self.width:
            self.player_score += 1
            if self.score_sound:
                self.score_sound.play()
            self.ball.reset()

        if self.player_score >= self.winning_score:
            self.game_over = True
            self.winner = "Player Wins!"
        elif self.ai_score >= self.winning_score:
            self.game_over = True
            self.winner = "AI Wins!"

    def render(self, screen):
        screen.fill((0,0,0))
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width//4, 20))
        screen.blit(ai_text, (self.width * 3//4, 20))

        if self.game_over:
            overlay = pygame.Surface((self.width, self.height))
            overlay.set_alpha(180)
            overlay.fill((0,0,0))
            screen.blit(overlay, (0,0))

            winner_text = self.font.render(self.winner, True, WHITE)
            screen.blit(winner_text, (self.width//2 - winner_text.get_width()//2, self.height//2 - 30))

            replay_text = self.font.render("Press 3/5/7 for Best of 3/5/7, ESC to Exit", True, WHITE)
            screen.blit(replay_text, (self.width//2 - replay_text.get_width()//2, self.height//2 + 10))

    def reset_game(self, winning_score=None):
        self.player_score = 0
        self.ai_score = 0
        self.ball.reset()
        self.game_over = False
        if winning_score:
            self.winning_score = winning_score
