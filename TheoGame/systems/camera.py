import pygame

from settings import SCREEN_WIDTH


class Camera:
    def __init__(self, level_width):
        self.level_width = level_width
        self.offset = pygame.Vector2(0, 0)

    def update(self, target_rect):
        self.offset.x = target_rect.centerx - SCREEN_WIDTH // 2
        max_offset = max(0, self.level_width - SCREEN_WIDTH)
        self.offset.x = max(0, min(self.offset.x, max_offset))

    def apply(self, rect):
        return rect.move(-self.offset)

    def apply_pos(self, pos):
        return (pos[0] - self.offset.x, pos[1] - self.offset.y)
