from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="CLOCKEDIN API",
        default_version="v1",
        description="Dokumentacja API dla projektu CLOCKEDIN_Backend",
        terms_of_service="https://www.yourapp.com/terms/",
        contact=openapi.Contact(email="jo2k.devepment@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("api/admin/", include("CLOCKEDIN_Backend.views.admin.urls")),
    path("auth/", include("CLOCKEDIN_Backend.views.auth.urls")),
    path("api/user/", include("CLOCKEDIN_Backend.views.user.urls")),
    path("api/test/", include("CLOCKEDIN_Backend.views.test.urls")),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
