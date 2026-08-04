# Theo's World — platform adventure

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from game import Game

Game().run()
