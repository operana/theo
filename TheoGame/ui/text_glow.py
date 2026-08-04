GLOW_OFFSETS = [
    (-3, 0), (3, 0), (0, -3), (0, 3),
    (-2, -2), (2, -2), (-2, 2), (2, 2),
    (-1, -1), (1, -1), (-1, 1), (1, 1),
]


def draw_glow_text(surface, text_surface, glow_surface, rect):
    for dx, dy in GLOW_OFFSETS:
        surface.blit(glow_surface, rect.move(dx, dy))
    surface.blit(text_surface, rect)
