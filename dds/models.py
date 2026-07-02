from django.db import models
from django.shortcuts import reverse

from dictionary.models import Status, Type, Category


# Create your models here.
class Dds(models.Model):
    created_at = models.DateField(auto_now_add=True)
    status = models.ForeignKey(to=Status, on_delete=models.DO_NOTHING, verbose_name='Статус')
    type = models.ForeignKey(to=Type, on_delete=models.PROTECT, verbose_name='Тип')
    category = models.ForeignKey(to=Category, on_delete=models.PROTECT, verbose_name='Категория')
    summa = models.IntegerField(verbose_name='Сумма, руб')
    comment = models.TextField(verbose_name='Комментарий', blank=True, null=True)

    def get_absolute_url(self):
        return reverse('dds-detail', args=[self.pk])
