from utils.specs import Specs
import json


class SpecsManager:
    def __init__(self, json_path="specs.json"):
        self.json_path = json_path
        self.specs = Specs.run_all()
        self.save_to_json()

    def save_to_json(self):
        """Save the specs dictionary to a JSON file."""
        with open(self.json_path, "w") as f:
            json.dump(self.specs, f, indent=2)
        return True
