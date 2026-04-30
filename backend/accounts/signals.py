from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save

from .models import User
from .tasks import send_activation_key


@receiver(post_save, sender=User)
def update_key(created, instance, *args, **kwargs):
    if created:
        email = instance.email
        activation_key = instance.activation_key
        send_activation_key.delay(email, activation_key)
