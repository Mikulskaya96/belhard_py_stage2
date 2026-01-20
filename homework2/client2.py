import socket

HOST = "127.0.0.1"
PORT = 7777

while True:
    print("\n1 - Регистрация")
    print("2 - Вход")
    print("0 - Выход")

    choice = input("Выбор: ")

    if choice == "0":
        break

    login = input("Логин: ")
    password = input("Пароль: ")

    if choice == "1":
        msg = f"command:reg; login:{login}; password:{password}"
    elif choice == "2":
        msg = f"command:signin; login:{login}; password:{password}"
    else:
        continue

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((HOST, PORT))
        client.send(msg.encode())
        response = client.recv(4096).decode()
        print("Ответ сервера:", response)