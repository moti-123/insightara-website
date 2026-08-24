from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.views.static import serve as media_serve

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("media/<path:path>", media_serve, {"document_root": settings.MEDIA_ROOT}),
]