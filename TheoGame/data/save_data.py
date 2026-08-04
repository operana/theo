import json

from settings import BASE_DIR

SAVE_PATH = BASE_DIR / "save.json"


class SaveData:
    def __init__(self):
        self.total_bones = 0
        self.unlocked_hats = ["none"]
        self.equipped_hat = "none"
        self.completed_levels = []

    @classmethod
    def load(cls):
        save = cls()
        if not SAVE_PATH.exists():
            return save

        with open(SAVE_PATH, encoding="utf-8") as file:
            data = json.load(file)

        save.unlocked_hats = data.get("unlocked_hats", ["none"])
        save.equipped_hat = data.get("equipped_hat", "none")
        save.completed_levels = data.get("completed_levels", [])
        return save

    def save(self):
        data = {
            "unlocked_hats": self.unlocked_hats,
            "equipped_hat": self.equipped_hat,
            "completed_levels": self.completed_levels,
        }
        with open(SAVE_PATH, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2)

    def add_bones(self, amount):
        self.total_bones += amount

    def can_afford(self, cost):
        return self.total_bones >= cost

    def unlock_hat(self, hat_id):
        if hat_id not in self.unlocked_hats:
            self.unlocked_hats.append(hat_id)

    def buy_or_equip_hat(self, hat_id, cost):
        if hat_id in self.unlocked_hats:
            self.equipped_hat = hat_id
            self.save()
            return "equipped"

        if not self.can_afford(cost):
            return "too_poor"

        self.total_bones -= cost
        self.unlock_hat(hat_id)
        self.equipped_hat = hat_id
        self.save()
        return "bought"

    def mark_level_complete(self, level_id):
        if level_id not in self.completed_levels:
            self.completed_levels.append(level_id)
