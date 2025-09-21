import json
import os
import time
from pyfirmata import Arduino

board = Arduino("/dev/ttyACM0")
servo_map = {
    "torso": {"pin": 2, "angle": 90},
    "shoulder": {"pin": 3, "angle": 90},
    "elbow": {"pin": 4, "angle": 90},
    "wrist": {"pin": 5, "angle": 90},
    "hand": {"pin": 6, "angle": 90},
}

def servo_move(servo, angle):
    """Moves a specific servo a specified angle in degrees."""
    if servo not in servo_map:
        print(f"invalid servo: '{servo}'")
        return
    if not (0 <= angle <= 180):
        print(f"invalid angle: '{angle}'")
        return
    board.digital[servo_map[servo]["pin"]].write(angle)
    servo_map[servo]["angle"] = angle

def save_state(data, filename):
    state = load_state(filename)
    state.append(data)
    with open(filename, "wt") as f:
        json.dump(state, f)

def load_state(filename):
    with open(filename, "rt") as f:
        return json.load(f)

def delete_file(filename):
    os.remove(filename)

def main():
    for pin in servo_map.values():
        board.servo_config(pin["pin"], 544, 2400)

    while True:
        user_input = input("$ ").lower()
        if user_input == "quit":
            break

        elif user_input == "reset":
            for pin in servo_map.values():
                board.digital[pin["pin"]].write(90)
                time.sleep(0.5)

        elif user_input == "save":
            data = [servo_map]
            save_state(data, "data.json")

        elif user_input == "delete":
            delete_file("data.json")

        else:
            try:
                input_servo, input_angle = user_input.split()
                input_angle = int(input_angle)
                servo_move(input_servo, input_angle)

            except ValueError:
                print(f"invalid syntax: '{user_input}'")

if __name__ == "__main__":
    main()