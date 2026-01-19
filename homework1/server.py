"""
1. написать сервер на сокетах который может принимать 3 команды
    - time - отправляет обратно текущее время
    - rnd a:int b:int - отправляет обратно случайное число от а до b (пример - int 1 6)
    - stop - останавливает сервер - отправляет сообщение об этом
    - если прислана неизвестная  команда сообщить об этом клиенту

    * на сервере вести лог всех присланных команд в файл

"""
import socket
import datetime
import random
import logging

# ---------- логирование ----------
logging.basicConfig(
    filename="server.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

HOST = "0.0.0.0"
PORT = 9001


def handle_command(command: str) -> str:
    logging.info(f"Command received: {command}")

    parts = command.split()

    if command == "time":
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")#формат вреиени 2026.01.14и время 18:42 07 сек

    elif parts[0] == "rnd" and len(parts) == 3:
        try:
            a = int(parts[1])
            b = int(parts[2])
            return str(random.randint(a, b))
        except ValueError:
            return "Error: rnd command requires two integers"

    elif command == "stop":
        return "Server is stopping"

    else:
        return "Unknown command"


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, PORT))
        server.listen()

        print("Server started...")
        logging.info("Server started")

        while True:
            conn, addr = server.accept()
            with conn:
                print(f"Connected by {addr}")

                while True:
                    data = conn.recv(1024)
                    if not data:
                        break

                    command = data.decode().strip()
                    response = handle_command(command)
                    conn.sendall(response.encode())

                    if command == "stop":
                        print("Server stopped")
                        logging.info("Server stopped")
                        return


if __name__ == "__main__":
    main()