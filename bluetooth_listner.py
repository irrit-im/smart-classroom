import bluetooth
import config

class BluetoothListener:

    def __init__(self, handler):

        self.handler = handler

        self.server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.server_sock.bind(("", config.BT_PORT))
        self.server_sock.listen(1)

        print("Waiting for bluetooth connection...")

        self.client_sock, address = self.server_sock.accept()
        print("Connected to", address)

    def listen(self):

        while True:
            data = self.client_sock.recv(1024).decode().strip()

            if data:
                print("Received:", data)
                self.handler(data)