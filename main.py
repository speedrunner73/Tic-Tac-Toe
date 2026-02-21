import pygame
from constants import *
from game import Game


def main() -> None:

    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tic Tac Toe")

    clock = pygame.time.Clock()
    game = Game()

    running = True

    while running:
        clock.tick(60)

        # -------------------------
        # Event Loop
        # -------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                game.handle_event(event)

        # -------------------------
        # Update Logic
        # -------------------------
        game.update()

        # -------------------------
        # Render
        # -------------------------
        screen.fill(BACKGROUND)
        game.render(screen)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()