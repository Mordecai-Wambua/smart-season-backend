from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Djoser Core Endpoints (users, me, etc.)
    path('api/auth/', include('djoser.urls')),
    
    # Djoser JWT Endpoints (login, refresh, verify)
    path('api/auth/', include('djoser.urls.jwt')),

    path('api/', include('operations.urls')),

    # OpenAPI Schema and Swagger UI
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]