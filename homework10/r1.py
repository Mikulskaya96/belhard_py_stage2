import requests

BASE_URL = "http://127.0.0.1:8000"


def show_all_users() -> None:
    """Запросить и вывести всех пользователей из API."""
    res = requests.get(f"{BASE_URL}/users")
    print("Status:", res.status_code)
    print("JSON:", res.json())


def create_test_users(count: int = 5) -> None:
    """Создать несколько тестовых пользователей через API."""
    for i in range(count):
        payload = {"name": f"user_{i}", "age": 33}
        res = requests.post(f"{BASE_URL}/users", params=payload)
        print(f"Created user_{i}: {res.status_code} -> {res.text}")


def main() -> None:
    print("Тестовый клиент для Homework10 API")
    print("1) Показать всех пользователей (/users)")
    print("2) Создать несколько тестовых пользователей")

    choice = input("Выбери действие (1/2): ").strip()

    if choice == "1":
        show_all_users()
    elif choice == "2":
        try:
            count_str = input("Сколько пользователей создать? [по умолчанию 5]: ").strip()
            count = int(count_str) if count_str else 5
        except ValueError:
            print("Некорректное число, будет использовано значение 5.")
            count = 5
        create_test_users(count)
    else:
        print("Неизвестный выбор. Ничего не делаем.")


if __name__ == "__main__":
    main()