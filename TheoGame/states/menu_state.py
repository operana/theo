import pygame

from settings import FONT_PATH, GRAPHICS_PATH
from states.base_state import State
from states.play_state import PlayState


class MenuState(State):
    def enter(self):
        self.background = pygame.image.load(
            GRAPHICS_PATH / "backgrounds" / "cafe.png"
        ).convert_alpha()
        self.title_font = pygame.font.Font(str(FONT_PATH), 75)
        self.hint_font = pygame.font.Font(str(FONT_PATH), 20)
        self.title_surface = self.title_font.render("theo's world", False, "#FFCCCC")
        self.title_glow_surface = self.title_font.render("theo's world", False, "#2E1A0E")
        self.title_rect = self.title_surface.get_rect(center=(400, 70))
        self.title_glow_offsets = [
            (-3, 0), (3, 0), (0, -3), (0, 3),
            (-2, -2), (2, -2), (-2, 2), (2, 2),
            (-1, -1), (1, -1), (-1, 1), (1, 1),
        ]
        self.hint_surface = self.hint_font.render(
            "Press SPACE to start", False, "#000000"
        )
        self.hint_rect = self.hint_surface.get_rect(center=(400, 340))
        self.blink_timer = 0
        self.show_hint = True

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.game.change_state(PlayState(self.game))

    def update(self, dt):
        self.blink_timer += dt
        if self.blink_timer >= 600:
            self.blink_timer = 0
            self.show_hint = not self.show_hint

    def _draw_title(self, surface):
        for dx, dy in self.title_glow_offsets:
            surface.blit(self.title_glow_surface, self.title_rect.move(dx, dy))
        surface.blit(self.title_surface, self.title_rect)

    def draw(self, surface):
        surface.blit(self.background, (0, 0))
        self._draw_title(surface)
        if self.show_hint:
            surface.blit(self.hint_surface, self.hint_rect)
