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

    # שימוש ב-META ליתר ביטחון (תואם גרסאות ישנות וחדשות)
    origin = request.META.get('HTTP_ORIGIN') or request.META.get('HTTP_REFERER', '')

    # חילוץ נקי של הדומיין
    current_domain = urlparse(origin).netloc.lower()
    if not current_domain and origin:  # במקרה שה-origin הוא מחרוזת פשוטה ללא פרוטוקול
        current_domain = origin.split('/')[0].lower()

    # הסרת www.
    if current_domain.startswith('www.'):
        current_domain = current_domain[4:]

    print(f"DEBUG: Found domain: '{current_domain}' from origin: '{origin}'")

    if not key:
        return Response({'valid': False, 'message': 'Missing Key'}, status=400)

    try:
        license_obj = ClientLicense.objects.get(api_key=key)

        # זיקוק הדומיין ששמור ב-Admin
        stored_raw = license_obj.domain.lower()
        stored_domain = urlparse(stored_raw).netloc or stored_raw
        if '/' in stored_domain:
            stored_domain = stored_domain.split('/')[0]
        if stored_domain.startswith('www.'):
            stored_domain = stored_domain[4:]

        # ניקוי סופי של תווים לבנים (רווחים)
        current_domain = current_domain.strip()
        stored_domain = stored_domain.strip()

        if current_domain != stored_domain:
            return Response({
                'valid': False,
                'message': f'Unauthorized Domain. Expected: {stored_domain}, Got: {current_domain}'
            }, status=403)

        if license_obj.is_valid:
            return Response({
                'valid': True,
                'config': {'position': 'left', 'language': 'he', 'ui_theme': 'light'}
            })

        return Response({'valid': False, 'message': 'License Expired'}, status=403)

    except ClientLicense.DoesNotExist:
        return Response({'valid': False, 'message': 'Invalid Key'}, status=404)