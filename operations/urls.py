from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FieldViewSet, FieldUpdateViewSet, DashboardView

router = DefaultRouter()
router.register(r'fields', FieldViewSet, basename='field')
router.register(r'updates', FieldUpdateViewSet, basename='fieldupdate')

urlpatterns = [
    # Custom APIView endpoints
    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    # Router endpoints (fields and updates)
    path('', include(router.urls)),
]