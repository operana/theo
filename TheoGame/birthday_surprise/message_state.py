# TEMPORARY birthday feature — delete with the birthday_surprise/ folder.

import random

import pygame

from settings import (
    FONT_PATH,
    GRAPHICS_PATH,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    PLATFORM_COLOR,
    PLATFORM_BORDER,
    PLATFORM_HIGHLIGHT,
    PLATFORM_SHADOW,
)
from entities.player import Player
from states.base_state import State
from birthday_surprise.config import MESSAGE_TITLE, MESSAGE_LINES
from ui.text_glow import draw_glow_text

FLOOR_Y = 350
TEXT_CEILING_Y = 200

CONFETTI_COLORS = ["#FFCCCC", "#F2C896", "#FFD700", "#7BC96F", "#FF6666", "#D4956A"]


class ConfettiParticle:
    def __init__(self, spawn_top=True):
        self.x = random.uniform(0, SCREEN_WIDTH)
        if spawn_top:
            self.y = random.uniform(-30, SCREEN_HEIGHT * 0.4)
        else:
            self.y = random.uniform(-40, -5)
        self.vx = random.uniform(-1.2, 1.2)
        self.vy = random.uniform(1.0, 3.5)
        self.color = random.choice(CONFETTI_COLORS)
        self.size = random.randint(5, 9)
        self.spin = random.uniform(-3, 3)
        self.rotation = random.uniform(0, 360)
        self._surface = pygame.Surface((self.size, self.size * 2), pygame.SRCALPHA)
        self._surface.fill(self.color)
        self._build_rotated()

    def _build_rotated(self):
        self.image = pygame.transform.rotate(self._surface, self.rotation)

    def update(self, dt):
        scale = dt / 16.0
        self.vy += 0.06 * scale
        self.x += self.vx * scale
        self.y += self.vy * scale
        self.rotation = (self.rotation + self.spin * scale) % 360
        self._build_rotated()

    def off_screen(self):
        return self.y > SCREEN_HEIGHT + 20 or self.x < -20 or self.x > SCREEN_WIDTH + 20

    def draw(self, surface):
        rect = self.image.get_rect(center=(int(self.x), int(self.y)))
        surface.blit(self.image, rect)


class Confetti:
    def __init__(self, particle_count=70):
        self.particles = [ConfettiParticle(spawn_top=True) for _ in range(particle_count)]
        self.spawn_cooldown = 0

    def update(self, dt):
        self.spawn_cooldown -= dt
        for particle in self.particles:
            particle.update(dt)

        for index, particle in enumerate(self.particles):
            if particle.off_screen():
                self.particles[index] = ConfettiParticle(spawn_top=False)

        if self.spawn_cooldown <= 0:
            self.particles.append(ConfettiParticle(spawn_top=False))
            self.spawn_cooldown = 120

        if len(self.particles) > 90:
            self.particles.pop(0)

    def draw(self, surface):
        for particle in self.particles:
            particle.draw(surface)


class SecretRoom:
    def __init__(self, save_data):
        equipped_hat = save_data.equipped_hat if save_data else "none"
        spawn_x = SCREEN_WIDTH // 2
        self.player = Player((spawn_x, FLOOR_Y), equipped_hat=equipped_hat)
        self.platforms = [
            pygame.Rect(0, FLOOR_Y, SCREEN_WIDTH, 50),
            pygame.Rect(0, 0, SCREEN_WIDTH, TEXT_CEILING_Y),
        ]

    def update(self, keys):
        self.player.handle_input(keys)
        self.player.update(self.platforms, SCREEN_WIDTH)

    def draw_room(self, surface, background):
        surface.blit(background, (0, 0))

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((40, 20, 10, 100))
        surface.blit(overlay, (0, 0))

        floor = pygame.Rect(0, FLOOR_Y, SCREEN_WIDTH, 50)
        pygame.draw.rect(surface, PLATFORM_SHADOW, floor.move(0, 3), border_radius=3)
        pygame.draw.rect(surface, PLATFORM_COLOR, floor, border_radius=3)
        highlight = pygame.Rect(floor.left + 4, floor.top + 3, floor.width - 8, 5)
        pygame.draw.rect(surface, PLATFORM_HIGHLIGHT, highlight, border_radius=2)
        pygame.draw.rect(surface, PLATFORM_BORDER, floor, 2, border_radius=3)

    def draw_player(self, surface):
        if not self.player.is_invincible() or (pygame.time.get_ticks() // 150) % 2 == 0:
            surface.blit(self.player.image, self.player.rect)


class MessageState(State):
    def enter(self):
        self.background = pygame.image.load(
            GRAPHICS_PATH / "backgrounds" / "cafe.png"
        ).convert_alpha()
        self.room = SecretRoom(self.game.save_data)

        self.title_font = pygame.font.Font(str(FONT_PATH), 52)
        self.body_font = pygame.font.Font(str(FONT_PATH), 22)
        self.hint_font = pygame.font.Font(str(FONT_PATH), 18)

        self.title_surface = self.title_font.render(MESSAGE_TITLE, False, "#FFCCCC")
        self.title_glow_surface = self.title_font.render(MESSAGE_TITLE, False, "#2E1A0E")
        self.title_rect = self.title_surface.get_rect(center=(SCREEN_WIDTH // 2, 70))

        self.line_surfaces = []
        self.line_glow_surfaces = []
        for line in MESSAGE_LINES:
            self.line_surfaces.append(self.body_font.render(line, False, "#F2C896"))
            self.line_glow_surfaces.append(self.body_font.render(line, False, "#2E1A0E"))

        self.hint_surface = self.hint_font.render(
            "ESC to exit", False, "#FFCCCC"
        )
        self.hint_glow_surface = self.hint_font.render(
            "ESC to exit", False, "#2E1A0E"
        )
        self.hint_rect = self.hint_surface.get_rect(bottomright=(SCREEN_WIDTH - 12, SCREEN_HEIGHT - 10))

        self.move_hint = self.hint_font.render(
            "← → move   space jump", False, "#F2C896"
        )
        self.confetti = Confetti()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            from states.menu_state import MenuState

            self.game.change_state(MenuState(self.game))

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.room.update(keys)
        self.confetti.update(dt)

    def draw(self, surface):
        self.room.draw_room(surface, self.background)
        self.confetti.draw(surface)

        draw_glow_text(
            surface,
            self.title_surface,
            self.title_glow_surface,
            self.title_rect,
        )

        start_y = 130
        for index, (line, glow) in enumerate(
            zip(self.line_surfaces, self.line_glow_surfaces)
        ):
            rect = line.get_rect(center=(SCREEN_WIDTH // 2, start_y + index * 34))
            draw_glow_text(surface, line, glow, rect)

        self.room.draw_player(surface)

        surface.blit(self.move_hint, (10, 10))
        draw_glow_text(
            surface,
            self.hint_surface,
            self.hint_glow_surface,
            self.hint_rect,
        )
