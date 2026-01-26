import socket #сетевое соеденение
import datetime
import os #работа с файломи
import re #используется для проверки логина(буквы + цыфры)

HOST = "127.0.0.1" #константы
PORT = 7777
FILES_DIR = "files" #откуда сервер будет отдавать HTML-файлы

users = {}  # login: password #хранилище пользователей,хранится на сервере

def now():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#SOCK_DGRAM - UDP скоросной протокол,не гарантирует доставку,использ в видео связи или игр. SOCK_STREAM -TCP гарантирует доставку, AF_INET -IPV4 ip адресс
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))  #привязываем сервер
server.listen()#определяет что мы будем ждать сервер,слушает подключение

print("Сервер запущен на порту", PORT) #старт нашего сервера

while True: #главный цыкл,работает пока мы его не остановим
    conn, addr = server.accept() #ждет клиента,когда клиен подключ
    print("Подключение от", addr)

    with conn: #контекстный менеджер,гарантир что соеден закроется коректно,даже при ошибки
        data = conn.recv(4096) #получаем данные от клиента,4096 сколько байт читаем за рар
        if not data:
            continue#если клиент ничего не прислал,ждем следующего

        text = data.decode(errors="ignore").strip()#преобраз байты в строку,убираем лишнии пробелы и перенос строки
        print("Получены данные:\n", text) #будем смотреть что нам реально пришло

        # =================================================
        # =================== HTTP ========================
        # =================================================
        if text.startswith("GET"): #браузер/иначе клиент
            first_line = text.splitlines()[0]
            path = first_line.split()[1]

            print("HTTP путь:", path)

            if path == "/favicon.ico": #браузер просит иконку,мы говорим ок но без содержимого
                conn.send(b"HTTP/1.1 204 No Content\r\n\r\n")
                continue

            body = ""

            if path == "/":
                body = "<h1>Главная страница</h1>"

            elif path.startswith("/test/"): #проверяем,путь,число,формируем ответ
                parts = path.strip("/").split("/")
                if len(parts) == 2 and parts[1].isdigit():
                    body = f"<h1>Тест с номером {parts[1]} запущен</h1>"
                else:
                    body = "<h1>Некорректный test</h1>"

            elif path.startswith("/message/"): #лигин,текст,выводим сообщение с датой
                parts = path.strip("/").split("/", 2)
                if len(parts) == 3:
                    login = parts[1]
                    message = parts[2]
                    body = f"<p>{now()} - сообщение от пользователя {login} - {message}</p>"
                    print(body)
                else:
                    body = "<h1>Некорректный message</h1>"

            elif path.endswith(".html"): #ищем файл в files,читаем и отдаем браузеру
                file_path = os.path.join(FILES_DIR, path.lstrip("/"))
                if os.path.exists(file_path):
                    with open(file_path, "r", encoding="utf-8") as f:
                        body = f.read()
                else:
                    body = "<h1>Файл не найден</h1>"

            else:
                body = f"<h1>Пришли неизвестные данные по HTTP - путь {path}</h1>"#сервер корректно сообщает нам об ошибке

            response = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/html; charset=utf-8\r\n" #отправка  HTML ответа,стату,заголовки,тело
                "\r\n"
                + body
            )

            conn.send(response.encode())#отправ браузеру

        # =================================================
        # =========== REG / SIGNIN (НЕ HTTP) ===============
        # =================================================
        #Если это не браузер,значит это клиент
        else:
            # ожидаем формат: command:reg; login:xxx; password:yyy
            parts = {}#словарь для разбора команд

            for item in text.split(";"):
                if ":" in item:
                    k, v = item.split(":", 1)
                    parts[k.strip()] = v.strip()

            command = parts.get("command")#достаем значение
            login = parts.get("login")
            password = parts.get("password")

            # -------- регистрация --------
            if command == "reg": #регистрация,провер логин,пароль,есть ли пользователь
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
            elif command == "signin": #проверяем есть ли логи и совпад ли пароль
                if login in users and users[login] == password:
                    response = f"{now()} - пользователь {login} произведен вход"
                else:
                    response = f"{now()} - ошибка входа {login} - неверный пароль/логин"

            else:
                response = f"Пришли неизвестные данные - {text}"

            conn.send(response.encode()) #ответ клиенту

 #веб-страница
# http://127.0.0.1:7777/index.html  #Index.html отлично работаетФайл успешно отдан сервером
 #http://127.0.0.1:7777/message/test123/hello/ время
 #http://127.0.0.1:7777/message/test123/hello/ тест с номером  запущен