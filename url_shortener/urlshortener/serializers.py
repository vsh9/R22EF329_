from rest_framework import serializers
from .models import ShortURL, ClickEvent

class ShortURLSerializer(serializers.ModelSerializer):
    validity = serializers.IntegerField(write_only=True, required=False, default=30)
    shortcode = serializers.CharField(required=False)

    class Meta:
        model = ShortURL
        fields = ["url", "shortcode", "validity"]

class ShortURLResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortURL
        fields = ["shortcode", "expiry"]

class ClickEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClickEvent
        fields = ["timestamp", "referrer", "ip_address"]
