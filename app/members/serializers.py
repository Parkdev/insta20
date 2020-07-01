from django.contrib.auth import get_user_model
from rest_framework import serializers

from members.models import User

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'pk',
            'email',
            'password'
        )
        extra_kwargs = {
            'password': {'write_only': True}
        }

