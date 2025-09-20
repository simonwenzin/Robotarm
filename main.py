import time
from pyfirmata import Arduino

board = Arduino("/dev/ttyACM0")
servo_map = {
    "torso": 2,
    "shoulder": 3,
    "elbow": 4,
    "wrist": 5,
    "hand": 6,
}

for pin in servo_map.values():
    board.servo_config(pin, 544, 2400)

def servo_move(servo, angle):
    if servo is None:
        print(f"invalid servo: '{servo}'")
        return
    if not (0 <= angle < 180):
        print(f"invalid angle: '{angle}'")
        return
    board.digital[servo_map[servo]].write(angle)

while True:
    user_input = input().lower()
    if user_input == "quit":
        break

    elif user_input == "reset":
        for pin in servo_map.values():
            board.digital[pin].write(180)
            time.sleep(0.5)

    try:
        input_servo, input_angle = user_input.split()
        input_angle = int(input_angle)
        servo_move(input_servo, input_angle)

    except ValueError:
        print(f"invalid syntax: '{user_input}'")