import socket
import datetime
import os
import re

HOST = "127.0.0.1"
PORT = 7777
FILES_DIR = "files"

users = {}  # login: password

def now():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print("Сервер запущен на порту", PORT)

while True:
    conn, addr = server.accept()
    print("Подключение от", addr)

    with conn:
        data = conn.recv(4096)
        if not data:
            continue

        text = data.decode(errors="ignore").strip()
        print("Получены данные:\n", text)

        # =================================================
        # =================== HTTP ========================
        # =================================================
        if text.startswith("GET"):
            first_line = text.splitlines()[0]
            path = first_line.split()[1]

            print("HTTP путь:", path)

            if path == "/favicon.ico":
                conn.send(b"HTTP/1.1 204 No Content\r\n\r\n")
                continue

            body = ""

            if path == "/":
                body = "<h1>Главная страница</h1>"

            elif path.startswith("/test/"):
                parts = path.strip("/").split("/")
                if len(parts) == 2 and parts[1].isdigit():
                    body = f"<h1>Тест с номером {parts[1]} запущен</h1>"
                else:
                    body = "<h1>Некорректный test</h1>"

            elif path.startswith("/message/"):
                parts = path.strip("/").split("/", 2)
                if len(parts) == 3:
                    login = parts[1]
                    message = parts[2]
                    body = f"<p>{now()} - сообщение от пользователя {login} - {message}</p>"
                    print(body)
                else:
                    body = "<h1>Некорректный message</h1>"

            elif path.endswith(".html"):
                file_path = os.path.join(FILES_DIR, path.lstrip("/"))
                if os.path.exists(file_path):
                    with open(file_path, "r", encoding="utf-8") as f:
                        body = f.read()
                else:
                    body = "<h1>Файл не найден</h1>"

            else:
                body = f"<h1>Пришли неизвестные данные по HTTP - путь {path}</h1>"

            response = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/html; charset=utf-8\r\n"
                "\r\n"
                + body
            )

            conn.send(response.encode())

        # =================================================
        # =========== REG / SIGNIN (НЕ HTTP) ===============
        # =================================================
        else:
            # ожидаем формат: command:reg; login:xxx; password:yyy
            parts = {}
            for item in text.split(";"):
                if ":" in item:
                    k, v = item.split(":", 1)
                    parts[k.strip()] = v.strip()

            command = parts.get("command")
            login = parts.get("login")
            password = parts.get("password")

            # -------- регистрация --------
            if command == "reg":
                if not login or not password:
                    response = f"{now()} - ошибка регистрации - пустые данные"

                elif not re.fullmatch(r"[A-Za-z0-9]{6,}", login):
                    response = f"{now()} - ошибка регистрации {login} - неверный логин"

                elif len(password) < 8 or not any(c.isdigit() for c in password):
                    response = f"{now()} - ошибка регистрации {login} - неверный пароль"

                elif login in users:
                    response = f"{now()} - ошибка регистрации {login} - пользователь уже существует"

                else:
                    users[login] = password
                    response = f"{now()} - пользователь {login} зарегистрирован"

            # -------- вход --------
            elif command == "signin":
                if login in users and users[login] == password:
                    response = f"{now()} - пользователь {login} произведен вход"
                else:
                    response = f"{now()} - ошибка входа {login} - неверный пароль/логин"

            else:
                response = f"Пришли неизвестные данные - {text}"

            conn.send(response.encode())