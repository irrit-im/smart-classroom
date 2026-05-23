from RPLCD.i2c import CharLCD
import subprocess
from time import sleep

lcd = CharLCD('PCF8574', 0x3f)
lcd.clear()

def get_ssid():
	try:
		ssid = subprocess.check_output(["iwgetid", "-r"], stderr=subprocess.DEVNULL)
		return ssid.decode().strip()
	except subprocess.CalledProcessError:
		return None


def update_lcd(ssid):
	msg = f'Connected:\n\r{ssid}' if ssid else 'Not connected'
	try:
		lcd.clear()
		lcd.write_string(msg)
	except OSError:
		pass

while True:
	ssid = get_ssid()
	update_lcd(ssid)
	sleep(2)

