"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 3.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

import mysite.env
mysite.env.set()


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ["eDocumentService_SECRET_KEY"]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'rest_framework',
	'corsheaders',
	'django_filters',
	'ebookSystem',
	'genericUser',
	#'rules',
	'rules.apps.AutodiscoverRulesConfig',
]

MIDDLEWARE = [
	'corsheaders.middleware.CorsMiddleware',
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

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
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

#DATABASES = {
#	'default': {
#		'ENGINE': 'django.db.backends.sqlite3',
#		'NAME': BASE_DIR / 'db.sqlite3',
#	}
#}

DB_BACKEND = os.environ.get('eDocumentService_DB_BACKEND')
if True:
	DATABASES = {
		'default': {
		'ENGINE': 'django.db.backends.mysql',
		'NAME': os.environ.get('eDocumentService_DATABASE'),
		'USER': os.environ.get('eDocumentService_DB_USER'),
		'PASSWORD': os.environ.get('eDocumentService_DB_PASS'),
		'HOST': os.environ.get('eDocumentService_DB_HOST'),
		'PORT': os.environ.get('eDocumentService_DB_PORT'),
		}
	}


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


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'genericUser.User'

AUTHENTICATION_BACKENDS = (
	'rules.permissions.ObjectPermissionBackend',
	'django.contrib.auth.backends.ModelBackend',
)

REST_FRAMEWORK = {
	#'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
	#'PAGE_SIZE': 10,
	'DEFAULT_PERMISSION_CLASSES': (
	#'rest_framework.permissions.IsAuthenticated',
	),
	'DEFAULT_AUTHENTICATION_CLASSES': (
	'rest_framework_simplejwt.authentication.JWTAuthentication',
	'rest_framework.authentication.SessionAuthentication',
	'rest_framework.authentication.BasicAuthentication',
	),
}

CORS_ORIGIN_ALLOW_ALL = True

LOGGING = {
	'version': 1,
	'disable_existing_loggers': False,
	'formatters': {
	'verbose': {
	'format':
	'%(message)s,%(levelname)s,%(asctime)s,%(module)s,%(process)d,%(thread)d',
	},
	},
	'handlers': {
	'file': {
	'level':
	'WARNING',
	'formatter':
	'verbose',
	'class':
	'logging.FileHandler',
	'filename':
	os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
	'log') + '/djangoOS.log',
	},
	'rotating_file': {
	'level':
	'WARNING',
	'formatter':
	'verbose',
	'class':
	'logging.handlers.TimedRotatingFileHandler',
	'filename':
	os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
	'log') + '/djangoOS_rotate.log',
	'when':
	'midnight',
	'interval':
	1,
	'backupCount':
	365,
	},
	},
	'loggers': {
	'django': {
	'handlers': ['rotating_file'],
	'level': 'WARNING',
	#'level': 'DEBUG',
	'propagate': True,
	},
	},
}

CACHES = {
	'default': {
	'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
	'LOCATION': os.environ.get('eDocumentService_MEMCACHED_SERVICE'),
	}
}

import socket
if socket.gethostname() == 'edspro':
	EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
else:
	EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

OTP_ACCOUNT = os.environ["eDocumentService_OTP_ACCOUNT"]
OTP_PASSWORD = os.environ["eDocumentService_OTP_PASSWORD"]

EMAIL_HOST = os.environ["eDocumentService_EMAIL_HOST"]
EMAIL_PORT = os.environ["eDocumentService_EMAIL_PORT"]
EMAIL_HOST_USER = os.environ["eDocumentService_EMAIL_HOST_USER"]
EMAIL_HOST_PASSWORD = os.environ["eDocumentService_EMAIL_HOST_PASSWORD"]
EMAIL_USE_TLS = True
SERVICE = EMAIL_HOST_USER
DEFAULT_FROM_EMAIL = 'incloud@forblind.org.tw'
MANAGER = ['edocumentservice@gmail.com', 'meichen@forblind.org.tw']
