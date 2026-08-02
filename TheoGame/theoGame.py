# Theo's World — platform adventure

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import pygame
from sys import exit

from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, FONT_PATH
from level import Level, LEVELS
from ui import HUD, LevelCompleteScreen

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Theo's World :)")
clock = pygame.time.Clock()
hint_font = pygame.font.Font(str(FONT_PATH), 20)
title_font = pygame.font.Font(str(FONT_PATH), 48)
hud = HUD(hint_font)
level_complete = LevelCompleteScreen(hint_font, title_font)

level = Level(LEVELS["1-1"])
hint_surface = hint_font.render("← → move   space jump", False, "#FFCCCC")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if level.complete and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            level = Level(LEVELS["1-1"])

    keys = pygame.key.get_pressed()
    level.update(keys)
    level.draw(screen)

    if level.complete:
        level_complete.draw(
            screen,
            level.name,
            level.player.bones_collected,
            level.total_bones,
        )
    else:
        screen.blit(hint_surface, (10, 10))
        hud.draw(screen, level.player.bones_collected, level.total_bones)

    pygame.display.update()
    clock.tick(FPS)
