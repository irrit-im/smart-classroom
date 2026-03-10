import RPi.GPIO as GPIO
import config

GPIO.setmode(GPIO.BCM)

class ServoController:

    def __init__(self):

        GPIO.setup(config.SERVO_X_PIN, GPIO.OUT)
        GPIO.setup(config.SERVO_Y_PIN, GPIO.OUT)

        self.servo_x = GPIO.PWM(config.SERVO_X_PIN, 50)
        self.servo_y = GPIO.PWM(config.SERVO_Y_PIN, 50)

        self.servo_x.start(7.5)
        self.servo_y.start(7.5)

    def move(self, x_angle, y_angle):

        duty_x = 2 + (x_angle / 18)
        duty_y = 2 + (y_angle / 18)

        self.servo_x.ChangeDutyCycle(duty_x)
        self.servo_y.ChangeDutyCycle(duty_y)