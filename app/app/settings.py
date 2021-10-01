from pathlib import Path
from os import getenv, path

import dj_database_url
import django_heroku


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# -----------------------------------------------------------------------------


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = getenv('SECRET_KEY', 'django-insecure-i+wy!!3p9r(p3he1icfkqcuzw360wvawif&_sn_)z%ijz1d_9l')


# -----------------------------------------------------------------------------


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = getenv("DEBUG", False) != "False"


# -----------------------------------------------------------------------------


ALLOWED_HOSTS = getenv('ALLOWED_HOSTS', '*').split(",")


# -----------------------------------------------------------------------------


VEHICLE_API = 'https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMake/'


# -----------------------------------------------------------------------------


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'core',
]


# -----------------------------------------------------------------------------


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# -----------------------------------------------------------------------------


# Activate Django-Heroku.
django_heroku.settings(locals())

# -----------------------------------------------------------------------------


ROOT_URLCONF = 'app.urls'


# -----------------------------------------------------------------------------


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# -----------------------------------------------------------------------------


WSGI_APPLICATION = 'app.wsgi.application'


# -----------------------------------------------------------------------------


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': getenv('POSTGRES_DB', "dev_db_name"),
        'USER': getenv('POSTGRES_USER', "dev_db_user"),
        'PASSWORD': getenv('POSTGRES_PASSWORD',
                           "6NwpPtvGyCsMLAKDZtazEP9WjANze25eP3e2UJdWrgrrKq"),
        'HOST': getenv('POSTGRES_HOST', "localhost"),
        'PORT': getenv('POSTGRES_PORT', 5432),
    }
}

if getenv('HEROKU_POSTGRESQL_BLUE_URL'):
    db_from_env = dj_database_url.config(conn_max_age=600)
    DATABASES['default'].update(db_from_env)


# -----------------------------------------------------------------------------


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# -----------------------------------------------------------------------------


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Warsaw'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# -----------------------------------------------------------------------------


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/


STATIC_URL = '/static/'

if not DEBUG:
    STATIC_ROOT = path.join(BASE_DIR, "staticfiles")
else:
    STATICFILES_DIRS = [
        path.join(BASE_DIR, "static")
    ]


# -----------------------------------------------------------------------------


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# -----------------------------------------------------------------------------


# Email setting for error reporting

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = getenv('EMAIL_HOST')
EMAIL_HOST_USER = getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = getenv('EMAIL_HOST_PASSWORD')
EMAIL_PORT = getenv('EMAIL_PORT')
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER


# -----------------------------------------------------------------------------


# Logging
# https://docs.djangoproject.com/en/3.1/topics/logging/

LOG_LEVEL = 'ERROR' if not DEBUG else 'DEBUG'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': not DEBUG,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s:=> %(message)s',
        },
        'focused': {
            'format': '\n----------------------'
                      '\n%(asctime)s [%(levelname)s] %(name)s:=> %(message)s '
                      '\n----------------------',
        },
    },
    'handlers': {
        'my_custom_debug': {
            'level': LOG_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'focused',
        },
        'request_handler': {
            'level': LOG_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': False,
        }
    },
    'loggers': {
        '': {
            'handlers': ['my_custom_debug'],
            'level': LOG_LEVEL,
            'propagate': True,
        },
        'django.request': {
            'handlers': ['request_handler'],
            'level': LOG_LEVEL,
            'propagate': True,
        },
        'django': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}