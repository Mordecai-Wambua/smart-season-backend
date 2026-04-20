from djoser.serializers import UserSerializer as BaseUserSerializer, UserCreateSerializer as BaseUserCreateSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        # Role is excluded to prevent self-assignment on registration
        fields = ('id', 'username', 'password', "first_name", "last_name")

class CurrentUserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = ('id', 'username', 'role', 'first_name', 'last_name')
        # CRITICAL: Prevents users from promoting themselves via /users/me/
        read_only_fields = ('role',) 

class AdminUserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = ('id', 'username', 'role', 'first_name', 'last_name')
        # Role is writable here. This serializer will only be accessible to Admins.