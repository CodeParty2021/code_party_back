release: python manage.py makemigrations
release: python manage.py migrate
release: python manage.py loaddata post_initial.json
web: gunicorn code_party_back.wsgi