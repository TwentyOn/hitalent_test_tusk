from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'activation_key', 'activation_key_expires']
        extra_kwargs = {
            'activation_key': {'read_only': True},
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


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)

    def validate_old_password(self, old_password):
        user = self.context.get('user')

        if not user:
            raise ValueError('Параметр user не передан в контекст')

        if not user.check_password(old_password):
            raise serializers.ValidationError('Неверный пароль')

    def validate_new_password(self, new_password):
        validate_password(new_password)
        return new_password

    def save(self, **kwargs):
        user = self.context.get('user')

        if not user:
            raise ValueError('Параметр user не передан в контекст')

        user.set_password(self.validated_data['new_password'])
        user.save()
        return user