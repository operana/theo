import math

import pygame

from settings import FONT_PATH, GRAPHICS_PATH, SCREEN_WIDTH
from states.base_state import State
from states.play_state import PlayState
from ui.text_glow import draw_glow_text

THEO_MENU_WIDTH = 80
BOB_AMPLITUDE = 6
BOB_SPEED = 0.003


class MenuState(State):
    def enter(self):
        self.background = pygame.image.load(
            GRAPHICS_PATH / "backgrounds" / "cafe.png"
        ).convert_alpha()

        theo_image = pygame.image.load(
            GRAPHICS_PATH / "player" / "TheoSpriteSmall.png"
        ).convert_alpha()
        scale = THEO_MENU_WIDTH / theo_image.get_width()
        theo_size = (THEO_MENU_WIDTH, int(theo_image.get_height() * scale))
        self.theo_surface = pygame.transform.scale(theo_image, theo_size)
        self.theo_rect = self.theo_surface.get_rect(center=(SCREEN_WIDTH // 2, 210))

        self.title_font = pygame.font.Font(str(FONT_PATH), 75)
        self.subtitle_font = pygame.font.Font(str(FONT_PATH), 22)
        self.hint_font = pygame.font.Font(str(FONT_PATH), 22)

        self.title_surface = self.title_font.render("theo's world", False, "#FFCCCC")
        self.title_glow_surface = self.title_font.render("theo's world", False, "#2E1A0E")
        self.title_rect = self.title_surface.get_rect(center=(SCREEN_WIDTH // 2, 58))

        self.subtitle_surface = self.subtitle_font.render(
            "a cozy platform adventure", False, "#F2C896"
        )
        self.subtitle_glow_surface = self.subtitle_font.render(
            "a cozy platform adventure", False, "#2E1A0E"
        )
        self.subtitle_rect = self.subtitle_surface.get_rect(center=(SCREEN_WIDTH // 2, 118))

        self.hint_surface = self.hint_font.render(
            "Press SPACE to start", False, "#FFCCCC"
        )
        self.hint_glow_surface = self.hint_font.render(
            "Press SPACE to start", False, "#2E1A0E"
        )
        self.hint_rect = self.hint_surface.get_rect(center=(SCREEN_WIDTH // 2, 355))

        self.blink_timer = 0
        self.show_hint = True
        self.elapsed = 0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.game.change_state(PlayState(self.game, new_level=True))
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.game.change_state(PlayState(self.game, new_level=True))

    def update(self, dt):
        self.elapsed += dt
        self.blink_timer += dt
        if self.blink_timer >= 600:
            self.blink_timer = 0
            self.show_hint = not self.show_hint

    def draw(self, surface):
        surface.blit(self.background, (0, 0))

        draw_glow_text(
            surface,
            self.title_surface,
            self.title_glow_surface,
            self.title_rect,
        )
        draw_glow_text(
            surface,
            self.subtitle_surface,
            self.subtitle_glow_surface,
            self.subtitle_rect,
        )

        bob_offset = int(math.sin(self.elapsed * BOB_SPEED) * BOB_AMPLITUDE)
        theo_pos = self.theo_rect.move(0, bob_offset)
        surface.blit(self.theo_surface, theo_pos)

        if self.show_hint:
            draw_glow_text(
                surface,
                self.hint_surface,
                self.hint_glow_surface,
                self.hint_rect,
            )
