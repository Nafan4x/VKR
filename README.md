# Telegram Bot on Aiogram

Минимальный рабочий телеграм бот на aiogram с использованием SQLite, SQLAlchemy и callback data.

## 📋 Требования

- Python 3.12.10
- Телеграм бот токен

## Запуск проекта

1. Клонируйте репозиторий
```bash
git clone <your-repo-url>
cd <project-folder>
```
2. Создайте и активируйте виртуальное окружение
```bash
python -m venv venv

# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```
3. Установите зависимости
```bash
pip install -r requirements.txt
```
3. Создайте и заполните файл .env в корне проекта (пример .env.example)

4. Проведите миграции через alembic
```bash
alembic upgrade head
```


