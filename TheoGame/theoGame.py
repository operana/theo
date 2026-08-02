# Theo's World — platform adventure (step 1: player + platforms + gravity)

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import pygame
from sys import exit

from settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FPS,
    GRAPHICS_PATH,
    FONT_PATH,
    PLATFORM_COLOR,
    PLATFORM_BORDER,
    PLATFORM_HIGHLIGHT,
    PLATFORM_SHADOW,
)
from entities.player import Player


def draw_platform(surface, platform):
    pygame.draw.rect(surface, PLATFORM_SHADOW, platform.move(0, 3), border_radius=3)
    pygame.draw.rect(surface, PLATFORM_COLOR, platform, border_radius=3)
    highlight = pygame.Rect(platform.left + 4, platform.top + 3, platform.width - 8, 5)
    pygame.draw.rect(surface, PLATFORM_HIGHLIGHT, highlight, border_radius=2)
    pygame.draw.rect(surface, PLATFORM_BORDER, platform, 2, border_radius=3)

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Theo's World :)")
clock = pygame.time.Clock()
hint_font = pygame.font.Font(str(FONT_PATH), 20)

background = pygame.image.load(
    GRAPHICS_PATH / "backgrounds" / "cafe.png"
).convert_alpha()

platforms = [
    pygame.Rect(0, 350, 800, 50),
    pygame.Rect(150, 280, 120, 20),
    pygame.Rect(400, 220, 120, 20),
    pygame.Rect(600, 280, 120, 20),
]

theo = Player((100, 350))
hint_surface = hint_font.render("← → move   space jump", False, "#FFCCCC")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    keys = pygame.key.get_pressed()
    theo.handle_input(keys)
    theo.update(platforms)

    screen.blit(background, (0, 0))

    for platform in platforms:
        draw_platform(screen, platform)

    screen.blit(theo.image, theo.rect)
    screen.blit(hint_surface, (10, 10))

    pygame.display.update()
    clock.tick(FPS)
