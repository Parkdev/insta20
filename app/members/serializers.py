from django.contrib.auth import get_user_model
from rest_framework import serializers

from members.models import FollowRelations

User = get_user_model()


class FollowRelationsSerializer(serializers.ModelSerializer):
    from_relation = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = FollowRelations
        fields = (
            'pk',
            'from_relation',
            'to_relation',
            'relation_type',
            'followed_at',
        )
        read_only_field = (
            'from_relation',
        )


class UserSerializer(serializers.ModelSerializer):
    # following = FollowRelationsSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = (
            'pk',
            'email',
            'password',
            'following',
        )
        extra_kwargs = {
            'password': {'write_only': True}
        }
