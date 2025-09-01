from django.urls import path
from .views import create_short_url, redirect_short_url, short_url_stats

urlpatterns = [
    path("shorturls/", create_short_url, name="create_short_url"),
    path("shorturls/<str:shortcode>/", short_url_stats, name="short_url_stats"),
    path("<str:shortcode>/", redirect_short_url, name="redirect_short_url"),
]
