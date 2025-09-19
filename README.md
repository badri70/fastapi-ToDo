# FastAPI ToDo

ToDo-приложение на FastAPI с поддержкой пользователей и Postgres.

## Быстрый старт

### 1. Клонируйте репозиторий

```bash
git clone https://github.com/badri70/fastapi-ToDo.git
cd fastapi-ToDo
```

### 2. Настройте переменные окружения

Отредактируйте файл `.env` при необходимости (по умолчанию уже настроен для docker-compose).

### 3. Запустите проект через Docker Compose

```bash
docker-compose up --build
```

- FastAPI будет доступен на [http://localhost:8000](http://localhost:8000)
- Postgres будет доступен на порту 5432

### 4. Документация API

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- Redoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Структура проекта

```
.
├── app/                # Основной код приложения
│   ├── tasks/          # Модуль задач
│   ├── users/          # Модуль пользователей
│   └── database.py     # Настройки базы данных
├── .env                # Переменные окружения
├── requirements.txt    # Python зависимости
├── Dockerfile          # Docker-образ приложения
├── docker-compose.yaml # Docker Compose конфигурация
└── README.md           # Этот файл
```

## Основные команды

- **Установка зависимостей локально:**  
  `pip install -r requirements.txt`

- **Миграции Alembic:**  
  `alembic upgrade head`

- **Запуск приложения локально:**  
  `uvicorn app.main:app --reload`

## Лицензия

MIT