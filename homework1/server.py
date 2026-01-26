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

HOST = "127.0.0.1"
PORT = 5000

# ---- настройка логгера ----
logging.basicConfig(
    filename="server.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)
#SOCK_DGRAM - UDP скоросной протокол,не гарантирует доставку,использ в видео связи или игр. SOCK_STREAM -TCP гарантирует доставку, AF_INET -IPV4 ip адресс
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()#определяет что мы будем ждать сервер

logger.info("Сервер запущен")
print("Сервер запущен...")

running = True

while running:
    conn, addr = server.accept()
    logger.info(f"Подключен клиент {addr}")
    print("Подключен клиент:", addr)

    with conn:
        while True:
            data = conn.recv(1024).decode().strip()
            if not data:
                break

            logger.info(f"Получена команда: {data}")
            parts = data.split()

            # ---- команды ----
            if parts[0] == "time":
                response = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            elif parts[0] == "rnd" and len(parts) == 3:
                try:
                    a = int(parts[1])
                    b = int(parts[2])
                    response = str(random.randint(a, b))
                except ValueError:
                    response = "Ошибка: a и b должны быть числами"
                    logger.warning("Ошибка преобразования a и b в int")

            elif parts[0] == "stop":
                response = "Сервер остановлен"
                conn.send(response.encode())
                logger.warning("Сервер остановлен командой stop")
                running = False
                break

            else:
                response = "Неизвестная команда"
                logger.warning(f"Неизвестная команда: {data}")

            conn.send(response.encode())

server.close()
logger.info("Сервер выключен")
print("Сервер выключен")