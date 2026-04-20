# operations/views.py
from rest_framework import viewsets, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Field, FieldUpdate
from .serializers import FieldSerializer, FieldUpdateSerializer
from .permissions import IsAdminOrAssignedAgent
from .filters import FieldFilter  # <-- Import your new filterset


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100


class FieldViewSet(viewsets.ModelViewSet):
    serializer_class = FieldSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrAssignedAgent]
    pagination_class = StandardResultsSetPagination

    # 🚨 Wire up the packages
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = FieldFilter
    search_fields = ['name', 'crop_type']  # Native DRF searching!

    def get_queryset(self):
        """
        Now this method ONLY handles data isolation.
        The filter_backends take care of the rest automatically.
        """
        user = self.request.user
        if user.is_admin():
            return Field.objects.all().order_by('-created_at')
        return Field.objects.filter(agent=user).order_by('-created_at')


class FieldUpdateViewSet(viewsets.ModelViewSet):
    serializer_class = FieldUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_admin():
            return FieldUpdate.objects.all().order_by('-created_at')
        return FieldUpdate.objects.filter(field__agent=user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(agent=self.request.user)


class DashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user

        if user.is_admin():
            fields = Field.objects.all().order_by('-updated_at')
        else:
            fields = Field.objects.filter(agent=user).order_by('-updated_at')

        total_fields = fields.count()
        status_breakdown = {
            'Active': 0,
            'At Risk': 0,
            'Completed': 0
        }

        for field in fields:
            status_breakdown[field.status] += 1

        at_risk_count = status_breakdown['At Risk']
        if total_fields == 0:
            insight_message = "No fields assigned yet. Ready to start the season!"
        elif at_risk_count > 0:
            insight_message = f"Attention needed: {at_risk_count} field(s) currently marked as At Risk."
        else:
            insight_message = "All assigned fields are currently on track. Great job!"

        recent_fields = fields[:5]
        serialized_fields = FieldSerializer(recent_fields, many=True).data

        return Response({
            'role': user.role,
            'total_fields': total_fields,
            'status_breakdown': status_breakdown,
            'insights': {
                'message': insight_message
            },
            'fields': serialized_fields
        })