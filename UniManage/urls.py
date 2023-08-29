from django.urls import path, include
from user.admin_site import admin_site
from django.views.generic import RedirectView
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="University Projects API",
        default_version='v1',
        description="API documentation for the School Projects app",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin_site.urls),
    path('user/', include('user.urls')),
    # Assuming 'user.urls' has both regular and API urls differentiated with 'api/' prefix
    path('project/', include('project.urls')),
    # Assuming 'project.urls' has both regular and API urls differentiated with 'api/' prefix
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
