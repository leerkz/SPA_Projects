# SPA_Project_

## Описание проекта

Данный проект — это современное Django-приложение с использованием Celery для фоновых задач, PostgreSQL как основной СУБД, Redis для брокера сообщений и Nginx в роли обратного прокси-сервера. Проект упакован для развертывания с помощью Docker и docker-compose, что упрощает запуск как локально, так и на удалённом сервере.

---

## Стек технологий

- **Python 3.12**
- **Django** (бэкенд, REST API)
- **PostgreSQL** (база данных)
- **Redis** (брокер для Celery)
- **Celery + celery-beat** (фоновая обработка задач и периодические задачи)
- **Nginx** (обратный прокси и раздача статики)
- **Docker, docker-compose** (контейнеризация)
- **Gunicorn** (WSGI сервер)
- **drf_yasg** (Swagger/OpenAPI для API-документации)
- **SimpleJWT** (аутентификация через JWT)

---

## Ссылки

- **Продакшен-сервер с развернутым приложением:**  
  http://YOUR_SERVER_IP_OR_DOMAIN

*(Замените на фактический адрес)*

---

## Быстрый старт (локально)

### 1. Клонирование репозитория

```bash
git clone https://github.com/your-username/SPA_Project_.git
cd SPA_Project_
```

### 2. Создание и настройка `.env`

Создайте файл `.env` в корневой директории со следующим содержимым (пример):

```ini
DJANGO_SECRET_KEY=your_secret_key
POSTGRES_DB=your_db
POSTGRES_USER=pg_user
POSTGRES_PASSWORD=pg_password
POSTGRES_HOST=db
POSTGRES_PORT=5432
REDIS_HOST=redis
REDIS_PORT=6379
STRIPE_SECRET_KEY=your_stripe_key
```

### 3. Запуск при помощи Docker Compose

```bash
docker-compose up --build
```

*Будут подняты сервисы: web (Django), nginx, db (Postgres), redis, celery, celery-beat.*

### 4. Применить миграции и создать суперпользователя

В новом терминале (после запуска контейнеров):

```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

### 5. Доступ

- Приложение: [http://localhost](http://localhost)
- Django admin: [http://localhost/admin](http://localhost/admin)
- Документация Swagger: [http://localhost/swagger/](http://localhost/swagger/) *(если настроено)*

---

## Развертывание на удалённом сервере (Ubuntu-based)

### 1. Подготовьте сервер

- Рекомендуется VPS на Ubuntu 20.04+/22.04+, минимум 2ГБ RAM
- Обновите систему:  
  ```bash
  sudo apt update && sudo apt upgrade -y
  ```
- Установите Docker и Docker Compose:  
  ```bash
  sudo apt install docker.io docker-compose -y
  ```

### 2. Клонируйте проект и настройте `.env`

Повторите шаги 1 и 2 из локальной инструкции.
Обеспечьте сохранность секретных ключей и используйте сложные пароли.

### 3. Настройка Firewall (опционально)

```bash
sudo ufw allow 'Nginx Full'
sudo ufw allow OpenSSH
sudo ufw enable
```

### 4. Запуск приложения

```bash
docker-compose up --build -d
```

### 5. Проверка

- Приложение и админка будут доступны по вашему публичному IP или домену.
- Пример: `http://your-server-ip` или `http://your-domain.com`

---

## CI/CD (Пример для GitHub Actions)

Используйте следующий шаблон `.github/workflows/deploy.yml` для автоматического деплоя на сервер:

```yaml
name: Deploy to VPS

on:
  push:
    branches: [main, master, dev]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Copy files to server
        uses: appleboy/scp-action@master
        with:
          host: ${{ secrets.SERVER_IP }}
          username: ${{ secrets.SERVER_USER }}
          key: ${{ secrets.SERVER_SSH_KEY }}
          source: "."
          target: "/home/${{ secrets.SERVER_USER }}/SPA_Project_"
      - name: Run deploy script via SSH
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.SERVER_IP }}
          username: ${{ secrets.SERVER_USER }}
          key: ${{ secrets.SERVER_SSH_KEY }}
          script: |
            cd SPA_Project_
            docker-compose down
            docker-compose pull
            docker-compose up --build -d
```

- **SECRET переменные:**  
  Заполните в настройках репозитория GitHub (`Settings > Secrets and variables > Actions`).

---

## Ручные полезные команды

- **Миграции:**  
  `docker-compose exec web python manage.py migrate`
- **Суперпользователь:**  
  `docker-compose exec web python manage.py createsuperuser`
- **Просмотр логов:**  
  `docker-compose logs -f`
- **Перезапуск сервиса:**  
  `docker-compose restart <service>`

---

## Структура проекта (основное)

- `config/` – настройки Django
- `users/` – пользовательские модели и логика
- `materials/` – бизнес-логика материалов
- `nginx/` – конфиги Nginx
- `Dockerfile`, `docker-compose.yml` – инфраструктура/деплой

---

## Контакты

Если возникли проблемы, обратитесь к maintainer:  
**your.email@example.com**


---

**P.S.**  
Замените `YOUR_SERVER_IP_OR_DOMAIN` на фактический адрес сервера.