import os
from .settings import * 
import dj_database_url

SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = False
# ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')
USE_PROD = os.environ.get('USE_PROD', 'False') == 'True'



# db

DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL')
    )
}

# SECURITY SETTINGS
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# STATIC FILES (for Whitenoise)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Whitenoise Storage
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# MIDDLEWARE 
MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
] + MIDDLEWARE 

# LOGGING
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
