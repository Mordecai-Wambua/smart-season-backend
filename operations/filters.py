# operations/filters.py
import django_filters
from django.db.models import Q, OuterRef, Subquery, BooleanField
from .models import Field, FieldUpdate

class FieldFilter(django_filters.FilterSet):
    # Map the URL params to our custom methods
    status = django_filters.ChoiceFilter(
        choices=[('Active', 'Active'), ('At Risk', 'At Risk'), ('Completed', 'Completed')],
        method='filter_by_status'
    )
    assignment = django_filters.ChoiceFilter(
        choices=[('assigned', 'Assigned'), ('unassigned', 'Unassigned')],
        method='filter_by_assignment'
    )

    class Meta:
        model = Field
        fields = ['status', 'assignment']

    def filter_by_assignment(self, queryset, name, value):
        if value == 'assigned':
            return queryset.filter(agent__isnull=False)
        elif value == 'unassigned':
            return queryset.filter(agent__isnull=True)
        return queryset

    def filter_by_status(self, queryset, name, value):
        if value == 'Completed':
            return queryset.filter(stage=Field.Stage.HARVESTED)

        # The Subquery logic moved here, keeping the ViewSet clean
        latest_issue = FieldUpdate.objects.filter(
            field=OuterRef('pk')
        ).order_by('-created_at').values('is_issue')[:1]

        qs = queryset.annotate(
            latest_is_issue=Subquery(latest_issue, output_field=BooleanField())
        )

        if value == 'At Risk':
            return qs.filter(latest_is_issue=True).exclude(stage=Field.Stage.HARVESTED)
        elif value == 'Active':
            return qs.filter(
                Q(latest_is_issue=False) | Q(latest_is_issue__isnull=True)
            ).exclude(stage=Field.Stage.HARVESTED)

        return queryset