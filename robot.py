import time


class Robot:

    def __init__(self, board):
        self.board = board
        self.servo_map = {
            "torso": {"pin": 2, "angle": 90},
            "shoulder": {"pin": 3, "angle": 90},
            "elbow": {"pin": 4, "angle": 90},
            "wrist-pitch": {"pin": 5, "angle": 90},
            "wrist-roll": {"pin": 6, "angle": 90},
            "hand": {"pin": 7, "angle": 90},
        }

        self.servo_objects = {}

        self.STEP_SIZE = 1
        self.STEP_DELAY = 0.002

    def configure(self):
        for name, data in self.servo_map.items():
            pin = data["pin"]
            self.servo_objects[name] = self.board.get_pin(f"d:{pin}:s")
            self.board.servo_config(pin, 544, 2400)
            time.sleep(0.05)

    def servo_move(self, servo, target_angle):
        current_angle = self.servo_map[servo]["angle"]

        if target_angle > current_angle:
            step = self.STEP_SIZE
        else:
            step = -self.STEP_SIZE

        print(f"moving servo '{servo}' to angle '{target_angle}'")

        for angle in range(current_angle, target_angle, step):
            self.servo_objects[servo].write(angle)
            time.sleep(self.STEP_DELAY)

        self.servo_objects[servo].write(target_angle)
        self.servo_map[servo]["angle"] = target_angle

    def reset(self):
        for servo in self.servo_map.keys():
            self.servo_move(servo, 90)
            time.sleep(0.5)

    def run_commands(self, commands):
        for command in commands:
            for servo in command.keys():
                self.servo_move(servo, command[servo]["angle"])
                time.sleep(0.1)
            time.sleep(1)

        if len(commands) == 0:
            print(f"no commands found")
        else:
            print(f"successfully ran")

    def loop(self, file, repetitions):
        for repetition in range(repetitions):
            self.run_commands(file)
            time.sleep(1)

    def get_servo_map(self):
        return self.servo_map

    def print_state(self):
        for name, angle in self.servo_map.items():
            print(f"{name}: {self.servo_map[name]['angle']}")

    def exit(self):
        self.board.exit()
