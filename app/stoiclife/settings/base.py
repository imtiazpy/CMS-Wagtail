"""
Django settings for stoiclife project.

Generated by 'django-admin startproject' using Django 5.0.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import environ

env = environ.Env()

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/


# Application definition

INSTALLED_APPS = [
    "wagtail.locales",
    "wagtail.contrib.simple_translation",
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail",
    "wagtail.contrib.settings",
    "modelcluster",
    "taggit",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]


LOCAL_APPS = [
    "home",
    "search",
    "menus",
    "streams",
    "news",
    "site_settings",
    "contact",
    "resume",
    "core",
    "language_switcher",
]

THIRD_PARTY_APPS = [
    "fontawesomefree",
    "django_recaptcha",
    "wagtailcaptcha",
]


INSTALLED_APPS += LOCAL_APPS + THIRD_PARTY_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
]

ROOT_URLCONF = "stoiclife.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(PROJECT_DIR, "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "wagtail.contrib.settings.context_processors.settings",
                "django.template.context_processors.i18n",
            ],
        },
    },
]

WSGI_APPLICATION = "stoiclife.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

if env.str('DATABASE_URL', ''):
    DATABASES = {
        'default': {**env.db(), **{'ENGINE': 'django.db.backends.postgresql'}}
    }
elif env.str('DATABASE', ""):
    DATABASES = {
        "default": {
            "ENGINE": env.str("DB_ENGINE"),
            "NAME": env.str("DB_NAME"),
            "USER": env.str("DB_USER"),
            "PASSWORD": env.str("DB_PASSWORD", "password"),
            "HOST": env.str("DB_HOST", "localhost"),
            "PORT": env.str("DB_PORT", "5432"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        }
    }


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True
WAGTAIL_I18N_ENABLED = True

USE_L10N = True

USE_TZ = True

# available languages: English, German
WAGTAIL_CONTENT_LANGUAGES = LANGUAGES = [
    ('en', "English"),
    ('de', "German")
]

WAGTAIL_CONTENT_LANGUAGES_FALLBACK = {
    'default': 'en',
}


WAGTAILEMBEDS_FINDERS = [
    {
        'class': 'streams.finders.YouTubePreserveRelFinder',
    },
    {
        'class': 'wagtail.embeds.finders.oembed',
    }
]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/


# AWS S3 Bucket Settings
USE_S3 = env.bool("USE_S3", default=False)

if USE_S3:
    # AWS Settings
    AWS_STORAGE_REGION = env.str("AWS_STORAGE_REGION", "")
    AWS_ACCESS_KEY_ID = env.str("AWS_ACCESS_KEY_ID", "")
    AWS_SECRET_ACCESS_KEY = env.str("AWS_SECRET_ACCESS_KEY", "")
    AWS_STORAGE_BUCKET_NAME = env.str("AWS_STORAGE_BUCKET_NAME", "")
    AWS_DEFAULT_ACL = env.str("AWS_DEFAULT_ACL", "public-read")
    AWS_S3_CUSTOM_DOMAIN = env.str("AWS_S3_CUSTOM_DOMAIN", "")
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400',}

    # s3 static settings
    AWS_LOCATION = 'static'
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
else:
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, "static"),
]

MEDIA_ROOT = os.path.join(BASE_DIR, "mediafiles")
MEDIA_URL = "/media/"

# Default storage settings, with the staticfiles storage updated.
# See https://docs.djangoproject.com/en/5.0/ref/settings/#std-setting-STORAGES
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    # ManifestStaticFilesStorage is recommended in production, to prevent
    # outdated JavaScript / CSS assets being served from cache
    # (e.g. after a Wagtail upgrade).
    # See https://docs.djangoproject.com/en/5.0/ref/contrib/staticfiles/#manifeststaticfilesstorage
    "staticfiles": {
        # "BACKEND": "django.contrib.staticfiles.storage.ManifestStaticFilesStorage",
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}


# Wagtail settings

WAGTAIL_SITE_NAME = ""

# Search
# https://docs.wagtail.org/en/stable/topics/search/backends.html
WAGTAILSEARCH_BACKENDS = {
    "default": {
        "BACKEND": "wagtail.search.backends.database",
    }
}

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
WAGTAILADMIN_BASE_URL = "http://example.com"


# editor settings
WAGTAILADMIN_RICH_TEXT_EDITORS = {
    'default': {
        'WIDGET': 'wagtail.admin.rich_text.DraftailRichTextArea',
        'OPTIONS': {'features': ['h2', 'h3', 'bold', 'italic', 'strikethrough', 'ol', 'ul', 'hr', 'link', 'buttons', 'embed', 'document-link', 'image'],}
    },
    'minimal': {
        'WIDGET': 'wagtail.admin.rich_text.DraftailRichTextArea',
        'OPTIONS': {
            'features': ['bold', 'italic', 'strikethrough','ol', 'ul',]
        }
    }
}


EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = env.str("EMAIL_HOST", "")
EMAIL_PORT = env.int("EMAIL_PORT", "")
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env.str("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = env.str("EMAIL_HOST_PASSWORD", "")

FROM_EMAIL = env.str("FROM_EMAIL")
RECIPIENT_LIST = env.list("RECIPIENT_LIST", default=[""])


RECAPTCHA_PUBLIC_KEY = env.str("RECAPTCHA_PUBLIC_KEY")
RECAPTCHA_PRIVATE_KEY = env.str("RECAPTCHA_PRIVATE_KEY")
NOCAPTCHA = True

WAGTAILEMBEDS_RESPONSIVE_HTML = True
