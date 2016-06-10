"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 1.8.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'e_#e-byj7#a+$v7#wmocwd8wp)+&wajk0axt70dl@)nsx!*glq'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
if DEBUG is False:
    #ALLOWED_HOSTS = ['www.edocumentservice.org', '104.155.204.241']
    ALLOWED_HOSTS = ['*']
else:
    ALLOWED_HOSTS = []
ADMINS = [
    ('woody', 'tsengwoody.tw@gmail.com'),
    ('amy', 't101598002@ntut.edu.tw'),
    ('eDocumentService', 'edocumentservice@gmail.com'),
]

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'account',
    'ebookSystem',
    'genericUser',
    'guest',
    'manager',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'mysite.urls'

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

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

if DEBUG is True:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'eDocumentServiceDev',
            'USER': 'root',
            'PASSWORD': 'root',
            'HOST': '127.0.0.1',
            'PORT': '3306',
        }
    }

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
LOGIN_URL = '/auth/login'
LOGIN_REDIRECT_URL = '/account/profile'
LOGOUT_URL = '/account/profile'
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
FILE_CHARSET='utf-8'
AUTH_USER_MODEL = 'genericUser.User'

#CACHES = {
#    'default': {
#        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
#        'LOCATION': 'my_cache_table',
#    }
#}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

from django.conf import global_settings
FILE_UPLOAD_HANDLERS = ('utils.cache.UploadProgressCachedHandler', ) + global_settings.FILE_UPLOAD_HANDLERS
#FILE_UPLOAD_HANDLERS = ('utils.uploadFile.ProgressUploadSessionHandler', ) + global_settings.FILE_UPLOAD_HANDLERS

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST='smtp.gmail.com'
EMAIL_PORT=587
EMAIL_HOST_USER = 'edocumentservice@gmail.com'
EMAIL_HOST_PASSWORD = 'cozpzzyyuetvhxwe'
EMAIL_USE_TLS = True
#smtp.mail.yahoo.com

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(message)s\t%(levelname)s\t%(asctime)s\t%(module)s\t%(process)d\t%(thread)d'
        },
    },
    'handlers': {
        'file': {
            'level': 'WARNING',
            'formatter': 'verbose',
            'class': 'logging.FileHandler',
            'filename': os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'log') +'/djangoOS.log',
        },
        'rotating_file':
        {
            'level' : 'DEBUG',
            'formatter' : 'verbose',
            'class' : 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'log') +'/djangoOS_rotate.log',
            'when' : 'midnight',
            'interval' : 1,
            'backupCount' : 7,
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'rotating_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

#special define
INACTIVE = 0
ACTIVE =1
EDIT =2
REVIEW =3
REVISE = 4
FINISH = 5
MANAGER = ['tsengwoody@yahoo.com.tw']
SERVICE = 'edocumentservice@gmail.com'
PREFIX_PATH = BASE_DIR +'/'
