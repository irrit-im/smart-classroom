import serial

ser = serial.Serial("/dev/rfcomm0")

while True:
    print(ser.readline().decode(errors="ignore").strip())
