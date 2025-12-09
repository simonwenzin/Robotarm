class MockServo:

    def __init__(self, pin):
        self.pin = pin
        self.angle = 0

    def write(self, angle):
        print(f"[SIM] Moving servo on pin {self.pin} to angle {angle}")
        self.angle = angle


class MockPin:

    def __init__(self, pin):
        self.pin = pin


class MockBoard:

    def __init__(self):
        self.analog = []
        self.digital = [None, None, MockPin(2), MockPin(3), MockPin(4), MockPin(5), MockPin(6), MockPin(7)]
        self.sp = None  # serial port placeholder

    def get_pin(self, pin_def):
        # e.g. 'd:9:s' for digital pin 9 servo
        pin_type = pin_def.split(':')[-1]
        if pin_type == 's':
            return MockServo(pin_def)
        raise NotImplementedError

    def servo_config(self, pin, _min_pulse, _max_pulse):
        print(f"[SIM] Successfully configured pin {pin}")

    def exit(self):
        print("[SIM] Closing mock board")
