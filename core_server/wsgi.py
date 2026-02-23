import os
import sys
from pathlib import Path

# הגדרת נתיב הפרויקט
path = '/home/GishaShava'
if path not in sys.path:
    sys.path.append(path)

# טעינת משתני סביבה מה-.env
env_path = Path(path) / '.env'
if env_path.exists():
    with env_path.open() as f:
        for line in f:
            if line.startswith('export '):
                key, value = line.replace('export ', '', 1).strip().split('=', 1)
                os.environ[key.strip()] = value.strip().strip("'").strip('"')

# הגדרת קובץ ההגדרות של דג'נגו
os.environ['DJANGO_SETTINGS_MODULE'] = 'core_server.settings'

# הפעלת האפליקציה
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()