import pygame

from settings import GRAPHICS_PATH, SCREEN_WIDTH, SCREEN_HEIGHT, UI_FONT_SIZE
from data.hats import HATS, SHOP_HATS
from entities.hat_assets import get_shop_hat
from states.base_state import State
from ui.mixed_text import get_pixel_font, get_ui_font, blit_mixed_line
from ui.text_glow import draw_glow_text


class ShopState(State):
    def __init__(self, game, level_id="1-1"):
        super().__init__(game)
        self.level_id = level_id

    def enter(self):
        self.background = pygame.image.load(
            GRAPHICS_PATH / "backgrounds" / "cafe.png"
        ).convert_alpha()
        self.title_font = get_pixel_font(48)
        self.pixel_font = get_pixel_font(22)
        self.small_font = get_pixel_font(18)
        self.ui_font = get_ui_font(UI_FONT_SIZE)
        self.message = ""
        self.message_timer = 0

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return

        if event.key == pygame.K_SPACE:
            from states.play_state import PlayState

            self.game.change_state(PlayState(self.game, level_id=self.level_id))
            return

        hat_keys = {
            pygame.K_1: SHOP_HATS[0],
            pygame.K_2: SHOP_HATS[1],
            pygame.K_3: SHOP_HATS[2],
        }
        if event.key in hat_keys:
            self._try_hat(hat_keys[event.key])

    def _try_hat(self, hat_id):
        hat = HATS[hat_id]
        result = self.game.save_data.buy_or_equip_hat(hat_id, hat["cost"])

        if result == "bought":
            self.message = f"Purchased {hat['name']}!"
        elif result == "equipped":
            self.message = f"Equipped {hat['name']}!"
        else:
            self.message = "Not enough bones!"
        self.message_timer = 2000

    def update(self, dt):
        if self.message_timer > 0:
            self.message_timer -= dt
            if self.message_timer <= 0:
                self.message = ""

    def _hat_line_parts(self, index, hat_id):
        hat = HATS[hat_id]
        unlocked = hat_id in self.game.save_data.unlocked_hats
        parts = [
            ("[", "pixel"),
            (str(index + 1), "ui"),
            ("] ", "pixel"),
            (f"{hat['name']} — ", "pixel"),
        ]
        if unlocked:
            parts.append(("Owned", "pixel"))
        else:
            parts.append((str(hat["cost"]), "ui"))
            parts.append((" bones", "pixel"))
        return parts

    def draw(self, surface):
        surface.blit(self.background, (0, 0))

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((20, 10, 5, 180))
        surface.blit(overlay, (0, 0))

        title = self.title_font.render("Hat Shop", False, "#FFCCCC")
        title_glow = self.title_font.render("Hat Shop", False, "#2E1A0E")
        draw_glow_text(surface, title, title_glow, title.get_rect(center=(SCREEN_WIDTH // 2, 50)))

        blit_mixed_line(
            surface,
            [("Bones: ", "pixel"), (str(self.game.save_data.total_bones), "ui")],
            (SCREEN_WIDTH // 2, 100),
            self.pixel_font,
            self.ui_font,
            "#F2C896",
        )

        equipped = HATS[self.game.save_data.equipped_hat]["name"]
        equipped_surface = self.small_font.render(
            f"Equipped: {equipped}",
            False,
            "#FFCCCC",
        )
        surface.blit(
            equipped_surface,
            equipped_surface.get_rect(center=(SCREEN_WIDTH // 2, 130)),
        )

        for index, hat_id in enumerate(SHOP_HATS):
            y = 185 + index * 45
            color = "#FFCCCC" if hat_id in self.game.save_data.unlocked_hats else "#F2C896"
            blit_mixed_line(
                surface,
                self._hat_line_parts(index, hat_id),
                (SCREEN_WIDTH // 2, y),
                self.pixel_font,
                self.ui_font,
                color,
            )

            hat_surface = get_shop_hat(hat_id)
            if hat_surface:
                surface.blit(
                    hat_surface,
                    hat_surface.get_rect(center=(SCREEN_WIDTH // 2 + 200, y)),
                )

        hint = self.small_font.render(
            "1/2/3 buy or equip  |  SPACE to return",
            False,
            "#F2C896",
        )
        surface.blit(hint, hint.get_rect(center=(SCREEN_WIDTH // 2, 340)))

        if self.message:
            msg = self.pixel_font.render(self.message, False, "#FFCCCC")
            surface.blit(msg, msg.get_rect(center=(SCREEN_WIDTH // 2, 370)))
