import pygame

from settings import GRAPHICS_PATH

COLLECTIBLE_DISPLAY_WIDTH = 60


class Collectible(pygame.sprite.Sprite):
    def __init__(self, pos, kind="bone"):
        super().__init__()
        self.kind = kind
        self.value = 1 if kind == "bone" else 5
        self.image = self._load_image(kind)
        self.rect = self.image.get_rect(midbottom=pos)

    def _load_image(self, kind):
        path = GRAPHICS_PATH / "items" / f"{kind}Small.png"
        image = pygame.image.load(path).convert_alpha()
        scale = COLLECTIBLE_DISPLAY_WIDTH / image.get_width()
        size = (COLLECTIBLE_DISPLAY_WIDTH, int(image.get_height() * scale))
        return pygame.transform.scale(image, size)

    def on_collect(self, player):
        player.collect_bone(self.value)
