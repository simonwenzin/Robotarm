import time

from file_manager import FileManager

USE_SIM = True   # toggle simulator

if USE_SIM:
    from mock_board import MockBoard
    board = MockBoard()
    print("[SIM] Using simulator")
else:
    from pyfirmata2 import Arduino
    board = Arduino("/dev/ttyACM0")

servo_map = {
    "torso": {"pin": 2, "angle": 90},
    "shoulder": {"pin": 3, "angle": 90},
    "elbow": {"pin": 4, "angle": 90},
    "wrist-pitch": {"pin": 5, "angle": 90},
    "wrist-roll": {"pin": 6, "angle": 90},
    "hand": {"pin": 7, "angle": 90},
}

servo_objects = {}

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

    print(f"moving servo '{servo}' to angle '{target_angle}'")

    for angle in range(current_angle, target_angle, step):
        servo_objects[servo].write(angle)
        time.sleep(STEP_DELAY)

    servo_objects[servo].write(target_angle)
    servo_map[servo]["angle"] = target_angle

def run_commands(commands):
    """Runs file."""
    for command in commands:
        for servo in command.keys():
            servo_move(servo, command[servo]["angle"])
    if len(commands) == 0:
        print(f"no commands found")
    else:
        print(f"successfully ran")

def main():
    default_filename = "data.json"
    filename = default_filename
    file = FileManager(filename)

    for name, data in servo_map.items():
        pin = data["pin"]
        servo_objects[name] = board.get_pin(f"d:{pin}:s")
        board.servo_config(pin, 544, 2400)
        time.sleep(0.05)

    while True:
        user_input = input(filename + "$ ").lower()
        user_inputs = user_input.split()
        command = user_inputs[0]
        if len(user_inputs) > 1:
            argument = user_inputs[1]
        else:
            argument = None

        if command in ["quit", "exit", "kys", "bye"]:
            board.exit()
            break

        elif command == "reset":
            for servo in servo_map.keys():
                servo_move(servo, 90)
                servo_map[servo]["angle"] = 90
                time.sleep(0.5)

        elif command == "save":
            data = servo_map
            file.save_state(data)

        elif command == "load":
            if argument is None:
                print("no file provided")
            else:
                filename = argument
                file = FileManager(filename)

        elif command == "delete":
            if argument is None:
                print("no file provided")
            else:
                FileManager(argument).delete()
                if argument == filename:
                    filename = default_filename

        elif command == "run":
            if argument is None:
                print("no file provided")
            else:
                commands = FileManager(filename).load_state()
                run_commands(commands)

        elif command == "state":
            for name, angle in servo_map.items():
                print(f"{name}: {servo_map[name]['angle']}")

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
│  state                  → displays servo state│
│  quit / exit            → close program       │
└───────────────────────────────────────────────┘
Servos: torso, shoulder, elbow, wrist-pitch, wrist-roll, hand
Angles: 0–180°
""")

        elif command in servo_map.keys():
            try:
                argument = int(argument)
                servo_move(command, argument)

            except ValueError:
                print(f"invalid syntax: '{user_input}'")

        else:
            print(f"invalid command: '{command}'")

if __name__ == "__main__":
    main()