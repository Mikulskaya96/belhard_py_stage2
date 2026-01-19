"""
2. написать клиент который запрашивает бесконечно команду для сервера
    и выводит в консоль ответ.
"""

import socket

HOST = "192.168.1.55"
PORT = 9001

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((HOST, PORT))
        print("Connected to server")

        while True:
            command = input("Enter command: ")
            client.sendall(command.encode())

            data = client.recv(1024)
            response = data.decode()
            print("Server:", response)

            if command == "stop":
                break


if __name__ == "__main__":
    main()