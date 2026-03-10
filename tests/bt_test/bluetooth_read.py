import serial # pip install pyserial

ser = serial.Serial(
    port="/dev/rfcomm0",
    baudrate=9600,
    timeout=1
)

def take_photo():
    print("photo taken")

while True:
    line = ser.readline().decode().strip()
    if line == "photo":
	    take_photo()
    else:
        print("Received:", line)
