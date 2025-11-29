from board_factory import create_board
from file_manager import FileManager
from robot import Robot

def main():
    default_filename = "data.json"
    filename = default_filename
    file = FileManager(filename)
    robot = Robot(create_board())
    robot.configure()

    while True:
        user_input = input(f"robotarm/{filename}$ ").lower()
        user_inputs = user_input.split()
        command = user_inputs[0]
        if len(user_inputs) > 1:
            argument = user_inputs[1]
        else:
            argument = None

        if command in ["quit", "exit", "kys", "bye"]:
            robot.exit()
            break

        elif command == "reset":
            robot.reset()

        elif command == "save":
            data = robot.get_servo_map()
            file.save_state(data)

        elif command == "select":
            filename = argument
            file = FileManager(filename)

        elif command == "delete":
            file.delete()
            filename = default_filename
            file = FileManager(filename)

        elif command == "run":
            robot.run_commands(file.load_state())

        elif command == "state":
            robot.print_state()

        elif command == "help":
            print("""
┌─ Robot Arm Control ───────────────────────────┐
│  [servo] [angle]        → move servo to angle │
│  save                   → save current state  │
│  run                    → run saved sequence  │
│  select [file]          → switch save file    │
│  delete                 → delete save file    │
│  reset                  → reset all servos    │
│  help                   → show this menu      │
│  state                  → displays servo state│
│  quit / exit            → close program       │
└───────────────────────────────────────────────┘
Servos: torso, shoulder, elbow, wrist-pitch, wrist-roll, hand
Angles: 0–180°
""")

        elif command in robot.get_servo_map().keys():
            try:
                robot.servo_move(command, int(argument))

            except ValueError:
                print(f"invalid syntax: '{user_input}'")

        else:
            print(f"invalid command: '{command}'")

if __name__ == "__main__":
    main()