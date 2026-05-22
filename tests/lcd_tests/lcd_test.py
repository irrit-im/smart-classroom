from RPLCD.i2c import CharLCD
import time

print("Initializing LCD...")

lcd = CharLCD('PCF8574', 0x3f)

print("LCD initialized.")

lcd.clear()

lcd.write_string("LCD Test\nHello World")

print("Message written.")

time.sleep(5)

lcd.clear()

print("Done.")