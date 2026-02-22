from django.contrib import admin
from django.urls import path, include  # <-- שים לב שהוספנו את include

urlpatterns = [
    path('admin/', admin.site.urls),

    # הפנייה לקובץ ה-URL של האפליקציה
    # כל כתובת שתתחיל ב-api/ תועבר לטיפול של licenses.urls
    path('api/', include('licenses.urls')),
]