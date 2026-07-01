from django.db import models
from django.shortcuts import reverse

# Create your models here.
class Dds(models.Model):
    created_at = models.DateField(auto_now_add=True)
    status = models.CharField(choices=[('Бизнес', 'Бизнес'), ('Личное', 'Личное'), ('Налог', 'Налог')])
    type = models.CharField(choices=[('Пополнение', 'Пополнение'), ('Списание', 'Списание')])

    summa = models.IntegerField()
    comments = models.TextField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse('dds-detail', args=[self.pk])