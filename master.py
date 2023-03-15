import pickle
import socket
from threading import Thread

import pyautogui


class Master:
    def __init__(self) -> None:
        self.profiles = [{"username": "root", "password": "root"}]
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(("localhost", 5000))
        self.buffer = 1024
        self.connection = None

    def listen(self):
        while True:
            self.socket.listen(1)
            print("Listening...")
            conn, address = self.socket.accept()
            print(f"Connection from {address}!")
            self.connection = True
            self.handle_connection(conn, address)
            print(f"Lost connection with {address}")

    def handle_connection(self, conn, address):
        receive_thread = Thread(target=self.receive, args=(conn, address))
        receive_thread.start()
        send_thread = Thread(target=self.send, args=(conn, address))
        send_thread.start()
        while self.connection:
            continue

    def receive(self, conn, address):
        while True:
            raw_payload = conn.recv(self.buffer)
            if not raw_payload:
                break
            payload = pickle.loads(raw_payload)
            self.process_data(payload)
        self.connection = False

    def send(self, conn, address):
        screenshot = pyautogui.screenshot()
        conn.send(pickle.dumps(screenshot))

    def process_data(self, data):
        print(data)


if __name__ == "__main__":
    master = Master()
    master.listen()
