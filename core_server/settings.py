# בתוך קובץ settings.py בתיקיית core_server

DEBUG = False  # בשלב הייצור תמיד False

# הוספתי את הכתובת של השרת שלך
ALLOWED_HOSTS = ['gishashava.pythonanywhere.com', 'localhost', '127.0.0.1']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',      # ודא שהוספת את זה
    'corsheaders',         # ודא שהוספת את זה
    'licenses',            # שם האפליקציה שלך
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware', # חייב להיות ראשון!
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

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

# הגדרות CORS - מאפשר לאתר ב-GitHub "לדבר" עם השרת
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    "https://gishashava.github.io",
    "https://buildstudio.website",
]