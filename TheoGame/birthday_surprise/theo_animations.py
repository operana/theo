# TEMPORARY birthday feature — delete with the birthday_surprise/ folder.

import pygame

from settings import GRAPHICS_PATH
from entities.hat_assets import compose_player_with_hat, get_player_hat

SHEET_PATH = GRAPHICS_PATH / "player" / "theoAnimationList.png"
CHOMP_SOURCE_RECTS = [
    pygame.Rect(47, 783, 153, 164),
    pygame.Rect(258, 783, 166, 164),
    pygame.Rect(486, 783, 174, 164),
    pygame.Rect(727, 783, 152, 164),
]
CHOMP_FRAME_MS = 85
CHOMP_IMPACT_FRAME = 2
CHOMP_ATTACK_FRAMES = {1, 2}
THEO_BODY_WIDTH = 80
THEO_BODY_HEIGHT = 71
WHITE_KEY_THRESHOLD = 245

_frame_cache = {}


def _strip_near_white(image, threshold=WHITE_KEY_THRESHOLD):
    cleaned = image.copy()
    width, height = cleaned.get_size()
    for y in range(height):
        for x in range(width):
            red, green, blue, alpha = cleaned.get_at((x, y))
            if alpha > 0 and red >= threshold and green >= threshold and blue >= threshold:
                cleaned.set_at((x, y), (0, 0, 0, 0))
    return cleaned


def _crop_to_content(image):
    mask = pygame.mask.from_surface(image)
    rects = mask.get_bounding_rects()
    if not rects:
        return image.copy()

    bounds = rects[0]
    for rect in rects[1:]:
        bounds.union_ip(rect)
    return image.subsurface(bounds).copy()


def _scale_frame(image):
    cropped = _crop_to_content(image)
    scale = min(
        THEO_BODY_WIDTH / cropped.get_width(),
        THEO_BODY_HEIGHT / cropped.get_height(),
    )
    size = (
        max(1, int(cropped.get_width() * scale)),
        max(1, int(cropped.get_height() * scale)),
    )
    return pygame.transform.scale(cropped, size)


def _load_base_frame(index, facing):
    key = (index, facing)
    if key in _frame_cache:
        return _frame_cache[key]

    sheet = pygame.image.load(SHEET_PATH).convert_alpha()
    frame = sheet.subsurface(CHOMP_SOURCE_RECTS[index]).copy()
    frame = _strip_near_white(frame)
    frame = _scale_frame(frame)
    if facing == "left":
        frame = pygame.transform.flip(frame, True, False)

    _frame_cache[key] = frame
    return frame


def _compose_frame(base, equipped_hat, facing):
    hat_surface = get_player_hat(equipped_hat, facing)
    if hat_surface:
        return compose_player_with_hat(base, hat_surface, facing)
    return base


class ChompAnimation:
    def __init__(self):
        self.active = False
        self.started_at = 0
        self.frame_index = 0

    def start(self, player):
        self.active = True
        self.started_at = pygame.time.get_ticks()
        self.frame_index = 0
        self._apply_frame(player)

    def update(self, player, powered=False):
        if not self.active:
            return

        elapsed = pygame.time.get_ticks() - self.started_at
        self.frame_index = min(len(CHOMP_SOURCE_RECTS) - 1, elapsed // CHOMP_FRAME_MS)

        if elapsed >= len(CHOMP_SOURCE_RECTS) * CHOMP_FRAME_MS:
            self.active = False
            player._update_facing()
            return

        self._apply_frame(player)

    def is_active(self):
        return self.active

    def is_impact_frame(self):
        return self.active and self.frame_index == CHOMP_IMPACT_FRAME

    def is_attack_frame(self):
        return self.active and self.frame_index in CHOMP_ATTACK_FRAMES

    def _apply_frame(self, player):
        feet = player.rect.midbottom
        base = _load_base_frame(self.frame_index, player.facing)
        player.image = _compose_frame(base, player.equipped_hat, player.facing)
        player.rect = player.image.get_rect()
        player.rect.midbottom = feet
