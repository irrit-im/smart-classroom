
import serial

ser = serial.Serial("/dev/rfcomm0")

while True:
    command = ser.readline().decode(errors="ignore").strip()
    print(command)
    if command != "photo":
        cords = command.split(",")
        x = int(cords[0])
        y = (cords[1])
        print(f"X is {x} and Y is {y}")
        print(cords)
