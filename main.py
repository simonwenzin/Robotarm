from file_manager import FileManager
from robot import Robot

def main():
    default_filename = "data.json"
    filename = default_filename
    file = FileManager(filename)
    robot = Robot()
    robot.configure()

    while True:
        user_input = input(filename + "$ ").lower()
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
                robot.run_commands(commands)

        elif command == "state":
            robot.print_state()

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

        elif command in robot.get_servo_map().keys():
            try:
                robot.servo_move(command, int(argument))

            except ValueError:
                print(f"invalid syntax: '{user_input}'")

        else:
            print(f"invalid command: '{command}'")

if __name__ == "__main__":
    main()