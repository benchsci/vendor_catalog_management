# pylint: skip-file
# Django settings may have similarities: https://github.com/PyCQA/pylint/issues/214
"""Example production settings.

Copy me to start a new project.
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

import environ
env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

# reading .env file
environ.Env.read_env()


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = []


# Application definition
PROJECT_APPS = [
    "benchsci.plugins.authenticator.apps.AuthenticatorConfig",
    "benchsci.vendor_catalog",
]

THIRD_PARTY_APPS = []

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

INSTALLED_APPS = PROJECT_APPS + DJANGO_APPS + THIRD_PARTY_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "benchsci.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': env.db(),
}


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = "/static/"

# BenchSci OAuth authenticator plugin settings
BENCHSCI_AUTHENTICATOR_OAUTH_KEY = env("SOCIAL_AUTH_GOOGLE_OAUTH2_KEY")
BENCHSCI_AUTHENTICATOR_OAUTH_SECRET = env("SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET")
LOGIN_URL = '/login/'
LOGOUT_REDIRECT_URL = '/'

# GCP backend authentication
GOOGLE_CLOUD_CREDENTIALS_FILE = env("GOOGLE_CLOUD_CREDENTIALS_FILE")
GCS_VENDOR_BUCKET=env("GCS_VENDOR_BUCKET")
TRANSLATION_LOCATION=env('TRANSLATION_LOCATION')
