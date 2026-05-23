from RPLCD.i2c import CharLCD

lcd = CharLCD("PCF8574", 0x3F)
lcd.clear()

FIRST_LINE = "http://192.168.1"
SECOND_LINE = ".234:5000"

def lcd_display() -> None:
    lcd.write_string(f"{FIRST_LINE}\n\r{SECOND_LINE}")
