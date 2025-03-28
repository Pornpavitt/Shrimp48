"""
Django settings for IT48 project.

Generated by 'django-admin startproject' using Django 5.0.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ne7zb!_8y&$e*h9b-%=aimjckc#zof&mdr%l02$2%t_o-*#12o'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app_general.apps.AppGeneralConfig',
    'app_users.apps.AppUsersConfig',
    'app_model.apps.AppModelConfig',
    'tailwind',
    'theme',
    'customadmin',
    "django_icons",
    'app_shrimp_pool.apps.AppShrimpPoolConfig',
    'app_shrimp_price.apps.AppShrimpPriceConfig',
    
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

ROOT_URLCONF = 'IT48.urls'

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

WSGI_APPLICATION = 'IT48.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
import os
 

DATABASES = {
    
    # 'default': dj_database_url.config(default=os.getenv("mysql://root:RgVzKYVBQssYFKRMNWKoLzfICCrKwaHS@hopper.proxy.rlwy.net:22509/railway"))
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME' : 'bit07_shrimp',
        'HOST' : 'localhost',
        'USER' : 'root',
        'PASSWORD' : '',
        'PORT' : '3306'
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': BASE_DIR / 'db.sqlite3',
    }
}

#mysql://root:RgVzKYVBQssYFKRMNWKoLzfICCrKwaHS@hopper.proxy.rlwy.net:22509/railway
# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'th'

TIME_ZONE = 'Asia/Bangkok'

USE_L10N = True

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#JAZZMIN

JAZZMIN_SETTINGS = {
    "site_brand": "Shrimp48",
}
    

#Tailwind
TAILWIND_APP_NAME = 'theme'


#Auth
LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "home"

DJANGO_ICONS = {
    "ICONS": {
        "edit": {"name": "far fa-pencil"},
    },
}

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


