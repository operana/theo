# TEMPORARY birthday feature — delete with the birthday_surprise/ folder.

import pygame

from settings import (
    SCREEN_WIDTH,
    PLATFORM_COLOR,
    PLATFORM_BORDER,
    PLATFORM_HIGHLIGHT,
    PLATFORM_SHADOW,
)
from entities.player import Player
from entities.goal import Goal
from systems.camera import Camera
from states.base_state import State
from birthday_surprise.passcode_state import PasscodeState
from ui.mixed_text import get_pixel_font

HALLWAY_WIDTH = 1400
FLOOR_Y = 350


class HallwayLevel:
    def __init__(self, save_data):
        equipped_hat = save_data.equipped_hat if save_data else "none"
        self.player = Player((100, FLOOR_Y), equipped_hat=equipped_hat)
        self.platforms = [pygame.Rect(0, FLOOR_Y, HALLWAY_WIDTH, 50)]
        self.goal = Goal((HALLWAY_WIDTH - 80, FLOOR_Y))
        self.camera = Camera(HALLWAY_WIDTH)
        self.reached_goal = False

    def update(self, keys):
        if self.reached_goal:
            return

        self.player.handle_input(keys)
        self.player.update(self.platforms, HALLWAY_WIDTH)
        self.camera.update(self.player.rect)

        if self.goal.is_reached(self.player):
            self.reached_goal = True

    def draw(self, surface):
        self._draw_hallway(surface)

        floor = self.camera.apply(self.platforms[0])
        self._draw_floor(surface, floor)

        surface.blit(self.goal.image, self.camera.apply(self.goal.rect))
        surface.blit(self.player.image, self.camera.apply(self.player.rect))

    def _draw_hallway(self, surface):
        surface.fill("#1A0F08")

        wall_top = 60
        back_wall = pygame.Rect(0, wall_top, SCREEN_WIDTH, FLOOR_Y - wall_top)
        pygame.draw.rect(surface, "#2E1A0E", back_wall)

        offset_x = int(self.camera.offset.x)
        panel_width = 120
        start_panel = -(offset_x % panel_width)

        for x in range(start_panel - panel_width, SCREEN_WIDTH + panel_width, panel_width):
            panel = pygame.Rect(x, wall_top + 20, panel_width - 8, FLOOR_Y - wall_top - 40)
            pygame.draw.rect(surface, "#3A2215", panel, border_radius=2)
            pygame.draw.rect(surface, "#4A2C1A", panel, 1, border_radius=2)

        ceiling = pygame.Rect(0, wall_top - 8, SCREEN_WIDTH, 8)
        pygame.draw.rect(surface, "#4A2C1A", ceiling)

        baseboard = pygame.Rect(0, FLOOR_Y - 6, SCREEN_WIDTH, 6)
        pygame.draw.rect(surface, "#4A2C1A", baseboard)

    def _draw_floor(self, surface, floor):
        pygame.draw.rect(surface, PLATFORM_SHADOW, floor.move(0, 3), border_radius=3)
        pygame.draw.rect(surface, PLATFORM_COLOR, floor, border_radius=3)
        highlight = pygame.Rect(floor.left + 4, floor.top + 3, floor.width - 8, 5)
        pygame.draw.rect(surface, PLATFORM_HIGHLIGHT, highlight, border_radius=2)
        pygame.draw.rect(surface, PLATFORM_BORDER, floor, 2, border_radius=3)


class HallwayState(State):
    def enter(self):
        self.level = HallwayLevel(self.game.save_data)
        self.hint_font = get_pixel_font(18)
        self.hint_surface = self.hint_font.render(
            "Walk to the door...", False, "#F2C896"
        )

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            from states.menu_state import MenuState

            self.game.change_state(MenuState(self.game))

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.level.update(keys)

        if self.level.reached_goal:
            self.game.change_state(PasscodeState(self.game))

    def draw(self, surface):
        self.level.draw(surface)
        surface.blit(self.hint_surface, (10, 10))
