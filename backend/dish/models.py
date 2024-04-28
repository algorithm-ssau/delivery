from django.db import models
from django.conf import settings


class Ingredient(models.Model):
    """Модель ингредиентов"""
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
        default_related_name = 'Types'

    def __str__(self):
        return f'{self.name}'


class Dish(models.Model):
    name = models.CharField(
        verbose_name="Название",
        max_length=settings.LIMIT_CHAR_100
    )
    description = models.CharField(
        verbose_name="Описание",
        max_length=settings.LIMIT_CHAR_500
    )
    cost = models.PositiveSmallIntegerField(
        verbose_name="Стоимость"
    )
    ccal = models.PositiveSmallIntegerField(
        verbose_name="Килокалории"
    )
    weight = models.PositiveSmallIntegerField(
        verbose_name="Вес"
    )
    image = models.ImageField(
        verbose_name="Фотография",
        upload_to="dishes/"
    )

    class Meta:
        verbose_name = "Блюдо"
        verbose_name_plural = "Блюда"
        default_related_name = "Dishes"

    def __str__(self):
        return f'{self.name} - {self.cost}'
