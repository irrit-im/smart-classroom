from RPLCD.i2c import CharLCD
import subprocess
import socket
import threading
import time


class LCDController:

    def __init__(self):

        self.lcd = CharLCD('PCF8574', 0x3f)

        self.running = False

    def get_ssid(self):

        try:
            ssid = subprocess.check_output(
                ["iwgetid", "-r"],
                stderr=subprocess.DEVNULL
            )

            return ssid.decode().strip()

        except subprocess.CalledProcessError:
            return "No WiFi"

    def get_ip(self):

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            s.connect(("8.8.8.8", 80))

            ip = s.getsockname()[0]

            s.close()

            return ip

        except:
            return "No IP"

    def update_display(self):

        ssid = self.get_ssid()
        ip = self.get_ip()

        message = f"{ssid[:16]}\n{ip[:16]}"

        try:
            self.lcd.clear()
            self.lcd.write_string(message)

        except OSError:
            pass

    def loop(self):

        while self.running:

            self.update_display()

            time.sleep(5)

    def start(self):

        self.running = True

        thread = threading.Thread(target=self.loop, daemon=True)

        thread.start()

    def stop(self):

        self.running = False

        self.lcd.clear()