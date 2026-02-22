from django.urls import path
from .views import validate_license

urlpatterns = [
    # הכתובת המלאה תהיה: your-domain.com/api/validate-license/
    path('validate-license/', validate_license, name='validate_license'),
]