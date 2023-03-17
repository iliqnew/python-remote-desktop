import pickle
import socket
from threading import Thread
from PIL import Image


class Slave:
    def __init__(self) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.buffer = 409600
        self.connection = None

    def connect(self, address, username, password):
        print(f"Connecting to {address}...")
        self.socket.connect(address)
        print(f"Established connection with {address}")
        self.connection = True
        self.send()
        self.receive()

    def handle_connection(self, conn, address):
        receive_thread = Thread(target=self.receive, args=(conn, address))
        receive_thread.start()
        send_thread = Thread(target=self.send, args=(conn, address))
        send_thread.start()
        while self.connection:
            continue

    def receive(self):
        while True:
            image_bytes = b""
            while True:
                chunk = self.socket.recv(self.buffer)
                if b"', (" in chunk:
                    break
                image_bytes += chunk
            last_chunk, metadata = chunk.split(b"&&&^^^&&&")
            image_bytes += last_chunk
            mode, size = eval(metadata)
            data = [mode, size, image_bytes]
            self.process_data(data)
            if not data:
                break
        self.connection = False

    def send(self):
        screenshot = "pyautogui.screenshot()"
        self.socket.send(pickle.dumps(screenshot))

    def process_data(self, data):
        mode, size, image_bytes = data

        image = Image.frombytes(mode=mode, size=size, data=image_bytes)
        image.show()


if __name__ == "__main__":
    slave = Slave()
    slave.connect(("127.0.0.1", 5000), "root", "root")
