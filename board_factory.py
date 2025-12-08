def create_board():
    use_sim = True  # toggle simulator

    if use_sim:
        from mock_board import MockBoard
        print("[SIM] Using simulator")
        return MockBoard()
    else:
        from pyfirmata2 import Arduino
        return Arduino("/dev/ttyACM0")
