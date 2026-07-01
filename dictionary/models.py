from django.db import models

# Create your models here.
class Status(models.Model):
    created_at = models.DateField(auto_now_add=True)
    name = models.CharField(verbose_name='Имя статуса', unique=True)

    def __str__(self):
        return self.name

class Type(models.Model):
    created_at = models.DateField(auto_now_add=True)
    name = models.CharField(verbose_name='Имя типа', unique=True)

    def __str__(self):
        return self.name