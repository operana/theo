import pygame

from data.hats import HATS
from settings import (
    GRAVITY,
    JUMP_STRENGTH,
    PLAYER_SPEED,
    GRAPHICS_PATH,
    PLAYER_HITBOX_HEIGHT,
    PLAYER_HITBOX_WIDTH_RATIO,
    PLAYER_PICKUP_WIDTH,
    PLAYER_PICKUP_HEIGHT,
)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, equipped_hat="none"):
        super().__init__()
        self.base_image = pygame.image.load(
            GRAPHICS_PATH / "player" / "TheoSpriteSmall.png"
        ).convert_alpha()
        self.image = self.base_image
        self.rect = self.image.get_rect(midbottom=pos)
        self.velocity = pygame.Vector2(0, 0)
        self.on_ground = False
        self.facing = "right"
        self.bones_collected = 0
        self.equipped_hat = equipped_hat
        self.spawn_pos = pos
        self.lives = 3
        self.invincible_until = 0

    def collision_rect(self):
        width = max(1, int(self.rect.width * PLAYER_HITBOX_WIDTH_RATIO))
        hitbox = pygame.Rect(0, 0, width, PLAYER_HITBOX_HEIGHT)
        hitbox.midbottom = self.rect.midbottom
        return hitbox

    def pickup_rect(self):
        pickup = pygame.Rect(0, 0, PLAYER_PICKUP_WIDTH, PLAYER_PICKUP_HEIGHT)
        pickup.midbottom = self.rect.midbottom
        return pickup

    def collect_bone(self, value=1):
        self.bones_collected += value

    def is_invincible(self):
        return pygame.time.get_ticks() < self.invincible_until

    def take_damage(self):
        if self.is_invincible():
            return False

        self.lives -= 1
        self.respawn()
        self.invincible_until = pygame.time.get_ticks() + 2000
        return True

    def respawn(self):
        self.rect.midbottom = self.spawn_pos
        self.velocity = pygame.Vector2(0, 0)
        self.on_ground = False

    def reset_lives(self):
        self.lives = 3
        self.invincible_until = 0
        self.respawn()

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

    def update(self, platforms, level_width):
        self.apply_gravity()

        self.rect.x += self.velocity.x
        self._resolve_horizontal(platforms)

        self.rect.y += self.velocity.y
        self.on_ground = False
        self._resolve_vertical(platforms)
        self._clamp_to_level(level_width)

        self._update_facing()

    def _resolve_horizontal(self, platforms):
        hitbox = self.collision_rect()
        for platform in platforms:
            if hitbox.colliderect(platform):
                if self.velocity.x > 0:
                    self.rect.right = platform.left + (self.rect.right - hitbox.right)
                elif self.velocity.x < 0:
                    self.rect.left = platform.right - (hitbox.left - self.rect.left)

    def _resolve_vertical(self, platforms):
        hitbox = self.collision_rect()
        for platform in platforms:
            if hitbox.colliderect(platform):
                if self.velocity.y > 0:
                    self.rect.bottom = platform.top + (self.rect.bottom - hitbox.bottom)
                    self.velocity.y = 0
                    self.on_ground = True
                elif self.velocity.y < 0:
                    self.rect.top = platform.bottom - (hitbox.top - self.rect.top)
                    self.velocity.y = 0

    def _clamp_to_level(self, level_width):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > level_width:
            self.rect.right = level_width

    def _update_facing(self):
        if self.facing == "left":
            base = pygame.transform.flip(self.base_image, True, False)
        else:
            base = self.base_image

        if self.equipped_hat != "none" and self.equipped_hat in HATS:
            self.image = base.copy()
            color = HATS[self.equipped_hat]["color"]
            if color:
                center_x = self.image.get_width() // 2
                pygame.draw.polygon(
                    self.image,
                    color,
                    [
                        (center_x, 2),
                        (center_x - 12, 18),
                        (center_x + 12, 18),
                    ],
                )
        else:
            self.image = base
