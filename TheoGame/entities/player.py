import pygame

from settings import GRAVITY, JUMP_STRENGTH, PLAYER_SPEED, GRAPHICS_PATH


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.base_image = pygame.image.load(
            GRAPHICS_PATH / "player" / "TheoSpriteSmall.png"
        ).convert_alpha()
        self.image = self.base_image
        self.rect = self.image.get_rect(midbottom=pos)
        self.velocity = pygame.Vector2(0, 0)
        self.on_ground = False
        self.facing = "right"

    def handle_input(self, keys):
        self.velocity.x = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velocity.x = -PLAYER_SPEED
            self.facing = "left"
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocity.x = PLAYER_SPEED
            self.facing = "right"
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground:
            self.velocity.y = JUMP_STRENGTH
            self.on_ground = False

    def apply_gravity(self):
        self.velocity.y += GRAVITY
        if self.velocity.y > 15:
            self.velocity.y = 15

    def update(self, platforms):
        self.apply_gravity()

        self.rect.x += self.velocity.x
        self._resolve_horizontal(platforms)

        self.rect.y += self.velocity.y
        self.on_ground = False
        self._resolve_vertical(platforms)

        self._update_facing()

    def _resolve_horizontal(self, platforms):
        for platform in platforms:
            if self.rect.colliderect(platform):
                if self.velocity.x > 0:
                    self.rect.right = platform.left
                elif self.velocity.x < 0:
                    self.rect.left = platform.right

    def _resolve_vertical(self, platforms):
        for platform in platforms:
            if self.rect.colliderect(platform):
                if self.velocity.y > 0:
                    self.rect.bottom = platform.top
                    self.velocity.y = 0
                    self.on_ground = True
                elif self.velocity.y < 0:
                    self.rect.top = platform.bottom
                    self.velocity.y = 0

    def _update_facing(self):
        if self.facing == "left":
            self.image = pygame.transform.flip(self.base_image, True, False)
        else:
            self.image = self.base_image
