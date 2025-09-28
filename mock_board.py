# mock_board.py
class MockServo:
    def __init__(self, pin):
        self.pin = pin
        self.angle = 0

    def write(self, angle):
        print(f"[SIM] Servo on pin {self.pin} -> angle {angle}")
        self.angle = angle

class MockPin:
    def __init__(self, pin):
        self.pin = pin

    def write(self, value):
        print(f"[SIM] Successfully wrote {value} to pin {self.pin} ")

class MockBoard:
    digital = [None,None,MockPin(2),MockPin(3),MockPin(4),MockPin(5),MockPin(6),MockPin(7)]
    def get_pin(self, pin_def):
        # e.g. 'd:9:s' for digital pin 9 servo
        pin_type = pin_def.split(':')[-1]
        if pin_type == 's':
            return MockServo(pin_def)
        raise NotImplementedError

    def servo_config(self, pin, min_pulse=544, max_pulse=2400, angle=0):
        print(f"[SIM] successfully configured pin {pin}")

    def exit(self):
        print("[SIM] Closing mock board")