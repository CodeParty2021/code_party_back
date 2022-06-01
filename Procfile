release: python manage.py makemigrations
release: python manage.py migrate
web: gunicorn code_party_back.wsgi
release: python manage.py loaddata post_initial.json
release: python manage.py loaddata event.json