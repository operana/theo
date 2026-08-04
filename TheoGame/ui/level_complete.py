import pygame

from settings import SCREEN_WIDTH, SCREEN_HEIGHT, UI_FONT_SIZE
from ui.mixed_text import get_pixel_font, get_ui_font, blit_mixed_line


class LevelCompleteScreen:
    def __init__(self, pixel_size=20, title_size=48):
        self.pixel_font = get_pixel_font(pixel_size)
        self.title_font = get_pixel_font(title_size)
        self.ui_font = get_ui_font(UI_FONT_SIZE)

    def draw(self, surface, level_name, bones_collected, total_bones, banked_bones):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((20, 10, 5, 160))
        surface.blit(overlay, (0, 0))

        title = self.title_font.render("Level Complete!", False, "#FFCCCC")
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 110))
        pygame.draw.rect(surface, "#4A2C1A", title_rect.inflate(24, 12), border_radius=6)
        surface.blit(title, title_rect)

        name = self.pixel_font.render(level_name, False, "#F2C896")
        surface.blit(name, name.get_rect(center=(SCREEN_WIDTH // 2, 165)))

        blit_mixed_line(
            surface,
            [
                ("Level bones: ", "pixel"),
                (f"{bones_collected}/{total_bones}", "ui"),
            ],
            (SCREEN_WIDTH // 2, 210),
            self.pixel_font,
            self.ui_font,
            "#FFCCCC",
        )

        blit_mixed_line(
            surface,
            [
                ("Total saved: ", "pixel"),
                (str(banked_bones), "ui"),
                (" bones", "pixel"),
            ],
            (SCREEN_WIDTH // 2, 245),
            self.pixel_font,
            self.ui_font,
            "#F2C896",
        )

        hint = self.pixel_font.render("S shop  |  R replay", False, "#F2C896")
        surface.blit(hint, hint.get_rect(center=(SCREEN_WIDTH // 2, 310)))
