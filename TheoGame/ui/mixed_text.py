import pygame

from settings import FONT_PATH, UI_FONT_SIZE


def get_pixel_font(size):
    return pygame.font.Font(str(FONT_PATH), size)


def get_ui_font(size=UI_FONT_SIZE):
    return pygame.font.SysFont("arial,helvetica,dejavusans,sans-serif", size)


def render_mixed_parts(parts, pixel_font, ui_font, color):
    surfaces = []
    for text, kind in parts:
        font = pixel_font if kind == "pixel" else ui_font
        antialias = kind == "ui"
        surfaces.append(font.render(text, antialias, color))
    return surfaces


def blit_mixed_line(surface, parts, center, pixel_font, ui_font, color):
    surfaces = render_mixed_parts(parts, pixel_font, ui_font, color)
    total_width = sum(item.get_width() for item in surfaces)
    x = center[0] - total_width // 2
    y_center = center[1]
    for item in surfaces:
        surface.blit(item, (x, y_center - item.get_height() // 2))
        x += item.get_width()


def blit_mixed_line_right(surface, parts, topright, pixel_font, ui_font, color):
    surfaces = render_mixed_parts(parts, pixel_font, ui_font, color)
    total_width = sum(item.get_width() for item in surfaces)
    line_height = max(item.get_height() for item in surfaces)
    x = topright[0] - total_width
    y_center = topright[1] + line_height // 2
    for item in surfaces:
        surface.blit(item, (x, y_center - item.get_height() // 2))
        x += item.get_width()


def mixed_line_size(parts, pixel_font, ui_font):
    surfaces = render_mixed_parts(parts, pixel_font, ui_font, "#FFFFFF")
    width = sum(item.get_width() for item in surfaces)
    height = max(item.get_height() for item in surfaces)
    return width, height
