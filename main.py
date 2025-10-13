import pygame
from game.game_engine import GameEngine

pygame.init()

WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong - Pygame Version")

clock = pygame.time.Clock()
FPS = 60

engine = GameEngine(WIDTH, HEIGHT, use_sounds=True)

def main():
    running = True
    while running:
        SCREEN.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Replay feature
            if event.type == pygame.KEYDOWN and engine.game_over:
                if event.key == pygame.K_3:
                    engine.reset_game(winning_score=3)
                elif event.key == pygame.K_5:
                    engine.reset_game(winning_score=5)
                elif event.key == pygame.K_7:
                    engine.reset_game(winning_score=7)
                elif event.key == pygame.K_ESCAPE:
                    running = False

        engine.handle_input()
        engine.update()
        engine.render(SCREEN)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
