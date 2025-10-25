import json
import os
import time
from pyfirmata import Arduino
from serial import SerialException
from mock_board import MockBoard

try:
    board = Arduino("/dev/ttyACM0")
except SerialException:
    print("board not found, running simulator")
    board = MockBoard()

servo_map = {
    "torso": {"pin": 2, "angle": 90},
    "shoulder": {"pin": 3, "angle": 90},
    "elbow": {"pin": 4, "angle": 90},
    "wrist-pitch": {"pin": 5, "angle": 90},
    "wrist-roll": {"pin": 6, "angle": 90},
    "hand": {"pin": 7, "angle": 90},
}

STEP_SIZE = 1
STEP_DELAY = 0.02

def servo_move(servo, target_angle):
    """Moves a specific servo a specified angle in degrees."""
    if servo not in servo_map:
        print(f"invalid servo: '{servo}'")
        return
    if not (0 <= target_angle <= 180):
        print(f"invalid angle: '{target_angle}'")
        return

    current_angle = servo_map[servo]["angle"]
    if target_angle > current_angle:
        step = STEP_SIZE
    else:
        step = -STEP_SIZE

    for angle in range(current_angle, target_angle, step):
        board.digital [servo_map[servo]["pin"]].write(angle)
        time.sleep(STEP_DELAY)

    board.digital[servo_map[servo]["pin"]].write(target_angle)
    servo_map[servo]["angle"] = target_angle
    print(f"moving servo '{servo}' to angle '{target_angle}'")

def save_state(data, filename):
    """Saves current state to file."""
    state = load_state(filename)
    state.append(data)
    with open(filename, "wt") as f:
        json.dump(state, f)
    print(f"saved '{filename}'")

def load_state(filename):
    """Loads state from file."""
    try:
        with open(filename, "rt") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def delete_file(filename):
    """Deletes file."""
    os.remove(filename)
    print(f"deleted '{filename}'")

def run_file(filename):
    """Runs file."""
    commands = load_state(filename)
    for command in commands:
        for servo in command.keys():
            servo_move(servo, command[servo]["angle"])
    if len(commands) == 0:
        print(f"no commands found in '{filename}'")
    else:
        print(f"successfully ran '{filename}'")

def main():
    default_filename = "data.json"
    filename = default_filename

    for pin in servo_map.values():
        board.servo_config(pin["pin"], 544, 2400)

    while True:
        user_input = input(filename + "$ ").lower()
        user_inputs = user_input.split()
        command = user_inputs[0]
        if len(user_inputs) > 1:
            argument = user_inputs[1]
        else:
            argument = None

        if command == "quit" or command == "exit":
            break

        elif command == "reset":
            for pin in servo_map.values():
                board.digital[pin["pin"]].write(90)
                time.sleep(0.5)

        elif command == "save":
            data = servo_map
            save_state(data, filename)

        elif command == "load":
            filename = argument

        elif command == "delete":
            delete_file(filename)
            filename = default_filename

        elif command == "run":
            run_file(argument)

        elif command == "help":
            print("""
┌─ Robot Arm Control ───────────────────────────┐
│  [servo] [angle]        → move servo to angle │
│  save                   → save current state  │
│  run [file]             → run saved sequence  │
│  load [file]            → switch save file    │
│  delete [file]          → delete save file    │
│  reset                  → reset all servos    │
│  help                   → show this menu      │
│  quit / exit            → close program       │
└───────────────────────────────────────────────┘
Servos: torso, shoulder, elbow, wrist-pitch, wrist-roll, hand
Angles: 0–180°
""")

        elif command in servo_map.keys():
            try:
                if command in servo_map:
                    argument = int(argument)
                    servo_move(command, argument)

            except ValueError:
                print(f"invalid syntax: '{user_input}'")

        else:
            print(f"invalid command: '{command}'")

if __name__ == "__main__":
    main()