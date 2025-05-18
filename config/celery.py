import os

from celery import Celery

# Указываем Django настройки
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")

# Чтение настроек из Django settings с префиксом CELERY
app.config_from_object("django.conf:settings", namespace="CELERY")

# Автоматическое обнаружение тасков во всех приложениях
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")


CELERY_TIMEZONE = "Europe/Moscow"
