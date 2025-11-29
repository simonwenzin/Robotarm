import json
import os


class FileManager:

    def __init__(self, filename):
        self.filename = filename

    def save_state(self, data):
        """Saves current state to file."""
        state = self.load_state()
        state.append(data)
        with open(self.filename, "wt") as f:
            json.dump(state, f)
        print(f"saved '{self.filename}'")

    def load_state(self):
        """Loads state from file."""
        try:
            with open(self.filename, "rt") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def delete(self):
        """Deletes file."""
        os.remove(self.filename)
        print(f"deleted '{self.filename}'")