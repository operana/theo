import pygame


def _make_goal_surface():
    surface = pygame.Surface((44, 52), pygame.SRCALPHA)
    frame = "#C9A227"
    door = "#F5E6C8"
    handle = "#4A2C1A"

    pygame.draw.rect(surface, frame, (4, 0, 36, 52), border_radius=4)
    pygame.draw.rect(surface, door, (8, 4, 28, 44), border_radius=3)
    pygame.draw.circle(surface, handle, (30, 28), 3)
    pygame.draw.arc(surface, frame, (14, 4, 16, 16), 3.14, 0, 2)
    return surface


class Goal(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = _make_goal_surface()
        self.rect = self.image.get_rect(midbottom=pos)

    def is_reached(self, player):
        return self.rect.colliderect(player.rect)
