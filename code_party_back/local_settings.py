
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

DEBUG = True

SECRET_KEY = "django-insecure-#xy3cwt55whodjw2s+xnz%xk6tu-09#ax8!44z)3e1@8c1hhn&"

ALLOWED_HOSTS = ['*']

# ローカルでPostgreSQLをテストしたい場合，以下のコメントアウトを外す
# import dj_database_url
# db_from_env = dj_database_url.config()
# DATABASES = {
#     'default' : dj_database_url.config()
# }