from rest_framework import serializers

from google_forms_clone.users.models import User


class UserSerializer(serializers.ModelSerializer[User]):
    class Meta:
        model = User
        fields = ["username", "first_name", "url"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"},
        }