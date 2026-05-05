from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils import timezone

from .models import VirtualMachine


class ActivateVmSerializer(serializers.Serializer):
    activation_key = serializers.CharField(max_length=36)

    def validate_activation_key(self, value):
        User = get_user_model()
        user = User.objects.filter(activation_key=value).first()

        if not user:
            raise serializers.ValidationError('Недействительный ключ активации')

        self.context['user'] = user

        return value

    def create(self, validated_data):
        vm = VirtualMachine.objects.filter(is_active=True, current_user=None).first()

        if not vm:
            raise serializers.ValidationError({'activation_key': 'Все прокси заняты'})

        user = self.context['user']

        vm.current_user = user
        vm.last_used_at = timezone.now()
        vm.save()

        return vm

    def to_representation(self, instance):
        return {
            'host': instance.host,
            'port': instance.port,
            'protocol': instance.protocol,
            'user_id': instance.current_user.pk,
        }
