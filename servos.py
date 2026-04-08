import RPi.GPIO as GPIO
import time

class Servo:

    def __init__(self, pin):

        self.pin = pin

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)

        self.pwm = GPIO.PWM(self.pin, 50)  # 50Hz
        self.pwm.start(0)

    def move(self, angle):

        duty = 2 + (angle / 18)

        self.pwm.ChangeDutyCycle(duty)

        time.sleep(0.4)

        # stop sending pulses
        self.pwm.ChangeDutyCycle(0)

    def cleanup(self):
        self.pwm.stop()