from .base import *

DEBUG = env.bool("DEBUG", default=False)
SECRET_KEY = env.str("SECRET_KEY")
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["*"])
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=["http://localhost:1337"])
CSRF_COOKIE_SECURE=env.bool("CSRF_COOKIE_SECURE", default=True)

try:
    from .local import *
except ImportError:
    pass
