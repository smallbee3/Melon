"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 2.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""
import json
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = os.path.dirname(BASE_DIR)

# 'django/templates' 폴더
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/
STATIC_ROOT = os.path.join(ROOT_DIR, '.static_root')
STATIC_URL = '/static/'
# STATIC_URL = '/asdf/' -> 바꿀 수 있음.
# -> 우선순위가 url.config보다 더 우선시 되는 것 같음.

# 만약 요청의 URL이 /static/으로 시작할 경우,
# STATICFILES_DIRS에 정의된 경로 목록에서
# /static/<path>/
#         <path> 부분에 정의된 경로에 해당하는
# 파일을 찾아 돌려준다.


# Media (User-uploaded files)
# ec2-deploy/.media
MEDIA_ROOT = os.path.join(ROOT_DIR, '.media')
MEDIA_URL = '/media/'


# 'django/static' 폴더
STATIC_DIR = os.path.join(BASE_DIR, 'static')
# Django에서 정적파일을 검색할 경로 목록
STATICFILES_DIRS = [
    STATIC_DIR
]


# SECRET #
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
SECRETS_DIR = os.path.join(ROOT_DIR, '.secrets')
SECRETS_BASE = os.path.join(SECRETS_DIR, 'base.json')

# 1) base.json 파일을 읽어온 결과
f = open(SECRETS_BASE, 'rt')
base_text = f.read()
f.close()

# 2) 위 결과(JSON형식의 문자열)를 파이선 객체로 변환
secrets_base = json.loads(base_text)

# print(secrets_base)


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = secrets_base['SECRET_KEY']
YOUTUBE_API_KEY = secrets_base['YOUTUBE_API_KEY']
FACEBOOK_APP_ID = secrets_base['FACEBOOK_APP_ID']
FACEBOOK_SECRET_CODE = secrets_base['FACEBOOK_SECRET_CODE']
EMAIL_HOST_PASSWORD = secrets_base['EMAIL_HOST_PASSWORD']
SMS_API_KEY = secrets_base['SMS_API_KEY']
SMS_API_SECRET = secrets_base['SMS_API_SECRET']
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# DEBUG = False

ALLOWED_HOSTS = [
    'localhost',
    '.amazonaws.com',
    '.dlighter.com',
]
# ALLOWED_HOSTS = ['*']
# ALLOWED_HOSTS = ['localhost']

# 특정 도메인에서 드러왔을 때만 장고 앱이 실행되게 하는 것.
# locul host -> 개발할 때 로컬호스트만 하니까.


# 02/23 Melon 23 Customizing User2
AUTH_USER_MODEL = 'members.User'


# FacebookBackend #

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'members.backends.FacebookBackend',
]


# Email

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = secrets_base['EMAIL_HOST_USER']
# EMAIL_HOST_PASSWORD =
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = secrets_base['DEFAULT_FROM_EMAIL']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Thirdparty App
    'django_extensions',
    'raven.contrib.django.raven_compat',


    # Custom App
    'album',
    'artist',
    'song',
    'members',
    'video',
    'sms',
    'emails',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            TEMPLATES_DIR
        ],
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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),

        # 'ENGINE': 'django.db.backends.postgresql',
        # 'HOST': 'localhost',
        # 'PORT': '5432',
        # 'NAME': 'fc-melon',
        # 'USER': 'smallbee3',
        # 'PASSWORD': 'asdfqwer',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True


import os
import raven

RAVEN_CONFIG = {
    'dsn': 'https://844d67919ebf49599e6525bee02651da:a60c7dbeac694aaa886cda13ca4dadec@sentry.io/298730',
    # If you are using git, you can also automatically configure the
    # release based on the git info.
    'release': raven.fetch_git_sha(os.path.abspath(os.pardir)),
}


# Google에서 django sentry log 검색 후 처음 문서
# https://docs.sentry.io/clients/python/integrations/django/

# (* Google에서 django sentry로 검색 후 나오는 처음 문서와 이유는 모르나
#   처음 부분에 내용이 조금 다름)
#   https://raven.readthedocs.io/en/stable/integrations/django.html

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'ERROR', # To capture more than ERROR, change to WARNING, INFO, etc.
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            'tags': {'custom-tag': 'x'},
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}
