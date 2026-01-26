
"""
Написать веб-приложение на Flask со следующими ендпоинтами:
    - главная страница - содержит ссылки на все остальные страницы
    - /duck/ - отображает заголовок "рандомная утка №ххх" и картинка утки
                которую получает по API https://random-d.uk/api/random

    - /fox/<int>/ - аналогично утке только с лисой (- https://randomfox.ca),
                    но количество разных картинок определено int.
                    если int больше 10 или меньше 1 - вывести сообщение
                    что можно только от 1 до 10

    - /weather-minsk/ - показывает погоду в минске в красивом формате

    - /weather/<city>/ - показывает погоду в городе указанного в city
                    если такого города нет - написать об этом

    - по желанию добавить еще один ендпоинт на любую тему

Добавить обработчик ошибки 404. (есть в example)
"""
"""
1. Написать веб-приложение на Flask со следующими ендпоинтами:
    - главная страница - содержит ссылки на все остальные страницы
    - /duck/ - отображает заголовок "рандомная утка №ххх" и картинка утки
                которую получает по API https://random-d.uk/api/random
"""

from flask import Flask, render_template
import requests
API_KEY = "60fb59c0a5dfacd337bf083de9286859" #ключ погода
app = Flask(__name__)

#1
@app.route("/")
def index():
    return render_template("index.html") #главная страница - содержит ссылки на все остальные страницы


@app.route("/duck/")
def duck():
    response = requests.get("https://random-d.uk/api/random")
    data = response.json()

    image_url = data["url"]

    return render_template(
        "duck.html",
        image_url=image_url
    )


"""
2. - /fox/<int>/ - аналогично утке только с лисой (- https://randomfox.ca),
                    но количество разных картинок определено int.
                    если int больше 10 или меньше 1 - вывести сообщение
                    что можно только от 1 до 10
"""
#2
@app.route("/fox/")
def fox():
    url = "https://randomfox.ca/floof/"
    response = requests.get(url)
    data = response.json()

    fox_image = data["image"]

    return render_template("fox.html", fox_image=fox_image)

"""
3. - по желанию добавить еще один ендпоинт на любую тему
"""
# @app.route("/kurama/")
# def kurama():
#     # Прямая ссылка на  Кураму
#     kurama_image = "https://images.fineartamerica.com/images/artworkimages/mediumlarge/3/kurama-y-naruto-andres-montanez.jpg"
#     return render_template("kurama.html", kurama_image=kurama_image)

@app.route("/kurama/")
def kurama():
    # Прямая ссылка на  Кураму
    kurama_image = "https://wallpapercave.com/wp/wp10475421.jpg"
    return render_template("kurama.html", kurama_image=kurama_image)


"""
4.  - /weather-minsk/ - показывает погоду в минске в красивом формате

    - /weather/<city>/ - показывает погоду в городе указанного в city
                    если такого города нет - написать об этом
"""
#4.

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


#другой город
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


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404

if __name__ == "__main__":
    app.run(debug=True)