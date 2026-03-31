# belhard_py_stage2

Student Python coursework (Belhard): **Flask** apps with Jinja2 templates, external HTTP APIs, and sessions; a **quiz** mini-project using **Flask + SQLAlchemy + Flask-Migrate**; and a separate **REST API** built with **FastAPI** (`homework10`).

## Stack

Flask, FastAPI, SQLAlchemy, Pydantic, uvicorn, requests, python-dotenv.

## Run (example: quizzes — `homework8`)

**Windows (PowerShell):**

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
cd homework8
python app.py
```

**Linux / macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd homework8
python app.py
```

Default URL: `http://127.0.0.1:5001/`

## Environment variables

Weather features in **homework3** and **homework4** need an OpenWeather key:

- `OPENWEATHER_API_KEY` — create a key at [openweathermap.org/api](https://openweathermap.org/api).

**homework4** (signed session cookies):

- `SECRET_KEY` — use a long random string in production. For local runs you can omit it; a dev-only fallback is used.

Copy `.env.example` to `.env` in the **repository root**, fill in values (`.env` is gitignored). For **homework3** and **homework4**, variables from that file are loaded automatically via `python-dotenv`. You can still override them with real environment variables or your IDE run configuration.

## Project layout

- `homework3`, `homework4` — Flask demos (ducks, foxes, weather, currency converter, etc.).
- `homework10` — FastAPI: from the `homework10` folder run `python main.py` (or uvicorn as described in `README_hw10.md`).

---

## Кратко по-русски

Учебный репозиторий: Flask (шаблоны, API, сессии), квизы на Flask + SQLAlchemy + миграции, отдельно API на FastAPI. Запуск квизов: см. блок **Run** выше. Скопируйте `.env.example` в `.env` в корне репозитория и заполните ключи; для homework3/homework4 файл подхватывается автоматически.
