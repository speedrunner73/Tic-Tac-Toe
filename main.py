import pygame
import sys
from constants import WIDTH, HEIGHT, BLACK
from game import Game

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("tic_tac_toe")

clock = pygame.time.Clock()

game = Game()

running = True

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        else:
            game.handle_event(event)

    screen.fill(BLACK)
    game.render(screen)

    pygame.display.update()
