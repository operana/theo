import pygame

from settings import GRAPHICS_PATH
from data.hats import HATS

PLAYER_HAT_WIDTH = 42
SHOP_HAT_WIDTH = 48
HAT_TOP_PADDING = 50
HAT_HEAD_Y = 12
HAT_ANCHOR_X = {"right": 56, "left": 24}

_cache = {}


def _crop_to_content(image):
    mask = pygame.mask.from_surface(image)
    rects = mask.get_bounding_rects()
    if not rects:
        return image

    bounds = rects[0]
    for rect in rects[1:]:
        bounds.union_ip(rect)
    return image.subsurface(bounds).copy()


def _scale_image(image, width):
    cropped = _crop_to_content(image)
    scale = width / cropped.get_width()
    size = (width, int(cropped.get_height() * scale))
    return pygame.transform.scale(cropped, size)


def _load_cache():
    if _cache:
        return

    for hat_id, hat in HATS.items():
        if not hat.get("image"):
            continue

        image = pygame.image.load(GRAPHICS_PATH / hat["image"]).convert_alpha()
        _cache[hat_id] = {
            "player": _scale_image(image, PLAYER_HAT_WIDTH),
            "shop": _scale_image(image, SHOP_HAT_WIDTH),
        }


def get_hat_anchor(facing):
    return (HAT_ANCHOR_X[facing], HAT_HEAD_Y)


def get_player_hat(hat_id, facing="right"):
    _load_cache()
    if hat_id not in _cache:
        return None

    hat = _cache[hat_id]["player"]
    if facing == "left":
        return pygame.transform.flip(hat, True, False)
    return hat


def compose_player_with_hat(base, hat_surface, facing):
    anchor = get_hat_anchor(facing)
    hat_rect = hat_surface.get_rect(midbottom=anchor)
    hat_rect.y += HAT_TOP_PADDING

    left_pad = max(0, -hat_rect.left)
    right_pad = max(0, hat_rect.right - base.get_width())
    width = base.get_width() + left_pad + right_pad
    height = base.get_height() + HAT_TOP_PADDING

    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    surface.blit(base, (left_pad, HAT_TOP_PADDING))
    hat_rect.x += left_pad
    surface.blit(hat_surface, hat_rect)
    return surface


def get_shop_hat(hat_id):
    _load_cache()
    if hat_id not in _cache:
        return None
    return _cache[hat_id]["shop"]
