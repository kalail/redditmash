web: python manage.py run_gunicorn --workers=9 --bind=0.0.0.0:$PORT
worker: python manage.py celery worker --concurrency=10 -E -B --loglevel=INFO
monitor: python manage.py celery flower --broker=redis://localhost