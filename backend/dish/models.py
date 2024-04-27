from django.db import models
from django.conf import settings


class Ingredient(models.Model):
    id = models.IntegerField(
        verbose_name="Индентификатор",
        max_length=settings.LIMIT_INT_100,
        primary_key=True
    )
    name = models.CharField(
        verbose_name="Название",
        max_length=settings.LIMIT_CHAR_200
    )
    measurement_unit = models.CharField(
        verbose_name="Единица измерения",
        max_length=settings.LIMIT_CHAR_200
    )

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'
        default_related_name = 'Ingredients'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_ingredient',
            )
        ]

    def __str__(self):
        return f'{self.name} {self.measurement_unit}'


class Teg(models.Model):
    TYPE = (
        (SUSHI, "Суши"),
        (PIZZA, "Пицца"),
        (Burger, "Бургер")
    )
    id = models.IntegerField(
        verbose_name="Индентификатор",
        max_length=settings.LIMIT_INT_100,
        primary_key=True
    )
    type = models.CharField(
        verbose_name="Тип",
        max_length=settings.LIMIT_CHAR_10,
        choices=TYPE
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        default_related_name = 'tags'

    def __str__(self):
        return f'{self.type}'
