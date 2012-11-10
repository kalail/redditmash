import os

DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': 'dckre304j71813',
    'HOST': 'ec2-54-243-130-196.compute-1.amazonaws.com',
    'PORT': 5432,
    'USER': 'mxdalonyrhwvkh',
    'PASSWORD': 'quKP6Lg5xi4nt6RqDI5LKdD58E'
  }
}

# URL prefix for static files.
STATIC_URL = 'https://s3.amazonaws.com/redditmash_static/'



# Protected variables
SECRET_KEY = os.environ.get("SECRET_KEY")

# Redis
import urlparse
redis_url = urlparse.urlparse(os.environ.get('REDISTOGO_URL', 'redis://localhost'))
BROKER_URL = os.environ.get('REDISTOGO_URL')
CELERY_REDIS_HOST = redis_url.hostname
CELERY_REDIS_PORT = redis_url.port
CELERY_REDIS_DB = 0

# Set up Cache
os.environ['MEMCACHE_SERVERS'] = os.environ.get('MEMCACHIER_SERVERS', '')
os.environ['MEMCACHE_USERNAME'] = os.environ.get('MEMCACHIER_USERNAME', '')
os.environ['MEMCACHE_PASSWORD'] = os.environ.get('MEMCACHIER_PASSWORD', '')

CACHES = {
 	'default': {
		'BACKEND': 'django_pylibmc.memcached.PyLibMCCache',
		'LOCATION': os.environ.get('MEMCACHIER_SERVERS', ''),
		'TIMEOUT': 500,
		'BINARY': True,
	}
}


# Amazon S3 setting
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")