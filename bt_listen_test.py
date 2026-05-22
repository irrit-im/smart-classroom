import serial

# Open the Bluetooth serial port
ser = serial.Serial('/dev/rfcomm0', 9600, timeout=1)

print("Listening on /dev/rfcomm0...")

try:
    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8', errors='ignore').strip()
            if data:
                print(data)

except KeyboardInterrupt:
    print("Exiting...")

finally:
    ser.close()

