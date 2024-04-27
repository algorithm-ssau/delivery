from django.db import models
from django.conf import settings


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name="Название",
        max_length=settings.LIMIT_CHAR_200
    )
    measurement_unit = models.CharField(
        verbose_name="Единица измерения",
        max_length=settings.LIMIT_CHAR_200
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        default_related_name = 'Ingredients'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_ingredient',
            )
        ]

    def __str__(self):
        return f'{self.name} {self.measurement_unit}'


class Type(models.Model):
    name = models.CharField(
        verbose_name="Название",
        max_length=settings.LIMIT_CHAR_100
    )
    slug = models.SlugField(
        unique=True,
        max_length=settings.LIMIT_CHAR_200
    )

    class Meta:
        verbose_name = 'Тип'
        verbose_name_plural = 'Типы'
        default_related_name = 'types'

    def __str__(self):
        return f'{self.name}'
