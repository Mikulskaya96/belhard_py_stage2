## Настройка проекта `belhard_py_stage2`

### 1. Виртуальное окружение (venv)

- Создание venv в корне проекта:

```bash
cd C:\Users\eliza\belhard_py_stage2
python -m venv .venv
```

- Активация в PowerShell (на одну сессию):

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

- Активация в cmd:

```cmd
.\.venv\Scripts\activate.bat
```

- Признак, что venv активен: в начале строки терминала видно `(.venv)`.

### 2. Установка зависимостей

- Основные пакеты для проектов:
  - Flask
  - Flask-SQLAlchemy
  - Flask-Migrate
  - requests
  - email-validator
  - urllib3

- Установка в активированном venv:

```bash
pip install -r homework8/requirements.txt
```

Или по отдельности:

```bash
pip install flask flask_sqlalchemy flask_migrate requests email-validator urllib3
```

### 3. Файл `requirements.txt`

- Сейчас находится в `homework8/requirements.txt`:

```text
Flask==2.3.2
Flask-SQLAlchemy==3.0.5
Flask-Migrate==4.0.4
email-validator==2.1.1
requests==2.31.0
urllib3==2.0.4
```

- При установке новой библиотеки в venv **нужно дописывать её сюда**, чтобы проект можно было легко развернуть на другом компьютере:

```bash
pip install <package>
```

и затем добавить `<package>`/`<package>==версия` в `requirements.txt`.

### 4. Обновление `requirements.txt` из venv

- После того как установила/удалила библиотеки в активированном venv, можно обновить файл:

```bash
pip freeze > requirements.txt
```

- Важно:
  - Команду запускать **только внутри нужного venv** (`(.venv)` видно в начале строки).
  - Она **перезапишет** `requirements.txt` полным списком пакетов и их версий из этого окружения.

### 5. Запуск приложений

- `homework4`:

```bash
cd C:\Users\eliza\belhard_py_stage2
(.venv) python homework4\main.py
```

- `homework8`:

```bash
cd C:\Users\eliza\belhard_py_stage2
(.venv) python homework8\app.py
```

- Остановка сервера во всех IDE/терминалах:
  - нажать `Ctrl + C` в том терминале, где запущен сервер (там, где видно `Running on http://127.0.0.1:...`).

### 5. IDE

- **PyCharm**:
  - Интерпретатор проекта: `C:\Users\eliza\belhard_py_stage2\.venv\Scripts\python.exe`.

- **Cursor / VS Code**:
  - Через `Python: Select Interpreter` выбран тот же путь к `.venv\Scripts\python.exe`.


#обновлять свой requirements.txt быстро

1. Открыть  терминал в папке проекта и включить  venv (если ещё не включён):

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1


2. Убедиться , что в начале строки есть (.venv).
pip freeze > requirements.txt


3. Открыть requirements.txt и посмотреть  — там теперь будет список моих установленных библиатек.