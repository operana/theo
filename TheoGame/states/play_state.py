import pygame

from settings import FONT_PATH
from level import Level, LEVELS
from states.base_state import State
from ui import HUD, LevelCompleteScreen


class PlayState(State):
    LEVEL_ID = "1-1"

    def enter(self):
        self.hint_font = pygame.font.Font(str(FONT_PATH), 20)
        self.title_font = pygame.font.Font(str(FONT_PATH), 48)
        self.hud = HUD(self.hint_font)
        self.level_complete = LevelCompleteScreen(self.hint_font, self.title_font)
        self.hint_surface = self.hint_font.render(
            "← → move   space jump", False, "#FFCCCC"
        )
        self._start_level()

    def _start_level(self):
        self.level = Level(LEVELS[self.LEVEL_ID])

    def handle_event(self, event):
        if self.level.complete and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self._start_level()

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.level.update(keys)

    def draw(self, surface):
        self.level.draw(surface)

        if self.level.complete:
            self.level_complete.draw(
                surface,
                self.level.name,
                self.level.player.bones_collected,
                self.level.total_bones,
            )
        else:
            surface.blit(self.hint_surface, (10, 10))
            self.hud.draw(
                surface,
                self.level.player.bones_collected,
                self.level.total_bones,
            )
