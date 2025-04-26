import os
from .settings import * 


SECRET_KEY = os.environ.get('SECRET_KEY')


# STATIC FILES (for Whitenoise)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Whitenoise Storage
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
