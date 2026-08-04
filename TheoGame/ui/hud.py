import pygame

from settings import SCREEN_WIDTH, UI_FONT_SIZE
from ui.mixed_text import get_pixel_font, get_ui_font, blit_mixed_line_right, mixed_line_size


class HUD:
    def __init__(self, pixel_size=20):
        self.pixel_font = get_pixel_font(pixel_size)
        self.ui_font = get_ui_font(UI_FONT_SIZE)

    def draw(self, surface, bone_count, total_bones, banked_bones=0, lives=3):
        parts = [
            ("Bones: ", "pixel"),
            (f"{bone_count}/{total_bones}", "ui"),
            ("  Bank: ", "pixel"),
            (str(banked_bones), "ui"),
            ("  Lives: ", "pixel"),
            (str(lives), "ui"),
        ]
        width, height = mixed_line_size(parts, self.pixel_font, self.ui_font)
        box = pygame.Rect(0, 0, width + 16, height + 8)
        box.topright = (SCREEN_WIDTH - 10, 10)
        pygame.draw.rect(surface, "#4A2C1A", box, border_radius=4)
        blit_mixed_line_right(
            surface,
            parts,
            (box.right - 8, box.centery - height // 2),
            self.pixel_font,
            self.ui_font,
            "#FFCCCC",
        )
