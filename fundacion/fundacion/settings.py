"""
Django settings for fundacion project.

Generated by 'django-admin startproject' using Django 1.11.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os


# GDAL PARA FUNCIONAR EN WINDOWS
"""
if os.name == 'nt':
    import platform
    OSGEO4W = r"C:\OSGeo4W"
    if '64' in platform.architecture()[0]:
        OSGEO4W += "64"
    assert os.path.isdir(OSGEO4W), "Directory does not exist: " + OSGEO4W
    os.environ['OSGEO4W_ROOT'] = OSGEO4W
    os.environ['GDAL_DATA'] = OSGEO4W + r"\share\gdal"
    os.environ['PROJ_LIB'] = OSGEO4W + r"\share\proj"
    os.environ['PATH'] = OSGEO4W + r"\bin;" + os.environ['PATH']
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'i=3^xi75cspp^ng3p)v@xn^we%p+u5v)mh9gp)3#m(d8^*cqcs'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

AUTH_USER_MODEL = 'config.Usuario'

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'ec2-34-221-30-40.us-west-2.compute.amazonaws.com', 'ec2-52-32-27-159.us-west-2.compute.amazonaws.com']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'widget_tweaks',
    'config.apps.ConfigConfig',
    'webapp.apps.WebappConfig',
    'adminstrador.apps.AdminstradorConfig',
    'supervisor.apps.SupervisorConfig',
    'consejero.apps.ConsejeroConfig',
    'directorio.apps.DirectorioConfig',
    'calidad.apps.CalidadConfig',
    'rest_framework',
    'rest_framework.authtoken',
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

ROOT_URLCONF = 'fundacion.urls'

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

WSGI_APPLICATION = 'fundacion.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.mysql',
        'NAME': 'fundacionorigen',
        'USER': 'inydes',
        'PASSWORD': 'rRy2S<_:',
        'HOST': 'inydes.cl7uq5voofn2.us-west-2.rds.amazonaws.com',
        'PORT': '3306'
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'es-MX'

TIME_ZONE = 'America/Mexico_City'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATICFILES_DIRS = [os.path.join(BASE_DIR, "fundacion/static"), ]

STATIC_URL = "/static/"

MEDIA_URL = "/media/"

STATIC_ROOT = "/var/django/static/"

MEDIA_ROOT = "/var/django/media/"

FILE_UPLOAD_PERMISSIONS = 0o644

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DATETIME_FORMAT': "%Y-%m-%d %H:%M",
    'TIME_FORMAT': "%H:%M",
}
