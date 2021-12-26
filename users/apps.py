from django.apps import AppConfig
from firebase_admin import credentials
import firebase_admin


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"
    # https://firebase.google.com/docs/admin/setup?hl=ja#python
    # firebaseの初期化
    cred = credentials.Certificate("firebaseKeys.json")
    firebase_admin.initialize_app(cred)
