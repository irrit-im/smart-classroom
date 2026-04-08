import pigpio
import time

# =========================
# Configuration
# =========================

SERVO_PIN = 13        # Change this to your GPIO pin
STEP_DEGREES = 45     # Movement step
PAUSE_SECONDS = 1     # Pause between moves


# =========================
# Helper functions
# =========================

def angle_to_pulsewidth(angle):
    """
    Convert angle (0–180) to servo pulse width in microseconds.
    Most servos expect 500–2500us.
    """
    return 500 + (angle / 180.0) * 2000


# =========================
# Main test
# =========================

def main():
    pi = pigpio.pi()

    if not pi.connected:
        print("Failed to connect to pigpio daemon.")
        return

    print("Starting servo test")

    try:

        # Move through angles
        for angle in range(0, 181, STEP_DEGREES):

            pulsewidth = angle_to_pulsewidth(angle)

            print(f"Moving to {angle} degrees")

            pi.set_servo_pulsewidth(SERVO_PIN, pulsewidth)

            time.sleep(PAUSE_SECONDS)

        time.sleep(2)

        for angle in range(0, 181, STEP_DEGREES):

            pulsewidth = angle_to_pulsewidth(angle)

            print(f"Moving to {angle} degrees")

            pi.set_servo_pulsewidth(SERVO_PIN, pulsewidth)

            time.sleep(PAUSE_SECONDS)


        print("Cycle complete. Idling servo.")

        # Disable servo pulses (prevents jitter and noise)
        pi.set_servo_pulsewidth(SERVO_PIN, 0)

    finally:

        time.sleep(1)
        pi.stop()
        print("Test finished")


if __name__ == "__main__":
    main()