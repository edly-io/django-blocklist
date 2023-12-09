from typing import Dict, Any

ALLOWED_HOSTS = ["localhost"]
BLOCKLIST_CONFIG: Dict[str, Any] = {}
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": "db.sqlite3"}}
INSTALLED_APPS = ["django_blocklist"]
MIDDLEWARE = ["django_blocklist.middleware.BlocklistMiddleware"]
ROOT_URLCONF = "urls"
USE_TZ = True
