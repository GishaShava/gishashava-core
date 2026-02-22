from django.db import models
import uuid
from datetime import date

class ClientLicense(models.Model):
    name = models.CharField("שם הלקוח", max_length=100)
    domain = models.CharField("דומיין מורשה", max_length=200, help_text="לדוגמה: example.com")
    # יצירת מפתח ייחודי אוטומטית לכל לקוח
    api_key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    is_active = models.BooleanField("פעיל?", default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateField("תאריך תפוגה")

    def __str__(self):
        return f"{self.name} ({self.domain})"

    # פונקציה לבדוק אם המנוי בתוקף
    @property
    def is_valid(self):
        return self.is_active and self.expires_at >= date.today()