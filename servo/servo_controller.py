import pigpio


class ServoController:

    PAN_PIN = 18 #TODO: get this from the configurations file
    TILT_PIN = 13

    MIN_ANGLE = 1
    MAX_ANGLE = 180

    def __init__(self):

        self.pi = pigpio.pi()

        if not self.pi.connected:
            raise RuntimeError("Could not connect to pigpio daemon")

        self.pan_angle = 90
        self.tilt_angle = 90

        self.move_pan(self.pan_angle)
        self.move_tilt(self.tilt_angle)

    def angle_to_pulsewidth(self, angle):
        return 1000 + (angle / 180.0) * 1000

    def move_servo(self, pin, angle):

        angle = max(self.MIN_ANGLE, min(self.MAX_ANGLE, angle))

        pulse = self.angle_to_pulsewidth(angle)

        self.pi.set_servo_pulsewidth(pin, pulse)

    def move_pan(self, angle):

        self.pan_angle = angle
        self.move_servo(self.PAN_PIN, angle)

    def move_tilt(self, angle):

        self.tilt_angle = angle
        self.move_servo(self.TILT_PIN, angle)

    def idle_all(self):

        self.pi.set_servo_pulsewidth(self.PAN_PIN, 0)
        self.pi.set_servo_pulsewidth(self.TILT_PIN, 0)