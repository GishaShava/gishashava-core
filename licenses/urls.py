from django.urls import path
from . import views

urlpatterns = [
    # שים לב שהוספנו 'licenses/' כאן כדי להשלים את הנתיב מהקובץ הראשי
    path('licenses/validate/', views.validate_license, name='validate_license'),
]