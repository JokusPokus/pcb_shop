from rest_framework import serializers
from .models import User, Profile


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('default_shipping_address', 'default_billing_address')


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'profile')
        depth = 2
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

