import serial
from typing import Optional
import config

class BTListener:
    def __init__(
        self,
        port: str = config.BT_PORT,
        on_msg: callable = None,
    ):
        self.port = port
        self.on_msg = on_msg

    def connect(self):
        """Open the Bluetooth serial connection."""
        self.ser = serial.Serial(self.port)

    def disconnect(self):
        """Close the Bluetooth serial connection."""
        if self.ser and self.ser.is_open:
            self.ser.close()

    def read_line(self) -> Optional[str]:
        """
        Read one line from the Bluetooth connection.
        Returns None if no data was received.
        """
        if not self.ser or not self.ser.is_open:
            raise RuntimeError("Bluetooth serial connection is not open.")

        data = self.ser.readline()

        if not data:
            return None

        return data.decode(errors="ignore").strip()

    def listen_forever(self):
        """Continuously print incoming Bluetooth messages."""
        try:
            while True:
                line = self.read_line()

                if line:
                    print(line)
                    if self.on_msg:
                        self.on_msg(line)

        except KeyboardInterrupt:
            print("\nStopping listener...")

        finally:
            self.disconnect()


if __name__ == "__main__":
    listener = BTListener()

    listener.connect()

    print("Listening for Bluetooth data...\n")

    listener.listen_forever()
