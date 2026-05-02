from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'activation_key', 'activation_key_expires']
        extra_kwargs = {
            'activation_key': {'write_only': True},
            'password': {'write_only': True}
        }

    def validate_password(self, password):
        validate_password(password)
        return password

    def create(self, validated_data):
        user = User(email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()

        return user
