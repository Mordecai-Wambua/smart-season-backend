from rest_framework import serializers
from .models import Field, FieldUpdate


class FieldUpdateSerializer(serializers.ModelSerializer):
    # This automatically fetches the username so the frontend doesn't just get a raw ID
    agent_name = serializers.ReadOnlyField(source='agent.username')

    class Meta:
        model = FieldUpdate
        fields = ('id', 'field', 'agent', 'agent_name', 'note', 'is_issue', 'created_at')
        # We make agent read-only because we will automatically set it to the logged-in user in the ViewSet
        read_only_fields = ('agent', 'created_at')


class FieldSerializer(serializers.ModelSerializer):
    # This exposes our computed property (Active, At Risk, Completed)
    status = serializers.ReadOnlyField()
    agent_name = serializers.ReadOnlyField(source='agent.username')

    # Nested updates so the frontend gets the field's history in one API call
    updates = FieldUpdateSerializer(many=True, read_only=True)

    class Meta:
        model = Field
        fields = (
            'id', 'name', 'crop_type', 'planting_date', 'stage',
            'status', 'agent', 'agent_name', 'created_at', 'updated_at', 'updates'
        )