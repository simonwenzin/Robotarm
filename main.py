from board_factory import create_board
from file_manager import FileManager
from robot import Robot
from robot_shell import RobotShell


def main():
    file = FileManager()
    robot = Robot(create_board())
    robot.configure()
    RobotShell(robot, file).cmdloop()

if __name__ == "__main__":
    main()