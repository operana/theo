# TEMPORARY birthday feature — delete with the birthday_surprise/ folder.

import random

import pygame

from settings import SCREEN_WIDTH, GRAPHICS_PATH, GRAVITY
from birthday_surprise.sounds import play, play_chomp
from birthday_surprise.theo_animations import ChompAnimation

PICKUP_DISPLAY_WIDTH = 40

THEO_MAX_HP = 100
ENEMY_MAX_HP = 300
BASE_CHOMP_DAMAGE = 12
POWER_CHOMP_DAMAGE = 26
ENEMY_CONTACT_DAMAGE = 18
UBE_HEAL = 22
CHOMP_COOLDOWN_MS = 450
CHOMP_IMPACT_RANGE = 108
POWERUP_DURATION_MS = 12000
POWER_BAR_WIDTH = 130
POWER_BAR_HEIGHT = 10
INVINCIBLE_MS = 900

UBE_SPAWN_MIN_MS = 3500
UBE_SPAWN_MAX_MS = 6500
BOBA_SPAWN_MIN_MS = 7000
BOBA_SPAWN_MAX_MS = 11000
POPUP_LIFETIME_MS = 900

_popup_font = None


def _get_popup_font():
    global _popup_font
    if _popup_font is None:
        from ui.mixed_text import get_pixel_font
        _popup_font = get_pixel_font(22)
    return _popup_font


class FloatingPopup:
    def __init__(self, text, world_pos, color):
        self.text = text
        self.x, self.y = world_pos
        self.color = color
        self.started_at = pygame.time.get_ticks()
        self.surface = _get_popup_font().render(text, False, color)

    def update(self):
        return pygame.time.get_ticks() - self.started_at < POPUP_LIFETIME_MS

    def draw(self, surface, camera):
        elapsed = pygame.time.get_ticks() - self.started_at
        if elapsed >= POPUP_LIFETIME_MS:
            return

        progress = elapsed / POPUP_LIFETIME_MS
        y = self.y - progress * 42
        alpha = int(255 * (1 - progress))
        pos = camera.apply_pos((self.x - self.surface.get_width() // 2, y))

        faded = self.surface.copy()
        faded.set_alpha(alpha)
        surface.blit(faded, pos)


def draw_health_bar(surface, anchor_rect, hp, max_hp, offset_y=-8, bar_height=7):
    bar_width = max(44, anchor_rect.width)
    x = anchor_rect.centerx - bar_width // 2
    y = anchor_rect.top + offset_y - bar_height

    back = pygame.Rect(x, y, bar_width, bar_height)
    pygame.draw.rect(surface, "#2E1A0E", back, border_radius=3)
    pygame.draw.rect(surface, "#4A2C1A", back, 1, border_radius=3)

    if max_hp > 0 and hp > 0:
        fill_width = int(bar_width * hp / max_hp)
        fill = pygame.Rect(x, y, fill_width, bar_height)
        color = "#7BC96F" if hp / max_hp > 0.35 else "#FF6666"
        pygame.draw.rect(surface, color, fill, border_radius=3)


def _load_item_image(filename):
    image = pygame.image.load(GRAPHICS_PATH / "items" / filename).convert_alpha()
    scale = PICKUP_DISPLAY_WIDTH / image.get_width()
    size = (PICKUP_DISPLAY_WIDTH, int(image.get_height() * scale))
    return pygame.transform.scale(image, size)


def _make_guard_surface():
    surface = pygame.Surface((120, 68), pygame.SRCALPHA)
    pygame.draw.ellipse(surface, "#3E2723", (0, 10, 120, 54))
    pygame.draw.ellipse(surface, "#6D4C41", (10, 18, 100, 36))
    pygame.draw.ellipse(surface, "#A1887F", (34, 28, 38, 14))
    pygame.draw.ellipse(surface, "#FF6666", (78, 24, 14, 14))
    pygame.draw.ellipse(surface, "#FF6666", (26, 24, 14, 14))
    pygame.draw.ellipse(surface, "#2E1A0E", (80, 28, 6, 6))
    pygame.draw.ellipse(surface, "#2E1A0E", (28, 28, 6, 6))
    return surface


class HallwayGuard:
    def __init__(self, pos):
        self.spawn_pos = pos
        self.image = _make_guard_surface()
        self.rect = self.image.get_rect(midbottom=pos)
        self.start_x = self.rect.centerx
        self.patrol_range = 130
        self.direction = 1
        self.speed = 2.5
        self.max_hp = ENEMY_MAX_HP
        self.hp = ENEMY_MAX_HP
        self.alive = True
        self.hit_flash_until = 0

    def reset(self):
        self.rect.midbottom = self.spawn_pos
        self.start_x = self.rect.centerx
        self.hp = self.max_hp
        self.alive = True
        self.direction = 1
        self.hit_flash_until = 0

    def update(self, platforms):
        if not self.alive:
            return

        self.rect.x += self.speed * self.direction
        if self.rect.centerx > self.start_x + self.patrol_range:
            self.rect.centerx = self.start_x + self.patrol_range
            self.direction = -1
        elif self.rect.centerx < self.start_x - self.patrol_range:
            self.rect.centerx = self.start_x - self.patrol_range
            self.direction = 1

        for platform in platforms:
            if (
                self.rect.colliderect(platform)
                and self.rect.bottom >= platform.top
                and self.rect.bottom <= platform.top + platform.height
            ):
                self.rect.bottom = platform.top
                return

    def take_damage(self, amount):
        if not self.alive:
            return False

        self.hp = max(0, self.hp - amount)
        self.hit_flash_until = pygame.time.get_ticks() + 120
        play("damage")
        if self.hp <= 0:
            self.alive = False
            play("defeat")
        return True

    def draw(self, surface, camera_rect):
        if not self.alive:
            return

        pos = camera_rect
        if pygame.time.get_ticks() < self.hit_flash_until:
            tinted = self.image.copy()
            tinted.fill((255, 180, 180, 0), special_flags=pygame.BLEND_RGBA_ADD)
            surface.blit(tinted, pos)
        else:
            surface.blit(self.image, pos)

        draw_health_bar(
            surface, camera_rect, self.hp, self.max_hp, offset_y=-14, bar_height=10
        )


class FallingUbe:
    def __init__(self, x):
        self.image = _load_item_image("ubeSmall.png")
        self.rect = self.image.get_rect(midtop=(x, -20))
        self.velocity_y = 2
        self.active = True
        self.on_ground = False
        self.despawn_at = 0

    def update(self, floor_y):
        if not self.active:
            return

        if not self.on_ground:
            self.velocity_y += GRAVITY * 0.5
            self.velocity_y = min(self.velocity_y, 8)
            self.rect.y += int(self.velocity_y)

            if self.rect.bottom >= floor_y:
                self.rect.bottom = floor_y
                self.on_ground = True
                self.despawn_at = pygame.time.get_ticks() + 4000
        elif pygame.time.get_ticks() >= self.despawn_at:
            self.active = False

    def collect(self, player):
        if not self.active:
            return False
        if player.pickup_rect().colliderect(self.rect):
            self.active = False
            return True
        return False

    def draw(self, surface, camera_rect):
        if self.active:
            surface.blit(self.image, camera_rect)


class CatapultBoba:
    def __init__(self, y, direction, spawn_x):
        self.image = _load_item_image("bobaSmall.png")
        self.direction = direction
        self.rect = self.image.get_rect(center=(spawn_x, y))
        self.speed = 6 * direction
        self.active = True

    def update(self, level_width):
        if not self.active:
            return

        self.rect.x += self.speed
        if self.rect.right < -40 or self.rect.left > level_width + 40:
            self.active = False

    def collect(self, player):
        if not self.active:
            return False
        if player.pickup_rect().colliderect(self.rect):
            self.active = False
            return True
        return False

    def draw(self, surface, camera_rect):
        if self.active:
            surface.blit(self.image, camera_rect)


class HallwayCombat:
    def __init__(self, player, platforms, level_width, enemy_pos):
        self.player = player
        self.platforms = platforms
        self.level_width = level_width
        self.enemy = HallwayGuard(enemy_pos)

        self.theo_max_hp = THEO_MAX_HP
        self.theo_hp = THEO_MAX_HP
        self.invincible_until = 0
        self.powered_until = 0
        self.powered_started_at = 0

        self.chomp_cooldown_until = 0
        self.chomp_hit_this_swing = False
        self.chomp_anim = ChompAnimation()

        self.ubes = []
        self.bobas = []
        self.next_ube_at = pygame.time.get_ticks() + random.randint(
            UBE_SPAWN_MIN_MS, UBE_SPAWN_MAX_MS
        )
        self.next_boba_at = pygame.time.get_ticks() + random.randint(
            BOBA_SPAWN_MIN_MS, BOBA_SPAWN_MAX_MS
        )

        self.door_unlocked = False
        self.respawn_pos = player.spawn_pos
        self.popups = []

    @property
    def enemy_defeated(self):
        return not self.enemy.alive

    def is_powered(self):
        return pygame.time.get_ticks() < self.powered_until

    def chomp_damage(self):
        return POWER_CHOMP_DAMAGE if self.is_powered() else BASE_CHOMP_DAMAGE

    def try_chomp(self):
        now = pygame.time.get_ticks()
        if now < self.chomp_cooldown_until or not self.enemy.alive or self.chomp_anim.is_active():
            return

        self.chomp_cooldown_until = now + CHOMP_COOLDOWN_MS
        self.chomp_hit_this_swing = False
        self.chomp_anim.start(self.player)
        play_chomp(self.is_powered())

    def chomp_rect(self):
        body = self.player.rect
        reach = CHOMP_IMPACT_RANGE
        if self.player.facing == "right":
            return pygame.Rect(body.right - 10, body.top, reach, body.height)
        return pygame.Rect(body.left - reach + 10, body.top, reach, body.height)

    def is_chomping(self):
        return self.chomp_anim.is_active()

    def update(self, camera):
        now = pygame.time.get_ticks()

        self.chomp_anim.update(self.player, powered=self.is_powered())
        self.enemy.update(self.platforms)

        chomp_connected = False
        if self.chomp_anim.is_attack_frame() and not self.chomp_hit_this_swing:
            if self.chomp_rect().colliderect(self.enemy.rect):
                if self.enemy.take_damage(self.chomp_damage()):
                    self.chomp_hit_this_swing = True
                    chomp_connected = True

        if self.enemy.alive and now >= self.invincible_until and not chomp_connected:
            if self.player.collision_rect().colliderect(self.enemy.rect):
                self._damage_theo(ENEMY_CONTACT_DAMAGE)

        for ube in self.ubes:
            ube.update(self.platforms[0].top)
            if ube.collect(self.player):
                self.theo_hp = min(self.theo_max_hp, self.theo_hp + UBE_HEAL)
                play("heal")
                self._spawn_popup("+HP", "#7BC96F")

        for boba in self.bobas:
            boba.update(self.level_width)
            if boba.collect(self.player):
                self.powered_started_at = now
                self.powered_until = now + POWERUP_DURATION_MS
                play("powerup")
                self._spawn_popup("+DAMAGE", "#FFD700")

        self.ubes = [item for item in self.ubes if item.active]
        self.bobas = [item for item in self.bobas if item.active]
        self.popups = [popup for popup in self.popups if popup.update()]

        if now >= self.next_ube_at:
            spawn_x = random.randint(
                int(camera.offset.x) + 80,
                int(camera.offset.x) + 720,
            )
            spawn_x = max(60, min(spawn_x, self.level_width - 60))
            self.ubes.append(FallingUbe(spawn_x))
            self.next_ube_at = now + random.randint(UBE_SPAWN_MIN_MS, UBE_SPAWN_MAX_MS)

        if now >= self.next_boba_at:
            direction = random.choice([-1, 1])
            y = random.randint(170, 260)
            if direction > 0:
                spawn_x = int(camera.offset.x) - 30
            else:
                spawn_x = int(camera.offset.x) + SCREEN_WIDTH + 30
            self.bobas.append(CatapultBoba(y, direction, spawn_x))
            self.next_boba_at = now + random.randint(BOBA_SPAWN_MIN_MS, BOBA_SPAWN_MAX_MS)

        if self.enemy_defeated:
            self.door_unlocked = True

        if self.theo_hp <= 0:
            self._respawn_theo()

    def _damage_theo(self, amount):
        self.theo_hp = max(0, self.theo_hp - amount)
        now = pygame.time.get_ticks()
        self.invincible_until = now + INVINCIBLE_MS
        self.player.invincible_until = now + INVINCIBLE_MS
        play("whimper")

    def _spawn_popup(self, text, color):
        anchor = (
            self.player.rect.centerx,
            self.player.rect.top - 8,
        )
        self.popups.append(FloatingPopup(text, anchor, color))

    def _respawn_theo(self):
        self.theo_hp = self.theo_max_hp
        self.player.respawn()
        self.enemy.reset()
        self.door_unlocked = False
        self.chomp_anim = ChompAnimation()
        now = pygame.time.get_ticks()
        self.invincible_until = now + 1500
        self.player.invincible_until = now + 1500

    def draw(self, surface, camera):
        for ube in self.ubes:
            ube.draw(surface, camera.apply(ube.rect))

        for boba in self.bobas:
            boba.draw(surface, camera.apply(boba.rect))

        if self.enemy.alive:
            self.enemy.draw(surface, camera.apply(self.enemy.rect))

        player_rect = camera.apply(self.player.rect)
        if self.theo_hp > 0:
            draw_health_bar(surface, player_rect, self.theo_hp, self.theo_max_hp, offset_y=-14)

        for popup in self.popups:
            popup.draw(surface, camera)

    def draw_overlays(self, surface, hint_font):
        if self.is_powered():
            remaining_ms = max(0, self.powered_until - pygame.time.get_ticks())
            fill_ratio = remaining_ms / POWERUP_DURATION_MS
            label = hint_font.render("BOBA POWER", False, "#FFD700")
            surface.blit(label, (10, 28))

            bar_x = 10
            bar_y = 50
            back = pygame.Rect(bar_x, bar_y, POWER_BAR_WIDTH, POWER_BAR_HEIGHT)
            pygame.draw.rect(surface, "#2E1A0E", back, border_radius=4)
            pygame.draw.rect(surface, "#4A2C1A", back, 1, border_radius=4)

            fill_width = max(0, int(POWER_BAR_WIDTH * fill_ratio))
            if fill_width > 0:
                fill = pygame.Rect(bar_x, bar_y, fill_width, POWER_BAR_HEIGHT)
                pygame.draw.rect(surface, "#FFD700", fill, border_radius=4)
                highlight = pygame.Rect(bar_x + 2, bar_y + 2, max(0, fill_width - 4), 3)
                pygame.draw.rect(surface, "#FFF2AA", highlight, border_radius=2)

        door_hint_y = 68 if self.is_powered() else 56
        if not self.door_unlocked:
            label = hint_font.render("Defeat the enemy to unlock the door", False, "#FFCCCC")
            surface.blit(label, (10, door_hint_y))
