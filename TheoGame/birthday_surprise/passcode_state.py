# TEMPORARY birthday feature — delete with the birthday_surprise/ folder.

import pygame

from settings import GRAPHICS_PATH, SCREEN_WIDTH, SCREEN_HEIGHT, FONT_PATH
from states.base_state import State
from birthday_surprise.config import PASSCODE
from birthday_surprise.message_state import MessageState
from ui.text_glow import draw_glow_text

DOOR_DISPLAY_WIDTH = 120
WRONG_CODE_MS = 1200
DIGIT_BOX_SIZE = 56
DIGIT_BOX_GAP = 16


class PasscodeState(State):
    def enter(self):
        self.background = pygame.image.load(
            GRAPHICS_PATH / "backgrounds" / "cafe.png"
        ).convert_alpha()

        door_image = pygame.image.load(
            GRAPHICS_PATH / "items" / "doorSmall.png"
        ).convert_alpha()
        scale = DOOR_DISPLAY_WIDTH / door_image.get_width()
        door_size = (DOOR_DISPLAY_WIDTH, int(door_image.get_height() * scale))
        self.door_surface = pygame.transform.scale(door_image, door_size)
        self.door_rect = self.door_surface.get_rect(center=(SCREEN_WIDTH // 2, 185))

        self.title_font = pygame.font.Font(str(FONT_PATH), 36)
        self.label_font = pygame.font.Font(str(FONT_PATH), 22)
        self.digit_font = pygame.font.Font(str(FONT_PATH), 40)
        self.placeholder_font = pygame.font.Font(str(FONT_PATH), 32)
        self.hint_font = pygame.font.Font(str(FONT_PATH), 18)

        self.digits = ""
        self.wrong_until = 0
        self.last_input_at = 0

    def _add_digit(self, digit):
        if len(self.digits) < 4:
            self.digits += digit
            self.last_input_at = pygame.time.get_ticks()

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return

        number_keys = {
            pygame.K_0: "0", pygame.K_1: "1", pygame.K_2: "2", pygame.K_3: "3",
            pygame.K_4: "4", pygame.K_5: "5", pygame.K_6: "6", pygame.K_7: "7",
            pygame.K_8: "8", pygame.K_9: "9",
            pygame.K_KP0: "0", pygame.K_KP1: "1", pygame.K_KP2: "2", pygame.K_KP3: "3",
            pygame.K_KP4: "4", pygame.K_KP5: "5", pygame.K_KP6: "6", pygame.K_KP7: "7",
            pygame.K_KP8: "8", pygame.K_KP9: "9",
        }

        if event.key in number_keys:
            self._add_digit(number_keys[event.key])
        elif event.key == pygame.K_BACKSPACE:
            self.digits = self.digits[:-1]
            self.last_input_at = pygame.time.get_ticks()
        elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            self._submit()
        elif event.key == pygame.K_ESCAPE:
            from states.menu_state import MenuState

            self.game.change_state(MenuState(self.game))

    def _submit(self):
        if self.digits == PASSCODE:
            self.game.change_state(MessageState(self.game))
        else:
            self.wrong_until = pygame.time.get_ticks() + WRONG_CODE_MS
            self.digits = ""

    def update(self, dt):
        pass

    def _draw_digit_boxes(self, surface, center_y):
        wrong = pygame.time.get_ticks() < self.wrong_until
        total_width = 4 * DIGIT_BOX_SIZE + 3 * DIGIT_BOX_GAP
        start_x = SCREEN_WIDTH // 2 - total_width // 2
        flash = pygame.time.get_ticks() - self.last_input_at < 150

        for index in range(4):
            x = start_x + index * (DIGIT_BOX_SIZE + DIGIT_BOX_GAP)
            box = pygame.Rect(x, center_y - DIGIT_BOX_SIZE // 2, DIGIT_BOX_SIZE, DIGIT_BOX_SIZE)

            filled = index < len(self.digits)
            is_next = index == len(self.digits) and len(self.digits) < 4
            show_cursor = is_next and (pygame.time.get_ticks() // 400) % 2 == 0

            if wrong:
                fill_color = "#5A2020"
                border_color = "#FF6666"
            elif filled and flash and index == len(self.digits) - 1:
                fill_color = "#8B5A3C"
                border_color = "#FFCCCC"
            elif filled:
                fill_color = "#6B4423"
                border_color = "#F2C896"
            elif is_next:
                fill_color = "#4A2C1A"
                border_color = "#FFCCCC" if show_cursor else "#F2C896"
            else:
                fill_color = "#3A2215"
                border_color = "#8B5A3C"

            pygame.draw.rect(surface, fill_color, box, border_radius=6)
            pygame.draw.rect(surface, border_color, box, 3, border_radius=6)

            if filled:
                digit = self.digit_font.render(self.digits[index], False, "#FFCCCC")
                surface.blit(digit, digit.get_rect(center=box.center))
            elif is_next and show_cursor:
                cursor = self.placeholder_font.render("|", False, "#FFCCCC")
                surface.blit(cursor, cursor.get_rect(center=box.center))
            else:
                placeholder = self.placeholder_font.render("?", False, "#6B4423")
                surface.blit(placeholder, placeholder.get_rect(center=box.center))

    def draw(self, surface):
        surface.blit(self.background, (0, 0))

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((20, 10, 5, 140))
        surface.blit(overlay, (0, 0))

        surface.blit(self.door_surface, self.door_rect)

        title = self.title_font.render("Secret Door", False, "#FFCCCC")
        title_glow = self.title_font.render("Secret Door", False, "#2E1A0E")
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 60))
        draw_glow_text(surface, title, title_glow, title_rect)

        label = self.label_font.render("Enter 4-digit passcode", False, "#F2C896")
        surface.blit(label, label.get_rect(center=(SCREEN_WIDTH // 2, 255)))

        self._draw_digit_boxes(surface, 305)

        if pygame.time.get_ticks() < self.wrong_until:
            wrong = self.hint_font.render("Wrong passcode — try again", False, "#FF6666")
            surface.blit(wrong, wrong.get_rect(center=(SCREEN_WIDTH // 2, 340)))

        hint = self.hint_font.render(
            "0-9 type code  |  ENTER submit  |  ESC menu", False, "#F2C896"
        )
        surface.blit(hint, hint.get_rect(center=(SCREEN_WIDTH // 2, 370)))
