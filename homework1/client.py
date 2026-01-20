"""
2. написать клиент который запрашивает бесконечно команду для сервера
    и выводит в консоль ответ.
"""

import socket

HOST = "127.0.0.1"
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

print("Подключено к серверу")

while True:
    command = input("Введите команду: ")

    client.send(command.encode())
    response = client.recv(1024).decode()
    print("Ответ сервера:", response)

    if command == "stop":
        break

client.close()
print("Соединение закрыто")