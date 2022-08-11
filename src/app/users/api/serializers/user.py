from rest_framework import serializers

from app.users.models import User
from utils.rest_framework.serializers import build_model_serializer_class


class UserSerializer(serializers.ModelSerializer[User]):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "username",
            "is_staff",
            "is_active",
            "is_superuser",
        )
        read_only_fields = (
            "id",
            "is_staff",
            "is_active",
            "is_superuser",
        )


SimpleUserSerializer = build_model_serializer_class(
    model_class=User,
    field_list=["username", "email", "first_name", "last_name"],
)
