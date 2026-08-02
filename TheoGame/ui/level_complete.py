import pygame

from settings import SCREEN_WIDTH, SCREEN_HEIGHT


class LevelCompleteScreen:
    def __init__(self, font, title_font):
        self.font = font
        self.title_font = title_font

    def draw(self, surface, level_name, bones_collected, total_bones):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((20, 10, 5, 160))
        surface.blit(overlay, (0, 0))

        title = self.title_font.render("Level Complete!", False, "#FFCCCC")
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 120))
        pygame.draw.rect(surface, "#4A2C1A", title_rect.inflate(24, 12), border_radius=6)
        surface.blit(title, title_rect)

        name = self.font.render(level_name, False, "#F2C896")
        name_rect = name.get_rect(center=(SCREEN_WIDTH // 2, 180))
        surface.blit(name, name_rect)

        bones = self.font.render(
            f"Bones: {bones_collected}/{total_bones}",
            False,
            "#FFCCCC",
        )
        bones_rect = bones.get_rect(center=(SCREEN_WIDTH // 2, 230))
        surface.blit(bones, bones_rect)

        hint = self.font.render("Press R to replay", False, "#F2C896")
        hint_rect = hint.get_rect(center=(SCREEN_WIDTH // 2, 300))
        surface.blit(hint, hint_rect)
