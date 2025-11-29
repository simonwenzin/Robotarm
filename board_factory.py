def create_board():
    USE_SIM = True  # toggle simulator

    if USE_SIM:
        from mock_board import MockBoard
        print("[SIM] Using simulator")
        return MockBoard()
    else:
        from pyfirmata2 import Arduino
        return Arduino("/dev/ttyACM0")
