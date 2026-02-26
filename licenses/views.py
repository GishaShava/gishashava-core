from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from .models import ClientLicense


@csrf_exempt  # פטור מבדיקת CSRF (קריטי ל-API חיצוני)
@api_view(['GET'])
@permission_classes([AllowAny])  # מבטיח שגם משתמשים לא מחוברים יוכלו לבדוק רישיון
def validate_license(request):
    key = request.GET.get('key')

    # זיהוי הדומיין שממנו נשלחה הבקשה
    origin = request.headers.get('Origin') or request.META.get('HTTP_REFERER', '')

    if not key:
        return Response({'valid': False, 'message': 'Missing Key'}, status=400)

    try:
        # שליפת הרישיון מהדאטה-בייס
        license_obj = ClientLicense.objects.get(api_key=key)

        # בדיקה שהדומיין של הלקוח תואם למה שרשום במערכת
        # הוספנו בדיקה מקלה למקרה של סביבת פיתוח או חוסר ב-Origin
        if origin and license_obj.domain not in origin:
            return Response({
                'valid': False,
                'message': f'Unauthorized Domain: {origin}'
            }, status=403)

        # בדיקה אם הרישיון פעיל (is_valid הוא שדה במודיל שלך)
        if license_obj.is_valid:
            return Response({
                'valid': True,
                'config': {
                    'position': 'left',  # עדכנו לשמאל כפי שביקשת
                    'language': 'he',
                    'ui_theme': 'light'
                }
            })

        return Response({'valid': False, 'message': 'License Expired'}, status=403)

    except ClientLicense.DoesNotExist:
        return Response({'valid': False, 'message': 'Invalid Key'}, status=404)