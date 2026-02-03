import re
from flask import Flask, render_template, request, redirect, session
import requests
API_KEY = "60fb59c0a5dfacd337bf083de9286859" #ключ погода
app = Flask(__name__)
app.secret_key = "secret123"

users = {}

#Маршрут
@app.route("/")
def index():
    user = session.get("user")
    return render_template("index.html", user=user)

@app.route("/duck/")
def duck():
    response = requests.get("https://random-d.uk/api/random")
    data = response.json()

    image_url = data["url"]

    return render_template(
        "duck.html",
        image_url=image_url
    )

def get_foxes(count):
    fox_images = []

    for _ in range(count):
        try:
            response = requests.get(
                "https://randomfox.ca/floof/",
                timeout=3
            )
            data = response.json()
            fox_images.append(data["image"])
        except requests.exceptions.RequestException:
            pass  # если API не ответил — просто пропускаем

    return fox_images


@app.route("/fox/")
def fox_4():
    fox_images = get_foxes(4)
    return render_template("fox.html", fox_images=fox_images, count=4)


@app.route("/fox/10/")
def fox_10():
    fox_images = get_foxes(10)
    return render_template("fox.html", fox_images=fox_images, count=10)


@app.route("/kurama/")
def kurama():
    # Прямая ссылка на  Кураму
    kurama_image = "https://wallpapercave.com/wp/wp10475421.jpg"
    return render_template("kurama.html", kurama_image=kurama_image)




@app.route("/weather-minsk/")
def weather_minsk():
    city = "Minsk"
    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={API_KEY}&units=metric&lang=ru"
    )

    data = requests.get(url).json()

    weather = {
        "city": data["name"],
        "temp": data["main"]["temp"],
        "feels": data["main"]["feels_like"],
        "description": data["weather"][0]["description"],
        "icon": data["weather"][0]["icon"]
    }
    return render_template("weather.html", weather=weather)


@app.route("/weather/<city>/")
def weather_city(city):
    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={API_KEY}&units=metric&lang=ru"
    )

    data = requests.get(url).json()

    if data.get("cod") != 200:
        return f"Город «{city}» не найден "

    weather = {
        "city": data["name"],
        "temp": data["main"]["temp"],
        "feels": data["main"]["feels_like"],
        "description": data["weather"][0]["description"],
        "icon": data["weather"][0]["icon"]
    }
    return render_template("weather.html", weather=weather)





#Регистрация пользователя(register)
@app.route("/register/", methods=["GET", "POST"])
def register():
    error = ""
    success = ""

    if request.method == "POST":
        login = request.form.get("login")
        password = request.form.get("password")

        # проверка логина
        if not re.match(r'^[a-zA-Z0-9_]{6,20}$', login):
            error = "Логин: 6–20 символов, латиница, цифры и _"

        # проверка пароля
        elif not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,15}$', password):
            error = "Пароль: 8–15 символов, заглавная, строчная буква и цифра"

        elif login in users:
            error = "Пользователь уже существует"

        else:
            users[login] = password
            session["user"] = login
            return redirect("/")   #

    return render_template("register.html", error=error)


# Вход пользователя(login)
@app.route("/login/", methods=["GET", "POST"])
def login():
    error = ""

    if request.method == "POST":
        login = request.form.get("login")
        password = request.form.get("password")

        if login not in users:
            error = "Пользователь не найден"
        elif users[login] != password:
            error = "Неверный пароль"
        else:
            session["user"] = login
            return redirect("/")

    return render_template("login.html", error=error)


@app.route("/logout/")
def logout():
    session.pop("user", None)
    return redirect("/login/")


@app.before_request
def check_login():
    allowed_routes = ["login", "register", "static"]

    if request.endpoint is None:
        return

    if "user" not in session and request.endpoint not in allowed_routes:
        return redirect("/login/")


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)