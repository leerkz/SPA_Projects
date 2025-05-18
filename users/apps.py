# flake8: noqa: F401
# или для игнора всех проверок в файле:
# flake8: noqa
from django.apps import AppConfig
class UsersConfig(AppConfig):

    default_auto_field = "django.db.models.BigAutoField"
    name = "users"

    def ready(self):
        import users.signals  # только импорт
