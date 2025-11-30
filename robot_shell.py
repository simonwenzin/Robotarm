import cmd

from file_manager import FileManager
from robot import Robot


class RobotShell(cmd.Cmd):

    def __init__(self, robot: Robot, file: FileManager):
        super().__init__()
        self.DEFAULT_FILENAME = "data.json"
        self.robot = robot
        self.file = file
        self.intro = "Welcome to the HOLMES IV robot control system."
        self.prompt = f"robotarm/{file.get_filename()}$ "

    def do_exit(self, _arg):
        """Exits the program."""
        self.robot.exit()
        exit()

    def do_reset(self, _arg):
        """Sets all servos to 90 degrees"""
        self.robot.reset()

    def do_save(self, _arg):
        """Saves current state to file"""
        data = self.robot.get_servo_map()
        self.file.save_state(data)

    def do_select(self, arg):
        """Selects file"""
        self.file = FileManager(arg)
        self.prompt = f"robotarm/{arg}$ "

    def do_delete(self, _arg):
        """Deletes selected file"""
        try:
            self.file.delete()
            self.file = FileManager()
            self.prompt = "robotarm/data.json$ "
        except FileNotFoundError:
            print("File not found.")

    def do_run(self, _arg):
        """Runs commands from selected file"""
        self.robot.run_commands(self.file.load_state())

    def do_state(self, _arg):
        """Prints the current state of the robot"""
        self.robot.print_state()

    def do_move(self, args):
        """Move servo to angle"""
        if len(args.split()) != 2:
            print(f"invalid argument: {args}")
            return
        servo, angle = args.split()
        valid_servo = validate_servo(servo, self.robot.servo_map.keys())
        valid_angle = parse_angle(angle)
        if not valid_servo:
            print(f"invalid servo: '{servo}'")
            return
        if not valid_angle:
            print(f"invalid angle: '{angle}'")
            return

        self.robot.servo_move(valid_servo, valid_angle)

def validate_servo(arg, valid_servos):
    if arg in valid_servos:
        return arg
    else:
        return None

def parse_angle(arg):
    try:
        angle = int(arg)
        if 0 <= angle <= 180:
            return angle
        else:
            return None
    except ValueError:
        return None
