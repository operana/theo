import pygame


def _make_puddle_surface():
    surface = pygame.Surface((44, 22), pygame.SRCALPHA)
    pygame.draw.ellipse(surface, "#3E2723", (0, 4, 44, 18))
    pygame.draw.ellipse(surface, "#5D4037", (4, 6, 36, 12))
    pygame.draw.ellipse(surface, "#8D6E63", (10, 8, 14, 6))
    return surface


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, patrol_range, speed=2):
        super().__init__()
        self.image = _make_puddle_surface()
        self.rect = self.image.get_rect(midbottom=pos)
        self.start_x = self.rect.centerx
        self.patrol_range = patrol_range
        self.direction = 1
        self.speed = speed

    def update(self, platforms):
        self.rect.x += self.speed * self.direction

        if self.rect.centerx > self.start_x + self.patrol_range:
            self.rect.centerx = self.start_x + self.patrol_range
            self.direction = -1
        elif self.rect.centerx < self.start_x - self.patrol_range:
            self.rect.centerx = self.start_x - self.patrol_range
            self.direction = 1

        self._stay_on_platform(platforms)

    def _stay_on_platform(self, platforms):
        for platform in platforms:
            if (
                self.rect.colliderect(platform)
                and self.rect.bottom >= platform.top
                and self.rect.bottom <= platform.top + platform.height
            ):
                self.rect.bottom = platform.top
                return

    def reset(self, pos, patrol_range):
        self.rect.midbottom = pos
        self.start_x = self.rect.centerx
        self.patrol_range = patrol_range
        self.direction = 1
