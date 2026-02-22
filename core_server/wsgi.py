import os
import sys

# הגדרת הנתיב לתיקיית הפרויקט
path = '/home/meydan/access_site'
if path not in sys.path:
    sys.path.append(path)

# הגדרת מודול ה-Settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'core_server.settings'

# הפעלת האפליקציה
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()