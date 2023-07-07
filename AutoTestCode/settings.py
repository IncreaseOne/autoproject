"""
Django settings for AutoTestCode project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import datetime
from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-8g#jo^8yp=b+c13fcd)p%6!=++xl%ek=@@fp4pwqz$i2c2l2jo'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


AMAZON_ACCOUNT = {
    "username": "15071094833",
    "password": "2894232wy"
}

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'TestAmazonCode'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'AutoTestCode.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'AutoTestCode.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

APPEND_SLASH=False


# 日志系统配置
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,  # Disable an existing logger
    'formatters': {  # Log Information Format
        'standard': {  # Detailed log format
            'format': '[%(asctime)s][%(threadName)s:%(thread)d][task_id:%(name)s][%(filename)s:%(lineno)d]'
                      '[%(levelname)s][%(message)s]'
        },
        'simple': {  # Simple log format
            'format': '[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d]%(message)s'
        },
        'collect': {  # Define a special log format
            'format': '%(message)s'
        }
    },
    'filters': {  # Filter the logs
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    # Processor
    'handlers': {
        # Print at terminal
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],  # The log is printed on the screen only when Django debug is True
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        # Default
        'default': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',  # Save to file
            'filename': os.path.join(BASE_DIR, f"./log/{datetime.date.today()}.log"),  # log_file Location
            'maxBytes': 1024 * 1024 * 30,  # log_size 30M
            'backupCount': 10,  # Maximum number of backups
            'formatter': 'standard',
            'encoding': 'utf-8',
        },
        # It is for error logging
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',  # save to log file
            'filename': os.path.join(BASE_DIR, f"./log/{datetime.date.today()}.log"),  # log file
            'maxBytes': 1024 * 1024 * 30,  # log_size 30M
            'backupCount': 10,
            'formatter': 'standard',
            'encoding': 'utf-8',
        },
        # A specific log is defined to collect specific information
        'collect': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, f"./log/{datetime.date.today()}.log"),
            'maxBytes': 1024 * 1024 * 30,  # log_size 30M
            'backupCount': 10,
            'formatter': 'collect',
            'encoding': "utf-8"
        }
    },
    'loggers': {
        # '': {  # The default logger application is configured as follows
        #     'handlers': ['default', 'console', 'error'],  # You can remove the console when you are online
        #     'level': 'DEBUG',
        #     'propagate': True,  # Pass to no higher level logger
        # },
        'collect': {  # The 'collect' logger is also handled separately
            'handlers': ['console', 'collect'],
            'level': 'INFO',
        },
    },
}



