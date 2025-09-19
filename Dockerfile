FROM python:3.12-slim

# Установка зависимостей
WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Копируем проект
COPY . /app

# Переменные окружения (опционально)
ENV PYTHONUNBUFFERED=1

# Запуск приложения
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]