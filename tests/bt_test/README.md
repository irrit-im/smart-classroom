## 1. Creating the Bluetooth connection
Run: `sudo rfcomm connect hci0 98:D3:71:F6:B2:4A` and keep the terminal running (open a new terminal to run commands).

OR:

Run: `sudo rfcomm bind 0 98:D3:71:F6:B2:4A`

## 2. Running the test:

**Python test:**\
Run: `python3 tests/bt_test/bt_listen.py`

**Directly read the data stream from a Bluetooth virtual serial port to the terminal:**\
Run: `cat /dev/rfcomm0`