# Theo's World — platform adventure

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import pygame
from sys import exit

from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, FONT_PATH
from level import Level, LEVELS
from ui import HUD

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Theo's World :)")
clock = pygame.time.Clock()
hint_font = pygame.font.Font(str(FONT_PATH), 20)
hud = HUD(hint_font)

level = Level(LEVELS["1-1"])
hint_surface = hint_font.render("← → move   space jump", False, "#FFCCCC")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    keys = pygame.key.get_pressed()
    level.update(keys)
    level.draw(screen)

    screen.blit(hint_surface, (10, 10))
    hud.draw(screen, level.player.bones_collected, level.total_bones)

    pygame.display.update()
    clock.tick(FPS)
