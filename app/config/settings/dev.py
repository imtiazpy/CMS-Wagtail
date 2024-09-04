from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", default=True)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str("SECRET_KEY")

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["*"])


try:
    from .local import *
except ImportError:
    pass
