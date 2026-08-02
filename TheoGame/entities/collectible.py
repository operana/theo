import pygame

from settings import GRAPHICS_PATH


class Collectible(pygame.sprite.Sprite):
    def __init__(self, pos, kind="bone"):
        super().__init__()
        self.kind = kind
        self.value = 1 if kind == "bone" else 5
        self.image = self._load_image(kind)
        self.rect = self.image.get_rect(midbottom=pos)

    def _load_image(self, kind):
        path = GRAPHICS_PATH / "items" / f"{kind}Small.png"
        return pygame.image.load(path).convert_alpha()

    def on_collect(self, player):
        player.collect_bone(self.value)
