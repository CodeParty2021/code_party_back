from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"
    # https://firebase.google.com/docs/admin/setup?hl=ja#python
    # firebaseの初期化
