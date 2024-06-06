from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

def trigger_error(request):
    division_by_zero = 1 / 0
    
# Create a Swagger/OpenAPI schema view
schema_view = get_schema_view(
    openapi.Info(
        title="API DOCUMENTATION",
        default_version="v1",
        description="Twiga",
        contact=openapi.Contact(email="salmanyagaka@gmail.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("social_media_project.apps.user_service.urls")),
    path("blogs/", include("social_media_project.apps.post_service.urls")),
    path('sentry-debug/', trigger_error),
    # Swagger documentation URL
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
]
