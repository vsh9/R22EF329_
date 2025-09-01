import string, random
from datetime import timedelta
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import ShortURL, ClickEvent
from .serializers import ShortURLSerializer, ShortURLResponseSerializer, ClickEventSerializer
from Logging_Middleware.main import Logger

logger = Logger()

def generate_shortcode(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

@api_view(["POST"])
def create_short_url(request):
    serializer = ShortURLSerializer(data=request.data)
    if serializer.is_valid():
        url = serializer.validated_data["url"]
        validity = serializer.validated_data.get("validity", 30)
        shortcode = serializer.validated_data.get("shortcode")

        if not shortcode:
            shortcode = generate_shortcode()

        if ShortURL.objects.filter(shortcode=shortcode).exists():
            logger.log("backend", "error", "handler", f"Shortcode {shortcode} already exists")
            return Response({"error": "Shortcode already exists"}, status=400)

        expiry = timezone.now() + timedelta(minutes=validity)
        short = ShortURL.objects.create(url=url, shortcode=shortcode, expiry=expiry)

        logger.log("backend", "info", "handler", f"Created short URL {shortcode}")

        resp = {
            "shortLink": f"http://localhost:8000/{shortcode}",
            "expiry": short.expiry.isoformat()
        }
        return Response(resp, status=status.HTTP_201_CREATED)
    
    logger.log("backend", "error", "handler", "Invalid request to create short URL")
    return Response(serializer.errors, status=400)


@api_view(["GET"])
def redirect_short_url(request, shortcode):
    short = get_object_or_404(ShortURL, shortcode=shortcode)

    if short.has_expired():
        logger.log("backend", "warn", "handler", f"Short URL {shortcode} expired")
        return Response({"error": "Link expired"}, status=410)

    # Log click event
    ClickEvent.objects.create(
        short_url=short,
        referrer=request.META.get("HTTP_REFERER"),
        ip_address=request.META.get("REMOTE_ADDR"),
    )
    short.click_count += 1
    short.save()

    logger.log("backend", "info", "handler", f"Redirected {shortcode} to {short.url}")

    return redirect(short.url)


@api_view(["GET"])
def short_url_stats(request, shortcode):
    short = get_object_or_404(ShortURL, shortcode=shortcode)

    clicks = ClickEventSerializer(short.clicks.all(), many=True).data

    data = {
        "url": short.url,
        "created_at": short.created_at,
        "expiry": short.expiry,
        "click_count": short.click_count,
        "clicks": clicks,
    }

    logger.log("backend", "info", "handler", f"Fetched stats for {shortcode}")

    return Response(data, status=200)
