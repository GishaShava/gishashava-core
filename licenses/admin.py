from django.contrib import admin
from .models import ClientLicense

@admin.register(ClientLicense)
class ClientLicenseAdmin(admin.ModelAdmin):
    list_display = ('name', 'domain', 'api_key', 'is_active', 'expires_at')
    search_fields = ('name', 'domain')