from django.db import models


# Create your models here.

class Category(models.Model):
    created_at = models.DateField(auto_now_add=True)
    name = models.CharField(verbose_name='Категория')
    parent = models.ForeignKey(
        to='self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Родительская категория'
    )

    def __str__(self):
        return self.name


class Status(models.Model):
    created_at = models.DateField(auto_now_add=True)
    name = models.CharField(verbose_name='Имя статуса', unique=True)

    def __str__(self):
        return self.name


class Type(models.Model):
    created_at = models.DateField(auto_now_add=True)
    name = models.CharField(verbose_name='Имя типа', unique=True)
    category = models.ManyToManyField(to=Category)

    def __str__(self):
        return self.name
