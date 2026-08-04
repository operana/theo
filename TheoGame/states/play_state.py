import pygame

from level import Level, LEVELS, ACT_1_LEVELS
from states.base_state import State
from states.shop_state import ShopState
from ui import HUD, LevelCompleteScreen


class PlayState(State):
    def __init__(self, game, new_level=False, level_id="1-1"):
        super().__init__(game)
        self.new_level = new_level
        self.level_id = level_id

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
        self.level = Level(LEVELS[self.level_id], self.game.save_data)
        self.bones_banked = False

    def _next_level_id(self):
        index = ACT_1_LEVELS.index(self.level_id)
        if index + 1 < len(ACT_1_LEVELS):
            return ACT_1_LEVELS[index + 1]
        return None

    def _is_act_complete(self):
        return self.level_id == ACT_1_LEVELS[-1]

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return

        if self.level.complete:
            if event.key == pygame.K_r:
                self._start_level()
            elif event.key == pygame.K_s:
                self.game.change_state(ShopState(self.game, self.level_id))
            elif event.key == pygame.K_n and self._next_level_id():
                self.level_id = self._next_level_id()
                self._start_level()
            elif event.key == pygame.K_SPACE and self._is_act_complete():
                from states.menu_state import MenuState

                self.game.change_state(MenuState(self.game))

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.level.update(keys)

        if self.level.complete and not self.bones_banked:
            self.game.save_data.add_bones(self.level.player.bones_collected)
            self.game.save_data.mark_level_complete(self.level_id)
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
                has_next_level=self._next_level_id() is not None,
                act_complete=self._is_act_complete(),
            )
        else:
            surface.blit(self.hint_surface, (10, 10))
            level_label = self.hint_font.render(
                f"Level {self.level_id}", False, "#F2C896"
            )
            surface.blit(level_label, (10, 34))
            self.hud.draw(
                surface,
                self.level.player.bones_collected,
                self.level.total_bones,
                self.game.save_data.total_bones,
                self.level.player.lives,
            )
