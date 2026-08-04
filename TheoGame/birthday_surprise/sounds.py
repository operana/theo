# TEMPORARY birthday feature — delete with the birthday_surprise/ folder.

import array
import math

import pygame

_sounds = {}


def _make_tone(frequency, duration_ms, volume=0.35, decay=True):
    sample_rate = 44100
    sample_count = int(sample_rate * duration_ms / 1000)
    buffer = array.array("h")

    for index in range(sample_count):
        progress = index / max(1, sample_count - 1)
        envelope = (1.0 - progress) if decay else 1.0
        wave = math.sin(2 * math.pi * frequency * (index / sample_rate))
        sample = int(32767 * volume * envelope * wave)
        buffer.append(sample)
        buffer.append(sample)

    return pygame.mixer.Sound(buffer=buffer)


def _make_whimper():
    sample_rate = 44100
    duration_ms = 320
    sample_count = int(sample_rate * duration_ms / 1000)
    buffer = array.array("h")

    for index in range(sample_count):
        progress = index / max(1, sample_count - 1)
        frequency = 420 - 200 * progress
        envelope = math.sin(math.pi * progress) ** 1.2
        tremolo = 0.85 + 0.15 * math.sin(2 * math.pi * 28 * (index / sample_rate))
        wave = math.sin(2 * math.pi * frequency * (index / sample_rate))
        sample = int(32767 * 0.32 * envelope * tremolo * wave)
        buffer.append(sample)
        buffer.append(sample)

    return pygame.mixer.Sound(buffer=buffer)


def _load_sounds():
    if _sounds:
        return _sounds

    try:
        if not pygame.mixer.get_init():
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        _sounds["chomp"] = _make_tone(180, 120, volume=0.45)
        _sounds["power_chomp"] = _make_tone(240, 140, volume=0.5)
        _sounds["damage"] = _make_tone(90, 220, volume=0.4)
        _sounds["whimper"] = _make_whimper()
        _sounds["heal"] = _make_tone(520, 160, volume=0.25, decay=True)
        _sounds["powerup"] = _make_tone(360, 200, volume=0.35)
        _sounds["defeat"] = _make_tone(420, 280, volume=0.4)
    except pygame.error:
        _sounds["_disabled"] = True

    return _sounds


def play(name):
    sounds = _load_sounds()
    if sounds.get("_disabled") or name not in sounds:
        return
    sounds[name].play()


def play_chomp(powered=False):
    play("power_chomp" if powered else "chomp")
