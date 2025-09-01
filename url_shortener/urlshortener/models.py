from django.db import models
from django.utils import timezone
from datetime import timedelta

class ShortURL(models.Model):
    url = models.TextField() 
    shortcode = models.CharField(max_length=2000000, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expiry = models.DateTimeField()
    click_count = models.PositiveIntegerField(default=0)

    def has_expired(self):
        return timezone.now() > self.expiry


class ClickEvent(models.Model):
    short_url = models.ForeignKey(ShortURL, on_delete=models.CASCADE, related_name="clicks")
    timestamp = models.DateTimeField(auto_now_add=True)
    referrer = models.CharField(max_length=255, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
