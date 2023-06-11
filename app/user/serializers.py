from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext as _

from rest_framework import serializers

from core.models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""
    # user_permissions = serializers.SerializerMethodField()
    # user_permissions = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'password', 'name', 'avatar', 'user_permissions')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    # def get_user_permissions(self, obj):
    #     return list(obj.user_permissions.all())
    # def get_user_permissions(self, obj):
    #     return list(obj.user_permissions.all()) # I'm not sure list type casting is necessary

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class UserAvatarSerializer(serializers.ModelSerializer):
    """Serializer for uploading avatars to users"""

    class Meta:
        model = User
        fields = ('id', 'avatar')
        read_only_fields = ('id',)
        extra_kwargs = {'image': {'required': 'True'}}


class AuthTokenSerialier(serializers.Serializer):
    """Serializer for the user authentication object"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msg = _("Unable to authenticate with provided credentials")
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs
