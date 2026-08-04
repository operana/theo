import pygame

from settings import (
    GRAPHICS_PATH,
    PLATFORM_COLOR,
    PLATFORM_BORDER,
    PLATFORM_HIGHLIGHT,
    PLATFORM_SHADOW,
)
from entities.player import Player
from entities.collectible import Collectible
from entities.goal import Goal
from entities.enemy import Enemy


class Level:
    def __init__(self, level_data, save_data=None):
        self.level_data = level_data
        self.name = level_data["name"]
        self.background = pygame.image.load(
            GRAPHICS_PATH / level_data["background"]
        ).convert_alpha()
        self.platforms = [pygame.Rect(*platform) for platform in level_data["platforms"]]
        equipped_hat = save_data.equipped_hat if save_data else "none"
        self.player = Player(level_data["spawn"], equipped_hat=equipped_hat)
        self.collectibles = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.total_bones = len(level_data.get("bones", []))
        self.goal = Goal(level_data["goal"])
        self.complete = False

        for pos in level_data.get("bones", []):
            self.collectibles.add(Collectible(pos))

        self._spawn_enemies()

    def _spawn_enemies(self):
        self.enemies.empty()
        for enemy_data in self.level_data.get("enemies", []):
            self.enemies.add(Enemy(enemy_data["pos"], enemy_data["range"]))

    def _reset_enemies(self):
        for enemy, enemy_data in zip(self.enemies, self.level_data.get("enemies", [])):
            enemy.reset(enemy_data["pos"], enemy_data["range"])

    def update(self, keys):
        if self.complete:
            return

        self.player.handle_input(keys)
        self.player.update(self.platforms)
        self.enemies.update(self.platforms)

        for collectible in pygame.sprite.spritecollide(
            self.player, self.collectibles, dokill=True
        ):
            collectible.on_collect(self.player)

        if pygame.sprite.spritecollide(self.player, self.enemies, dokill=False):
            if self.player.take_damage():
                self._respawn_collectibles()
                if self.player.lives <= 0:
                    self.player.reset_lives()
                    self._reset_enemies()

        if self.goal.is_reached(self.player):
            self.complete = True

    def _respawn_collectibles(self):
        self.collectibles.empty()
        for pos in self.level_data.get("bones", []):
            self.collectibles.add(Collectible(pos))
        self.player.bones_collected = 0

    def draw(self, surface):
        surface.blit(self.background, (0, 0))

        for platform in self.platforms:
            self._draw_platform(surface, platform)

        self.collectibles.draw(surface)
        self.enemies.draw(surface)
        surface.blit(self.goal.image, self.goal.rect)

        if not self.player.is_invincible() or (pygame.time.get_ticks() // 150) % 2 == 0:
            surface.blit(self.player.image, self.player.rect)

    def _draw_platform(self, surface, platform):
        pygame.draw.rect(surface, PLATFORM_SHADOW, platform.move(0, 3), border_radius=3)
        pygame.draw.rect(surface, PLATFORM_COLOR, platform, border_radius=3)
        highlight = pygame.Rect(platform.left + 4, platform.top + 3, platform.width - 8, 5)
        pygame.draw.rect(surface, PLATFORM_HIGHLIGHT, highlight, border_radius=2)
        pygame.draw.rect(surface, PLATFORM_BORDER, platform, 2, border_radius=3)
