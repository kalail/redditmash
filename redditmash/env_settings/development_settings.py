import os

DEBUG = False
TEMPLATE_DEBUG = DEBUG

import dj_database_url
DATABASES = {'default': dj_database_url.config(default='postgres://localhost')}

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