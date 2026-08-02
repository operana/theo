import pygame

from settings import SCREEN_WIDTH


class HUD:
    def __init__(self, font):
        self.font = font

    def draw(self, surface, bone_count, total_bones):
        score_surface = self.font.render(
            f"Bones: {bone_count}/{total_bones}",
            False,
            "#FFCCCC",
        )
        score_rect = score_surface.get_rect(topright=(SCREEN_WIDTH - 10, 10))
        pygame.draw.rect(
            surface,
            "#4A2C1A",
            score_rect.inflate(16, 8),
            border_radius=4,
        )
        surface.blit(score_surface, score_rect)
