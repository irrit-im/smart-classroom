# Smart Classroom

This project runs on a **Raspberry Pi 3B** with **Raspberry Pi OS (64-bit)**.

The system captures images of a classroom board using a Raspberry Pi camera mounted on a **servo gimbal**, and provides:

- Bluetooth control
- Image capture
- Image storage
- Live camera view through a Flask website

---

# Hardware

Required hardware:

- Raspberry Pi 3B
- Raspberry Pi Camera Module v1.3 (5MP)
- 2 Servo motors
- LCD screen (I2C interface)
- Bluetooth controller device (external system)

---

# Project Features

The system supports:

• Capturing board images via Bluetooth command  
• Saving images locally  
• Viewing saved images through a Flask website  
• Live camera preview in the browser  
• Servo motor control via Bluetooth  

---

# Setup

## 1. Update the system

```bash
sudo apt update
sudo apt upgrade
```

## 2. Enable the Raspberry Pi camera

```bash
sudo raspi-config
```

Navigate to:

```
Interface Options → Camera → Enable
```

Reboot:

```bash
sudo reboot
```

## 3. Install required system packages (apt)

These provide camera, OpenCV, and Bluetooth support.

```bash
sudo apt install \
python3-picamera2 \
python3-libcamera \
python3-opencv \
python3-bluez \
bluetooth \
bluez \
libbluetooth-dev \
libcap-dev
```

sudo apt install pigpio-tools python3-pigpio
Start the daemon:
sudo systemctl start pigpiod
sudo systemctl enable pigpiod

## 4. Enable the Bluetooth service

```bash
sudo systemctl enable bluetooth
sudo systemctl start bluetooth
```

## 5. Create and activate a Python virtual environment

The virtual environment must allow access to system packages so it can use the Raspberry Pi hardware libraries.

```bash
python3 -m venv venv --system-site-packages
```

Activate the environment:

```bash
source venv/bin/activate
```

## 6. Install Python packages

Install the pip dependencies listed in `requirements.txt`.

```bash
pip install -r requirements.txt
```

## 7. Configuration

Hardware settings such as GPIO pins, image directory, and camera resolution are defined in:

```
config.py
```

Adjust values in this file if the hardware configuration changes.
