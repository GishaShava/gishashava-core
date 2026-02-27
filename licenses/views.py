from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from urllib.parse import urlparse
from .models import ClientLicense


@csrf_exempt
@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def validate_license(request):
    key = request.GET.get('key')

    # 1. שליפת מקור הבקשה (Origin או Referer)
    raw_origin = request.META.get('HTTP_ORIGIN') or request.META.get('HTTP_REFERER', '')

    # 2. חילוץ וניקוי הדומיין מהבקשה
    current_domain = urlparse(raw_origin).netloc.lower()
    if not current_domain and raw_origin:
        current_domain = raw_origin.replace('https://', '').replace('http://', '').split('/')[0].lower()

    if current_domain.startswith('www.'):
        current_domain = current_domain[4:]

    current_domain = current_domain.strip()

    if not key:
        return Response({'valid': False, 'message': 'Missing Key'}, status=400)

    try:
        # 3. שליפת הרישיון מהדאטה-בייס
        license_obj = ClientLicense.objects.get(api_key=key)

        # 4. חילוץ וניקוי הדומיין השמור
        stored_raw = license_obj.domain.lower()
        stored_domain = urlparse(stored_raw).netloc or stored_raw
        if '/' in stored_domain:
            stored_domain = stored_domain.split('/')[0]
        if stored_domain.startswith('www.'):
            stored_domain = stored_domain[4:]

        stored_domain = stored_domain.strip()

        # --- בלוק ה-DEBUG הקריטי ---
        print(f"--- FAILED LOGIN DEBUG START ---")
        print(f"1. Key from Request: '{key}'")
        print(f"2. Key from DB Obj:  '{license_obj.api_key}'")
        print(f"3. Domain Request:   |{current_domain}| (len: {len(current_domain)})")
        print(f"4. Domain DB:        |{stored_domain}| (len: {len(stored_domain)})")
        print(f"5. Are they equal?   {current_domain == stored_domain}")
        print(f"--- FAILED LOGIN DEBUG END ---")

        # 5. בדיקת התאמה
        if current_domain != stored_domain:
            return Response({
                'valid': False,
                'message': f'Unauthorized Domain. Expected: {stored_domain}, Got: {current_domain}'
            }, status=403)

        # 6. בדיקת תוקף הרישיון
        if license_obj.is_valid:
            return Response({
                'valid': True,
                'config': {
                    'position': 'left',
                    'language': 'he',
                    'ui_theme': 'light'
                }
            })

        return Response({'valid': False, 'message': 'License Expired'}, status=403)

    except ClientLicense.DoesNotExist:
        return Response({'valid': False, 'message': 'Invalid Key'}, status=404)