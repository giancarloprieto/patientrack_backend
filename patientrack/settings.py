"""
Django settings for patientrack project.

Generated by 'django-admin startproject' using Django 2.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
from email.header import Header
from email.utils import formataddr

from django.utils.translation import gettext_lazy as _
from dotenv import load_dotenv

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

dotenv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
load_dotenv(dotenv_path)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '1ivvzx++&ea0p71l$l08&^e_0=c0%76!(_2f8cmzqmd+d&c%##'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = (os.getenv('DEBUG', 'False') == 'True')

ALLOWED_HOSTS = ['localhost', 'ewr2dm9n5i.execute-api.us-east-1.amazonaws.com']

AUTH_USER_MODEL = 'authentication.User'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.forms',
    'storages',
    'authentication.apps.AuthenticationConfig',
    'device.apps.DeviceConfig',
    'facility.apps.FacilityConfig',
    'followup.apps.FollowupConfig',
    'main.apps.MainConfig',
    'monitoring.apps.MonitoringConfig',
    'patient.apps.PatientConfig',
    'report.apps.ReportConfig',
    'staff.apps.StaffConfig',
    'my_pwa.apps.MyPwaConfig',
    'pwa'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'whitenoise.middleware.WhiteNoiseMiddleware',
]

# WHITENOISE_USE_FINDERS = True

ROOT_URLCONF = 'patientrack.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'patientrack.wsgi.application'

FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME", "patientrack"),
        "USER": os.getenv("DB_USERNAME", "postgres"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT", 5432),
        "CONN_MAX_AGE": (5 * 60)
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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

AWS_ACCESS_KEY_ID = os.getenv("AWS_PATIENTRACK_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_PATIENTRACK_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME", "patientrack")
AWS_REGION_NAME = 'us-east-1'

DEFAULT_FILE_STORAGE = 'main.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = 'main.s3boto3.S3Boto3StoragePublic'

MEDIA_FILETYPE = ['.pdf', '.png', '.jpg']
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "patientrack", "static"),
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

TIME_ZONE = 'America/Bogota'
USE_TZ = True
USE_I18N = True
USE_L10N = True
USE_THOUSAND_SEPARATOR = True

LANGUAGE_CODE = 'es-co'
LANGUAGES = [
    ('es-co', _('Colombian Spanish')),
    ('en-us', _('American English')),
]
LANG_SUPPORTED = dict(LANGUAGES).keys()
LANGUAGE_COOKIE_NAME = 'pt_lang'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = formataddr((str(Header('PatienTrack'.encode(), 'utf-8')), "patientrack.rpm@gmail.com"))

LOGIN_URL = '/authentication/login/'
LOGIN_REDIRECT_URL = 'monitoring:list'
LOGOUT_REDIRECT_URL = 'authentication:login'

PWA_APP_NAME = 'Patientrack'
PWA_APP_DESCRIPTION = 'Remote patient monitoring app'
PWA_APP_THEME_COLOR = "#eeeeee"
PWA_APP_BACKGROUND_COLOR = "#f3f6f4"
PWA_APP_DISPLAY = 'standalone'
PWA_APP_SCOPE = '/'
PWA_APP_ORIENTATION = 'any'
PWA_APP_START_URL = '/dev/authentication/login/'
PWA_APP_ROOT_URL = '/dev/'


PWA_SERVICE_WORKER_PATH = os.path.join(BASE_DIR, 'patientrack/static', 'serviceWorker.js')
PWA_APP_ICONS = [
    {'src': 'https://patientrack.s3.amazonaws.com/static/websiteplanet-dummy-144X144.png', 'sizes': "144x144"}
]

PWA_APP_ICONS_APPLE = [
    {'src': 'https://patientrack.s3.amazonaws.com/static/websiteplanet-dummy-144X144.png', 'sizes': "144x144"}
]

PWA_APP_SPLASH_SCREEN = [
    {'src': 'https://patientrack.s3.amazonaws.com/static/websiteplanet-dummy-1440X900.png'}
]

PWA_APP_SCREENSHOTS = [
    {
        'src': 'https://patientrack.s3.amazonaws.com/static/websiteplanet-dummy-750x1334.png',
        'sizes': '750x1334'
    },
    {
        'src': 'https://patientrack.s3.amazonaws.com/static/websiteplanet-dummy-1440x900.png',
        'sizes': '1440x900',
        'form_factor': 'wide',  # Para dispositivos de escritorio
    },
]


if DEBUG:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
            },
        },
        'loggers': {
            'django.db.backends': {
                'handlers': ['console'],
                'level': 'DEBUG',
            },
        },
    }
    PWA_SERVICE_WORKER_PATH = os.path.join(BASE_DIR, 'patientrack/static', 'serviceWorker.js')
    PWA_APP_ICONS = [
        {'src': f'{STATIC_URL}monitoreo-02-02.png', 'sizes': "155x134"}
    ]

    PWA_APP_ICONS_APPLE = [
        {'src': f'{STATIC_URL}monitoreo-02-02.png', 'sizes': "155x134"}
    ]

    PWA_APP_SPLASH_SCREEN = [
        {'src': f'{STATIC_URL}logo_web.png'}
    ]

