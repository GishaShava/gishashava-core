from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from urllib.parse import urlparse  # כלי לפירוק כתובות URL
from .models import ClientLicense


@csrf_exempt
@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def validate_license(request):
    # הדפסת כל ה-Headers כדי לראות מה הדפדפן באמת שולח
    print(f"--- DEBUG START ---")
    print(f"ALL HEADERS: {request.headers}")
    print(f"ORIGIN: {request.headers.get('Origin')}")
    print(f"REFERER: {request.META.get('HTTP_REFERER')}")

    key = request.GET.get('key')
    raw_origin = request.headers.get('Origin') or request.META.get('HTTP_REFERER', '')

    # 2. זיקוק הדומיין בלבד (למשל: מוריד https וסלאשים)
    # urlparse("https://site.com/").netloc -> "site.com"
    current_domain = urlparse(raw_origin).netloc or raw_origin

    # הסרת 'www.' אם קיים, כדי להתאים למסד הנתונים שלך
    if current_domain.startswith("www."):
        current_domain = current_domain[4:]

    current_domain = current_domain.strip().lower()

    if not key:
        return Response({'valid': False, 'message': 'Missing Key'}, status=400)

    try:
        license_obj = ClientLicense.objects.get(api_key=key)

        # 3. זיקוק הדומיין ששמור ב-Admin (ליתר ביטחון)
        stored_domain = urlparse(license_obj.domain).netloc or license_obj.domain
        if stored_domain.startswith("www."):
            stored_domain = stored_domain[4:]

        stored_domain = stored_domain.strip().lower()

        # 4. בדיקת התאמה מדויקת
        if current_domain != stored_domain:
            return Response({
                'valid': False,
                'message': f'Unauthorized Domain: {current_domain}'
            }, status=403)

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