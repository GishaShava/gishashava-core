import os
from pathlib import Path

# 1. הגדרת נתיב הבסיס - קריטי להפעלת השרת
BASE_DIR = Path(__file__).resolve().parent.parent

# טעינת משתני סביבה מה-.env (כדי שה-SECRET_KEY יעבוד ב-Terminal)
env_path = BASE_DIR / '.env'
if env_path.exists():
    with open(env_path) as f:
        for line in f:
            if line.startswith('export '):
                key, value = line.replace('export ', '', 1).strip().split('=', 1)
                os.environ[key.strip()] = value.strip().strip("'").strip('"')

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-development-key-only')

DEBUG = False

ALLOWED_HOSTS = ['gishashava.pythonanywhere.com', 'localhost', '127.0.0.1']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'licenses',
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

ROOT_URLCONF = 'core_server.urls'

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

WSGI_APPLICATION = 'core_server.wsgi.application'

# 2. הגדרת בסיס הנתונים - זה מה שהיה חסר בשגיאה שלך!
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# הגדרות סיסמה
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# שפה וזמן
LANGUAGE_CODE = 'he'
TIME_ZONE = 'Israel'
USE_I18N = True
USE_TZ = True

# 3. קבצים סטטיים - קריטי למראה של ה-Admin
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CORS
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    "https://gishashava.github.io",
    "https://buildstudio.website",
]