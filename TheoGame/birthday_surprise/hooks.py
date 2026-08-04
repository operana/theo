# TEMPORARY birthday feature — delete with the birthday_surprise/ folder.

import pygame

from birthday_surprise.config import ENABLED
from birthday_surprise.hallway_state import HallwayState

__all__ = ["ENABLED", "act_complete_extra_hint", "handle_act_complete_key"]


def act_complete_extra_hint():
    if not ENABLED:
        return ""
    return "  |  N continue"


def handle_act_complete_key(game, key):
    if not ENABLED:
        return False

    if key == pygame.K_n:
        game.change_state(HallwayState(game))
        return True

    return False
