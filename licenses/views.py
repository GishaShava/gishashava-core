from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import ClientLicense
from django.conf import settings

@api_view(['GET'])
def validate_license(request):
    key = request.GET.get('key')
    # זיהוי הדומיין שממנו נשלחה הבקשה
    origin = request.headers.get('Origin') or request.META.get('HTTP_REFERER', '')

    if not key:
        return Response({'valid': False, 'message': 'Missing Key'}, status=400)

    try:
        license_obj = ClientLicense.objects.get(api_key=key)

        # בדיקה שהדומיין של הלקוח תואם למה שרשום במערכת
        if origin and license_obj.domain not in origin:
            return Response({'valid': False, 'message': 'Unauthorized Domain'}, status=403)

        if license_obj.is_valid:
            return Response({
                'valid': True,
                'config': {
                    'position': 'right',
                    'language': 'he',
                    'ui_theme': 'light'
                }
            })

        return Response({'valid': False, 'message': 'License Expired'}, status=403)

    except ClientLicense.DoesNotExist:
        return Response({'valid': False, 'message': 'Invalid Key'}, status=404)