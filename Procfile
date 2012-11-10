web: python manage.py runserver
worker: python manage.py celery worker -E -B --loglevel=INFO
monitor: python manage.py celery flower --broker=redis://localhost:6379/0