from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from app.jwt.views import (
    CookieTokenObtainPairView,
    RefreshTokenView,
)

RefreshTokenView
urlpatterns = [
    path("admin/", admin.site.urls),
    path("user/", include("authentication.urls")),
    path("raffles/", include("raffles.urls")),
    path("api/token/", CookieTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", RefreshTokenView.as_view(), name="token_refresh"),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
        path("silk/", include("silk.urls", namespace="silk")),
    ] + urlpatterns
