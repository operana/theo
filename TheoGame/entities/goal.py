import pygame

from settings import GRAPHICS_PATH

GOAL_DISPLAY_WIDTH = 100


class Goal(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        image = pygame.image.load(
            GRAPHICS_PATH / "items" / "doorSmall.png"
        ).convert_alpha()
        scale = GOAL_DISPLAY_WIDTH / image.get_width()
        size = (GOAL_DISPLAY_WIDTH, int(image.get_height() * scale))
        self.image = pygame.transform.scale(image, size)
        self.rect = self.image.get_rect(midbottom=pos)

    def is_reached(self, player):
        return self.rect.colliderect(player.rect)
