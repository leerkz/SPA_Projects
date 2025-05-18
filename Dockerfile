
# Используем официальный образ Python
FROM python:3.12-slim

# Устанавливаем переменные окружения

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Устанавливаем зависимости системы
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Создаем и переходим в рабочую директорию
WORKDIR /code

# Копируем и устанавливаем зависимости Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем проект
COPY . .

# Команда запуска (может быть переопределена в docker-compose)
EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
