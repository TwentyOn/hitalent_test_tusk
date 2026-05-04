from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

from .validators import protocol_validator

User = get_user_model()


# Create your models here.
class VirtualMachine(models.Model):
    name = models.CharField(max_length=100, unique=True)
    host = models.CharField(max_length=255)
    port = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(65535)])
    protocol = models.CharField(validators=[protocol_validator])
    is_active = models.BooleanField(default=True)
    current_user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    last_user_at = models.DateTimeField(null=True, auto_now=True)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        db_table = f'{settings.DB_SCHEMA_NAME}"."virtual_machine'
        unique_together = [('host', 'port', 'protocol')]
