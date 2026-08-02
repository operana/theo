import pygame

from settings import (
    GRAPHICS_PATH,
    PLATFORM_COLOR,
    PLATFORM_BORDER,
    PLATFORM_HIGHLIGHT,
    PLATFORM_SHADOW,
)
from entities.player import Player


class Level:
    def __init__(self, level_data):
        self.name = level_data["name"]
        self.background = pygame.image.load(
            GRAPHICS_PATH / level_data["background"]
        ).convert_alpha()
        self.platforms = [pygame.Rect(*platform) for platform in level_data["platforms"]]
        self.player = Player(level_data["spawn"])

    def update(self, keys):
        self.player.handle_input(keys)
        self.player.update(self.platforms)

    def draw(self, surface):
        surface.blit(self.background, (0, 0))

        for platform in self.platforms:
            self._draw_platform(surface, platform)

        surface.blit(self.player.image, self.player.rect)

    def _draw_platform(self, surface, platform):
        pygame.draw.rect(surface, PLATFORM_SHADOW, platform.move(0, 3), border_radius=3)
        pygame.draw.rect(surface, PLATFORM_COLOR, platform, border_radius=3)
        highlight = pygame.Rect(platform.left + 4, platform.top + 3, platform.width - 8, 5)
        pygame.draw.rect(surface, PLATFORM_HIGHLIGHT, highlight, border_radius=2)
        pygame.draw.rect(surface, PLATFORM_BORDER, platform, 2, border_radius=3)
