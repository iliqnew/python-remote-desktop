import pyautogui
import socket
import threading


class Communication:
    def __init__(self) -> None:
        self.to_receive = []
        self.to_send = []

    def main(self):
        pass


class Slave:
    def __init__(self) -> None:
        pass


def handle(client, address):
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            print(f"Client {str(address)} says {message}")
        except Exception:
            print(f"Client {address} disconnected")
            client.close()
            pass


def receive(server):
    conn, address = server.accept()
    print(f"Connected with {address}!")
    conn.send("Connected to the server".encode("utf-8"))
    thread = threading.Thread(target=handle, args=(conn, address))
    thread.start()


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", 5000))
    server.listen(1)
    print("Server running...")
    receive(server)


if __name__ == "__main__":
    main()
