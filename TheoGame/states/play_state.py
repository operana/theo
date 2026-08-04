import pygame

from level import Level, LEVELS
from states.base_state import State
from states.shop_state import ShopState
from ui import HUD, LevelCompleteScreen


class PlayState(State):
    LEVEL_ID = "1-1"

    def __init__(self, game, new_level=False):
        super().__init__(game)
        self.new_level = new_level

    def enter(self):
        if not hasattr(self, "hud"):
            self.hud = HUD()
            self.level_complete = LevelCompleteScreen()
            self.hint_font = self.hud.pixel_font
            self.hint_surface = self.hint_font.render(
                "← → move   space jump", False, "#FFCCCC"
            )

        if self.new_level or not hasattr(self, "level"):
            self._start_level()
            self.bones_banked = False
        else:
            self.level.player.equipped_hat = self.game.save_data.equipped_hat
            self.level.player._update_facing()

        self.new_level = False

    def _start_level(self):
        self.level = Level(LEVELS[self.LEVEL_ID], self.game.save_data)
        self.bones_banked = False

    def handle_event(self, event):
        if not self.level.complete or event.type != pygame.KEYDOWN:
            return

        if event.key == pygame.K_r:
            self._start_level()
        elif event.key == pygame.K_s:
            self.game.change_state(ShopState(self.game))

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.level.update(keys)

        if self.level.complete and not self.bones_banked:
            self.game.save_data.add_bones(self.level.player.bones_collected)
            self.game.save_data.mark_level_complete(self.LEVEL_ID)
            self.game.save_data.save()
            self.bones_banked = True

    def draw(self, surface):
        self.level.draw(surface)

        if self.level.complete:
            self.level_complete.draw(
                surface,
                self.level.name,
                self.level.player.bones_collected,
                self.level.total_bones,
                self.game.save_data.total_bones,
            )
        else:
            surface.blit(self.hint_surface, (10, 10))
            self.hud.draw(
                surface,
                self.level.player.bones_collected,
                self.level.total_bones,
                self.game.save_data.total_bones,
                self.level.player.lives,
            )
