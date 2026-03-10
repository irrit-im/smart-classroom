from picamera2 import Picamera2
import time

# Initialize camera
picam2 = Picamera2()

# Configure for still capture
picam2.configure(picam2.create_still_configuration())

# Start camera
picam2.start()

# Give the camera time to warm up
time.sleep(2)

# Take photo
picam2.capture_file("image.jpg")

# Stop camera
picam2.stop()

print("Photo saved as image.jpg")
