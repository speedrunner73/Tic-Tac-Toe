import pygame
from constants import *

class Button:
    def __init__(self, rect: pygame.rect.Rect, label: str) -> None:
        self.rect = rect
        self.label = label

    def draw(self, screen: pygame.Surface, font: pygame.font.Font) -> None:
        pygame.draw.rect(screen, BLACK, self.rect, border_radius=8)
        pygame.draw.rect(screen, WHITE, self.rect, 2, border_radius=8)

        text = font.render(self.label, True, WHITE)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

    def is_clicked(self, mouse_pos) -> bool:
        return self.rect.collidepoint(mouse_pos)