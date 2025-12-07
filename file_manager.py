import json
import os


class FileManager:

    def __init__(self, filename="data.json"):
        self.filename = filename

    def save_state(self, data):
        state = self.load_state()
        state.append(data)
        with open(self.filename, "wt") as f:
            json.dump(state, f)
        print(f"Saved '{self.filename}'")

    def load_state(self):
        try:
            with open(self.filename, "rt") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def delete(self):
        os.remove(self.filename)
        print(f"Deleted '{self.filename}'")

    def get_filename(self):
        return self.filename
