import pygame
from constants import *


class Button:

    def __init__(self, rect: pygame.Rect, label: str, accent_color=None):
        self.rect = rect
        self.label = label
        self.hovered = False
        self.accent_color = accent_color

    def draw(self, screen, font):

        mouse_pos = pygame.mouse.get_pos()
        self.hovered = self.rect.collidepoint(mouse_pos)

        # Background
        pygame.draw.rect(screen, PANEL_BG, self.rect, border_radius=8)

        # Border color logic
        border_color = self.accent_color if self.accent_color else PANEL_BORDER

        # Hover effect brightens border
        if self.hovered:
            border_color = tuple(min(255, c + 40) for c in border_color)

        pygame.draw.rect(screen, border_color, self.rect, 2, border_radius=8)

        # Text
        text_surface = font.render(self.label.upper(), True, border_color)
        text_rect = text_surface.get_rect()
        text_rect.center = self.rect.center
        text_rect.y += 2.5  # fine tune vertical alignment

        screen.blit(text_surface, text_rect)

    def is_clicked(self, pos) -> bool:
        return self.rect.collidepoint(pos)