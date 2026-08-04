LEVEL_1_1 = {
    "name": "Under the Counter",
    "background": "backgrounds/cafe.png",
    "spawn": (100, 350),
    "platforms": [
        (0, 350, 800, 50),
        (150, 280, 120, 20),
        (400, 220, 120, 20),
        (600, 280, 120, 20),
    ],
    "bones": [
        (300, 350),
        (210, 280),
        (460, 220),
        (660, 280),
    ],
    "goal": (750, 350),
    "enemies": [
        {"pos": (400, 350), "range": 100},
    ],
}

LEVELS = {
    "1-1": LEVEL_1_1,
}
