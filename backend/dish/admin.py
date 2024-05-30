from django.contrib import admin
from django.contrib.auth.models import Group
from django.db.models import Sum

from .models import (Ingredient, Type, IngredientAmount, Dish, Order)

admin.site.unregister(Group)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Настройка Ingredient для панели Admin"""

    list_display = ('pk', 'name', 'measurement_unit')
    list_filter = ('name',)
    search_fields = ('name',)
    list_editable = ('name', 'measurement_unit',)
    ordering = ('pk',)


@admin.register(Type)
class TagAdmin(admin.ModelAdmin):
    """Настройка Type для панели Admin"""

    list_display = ('pk', 'name', 'slug')
    list_filter = ('name',)
    search_fields = ('name',)
    list_editable = ('name', 'slug')
    ordering = ('pk',)


@admin.register(IngredientAmount)
class IngredientAmountAdmin(admin.ModelAdmin):
    """Настройка IngredientAmount для панели Admin"""

    list_display = ('pk', 'recipes', 'ingredient', 'amount')
    list_filter = ('recipes',)
    search_fields = ('recipes',)
    ordering = ('pk',)


class IngredientInline(admin.TabularInline):
    """Настройка IngredientAmount для панели Admin"""

    model = IngredientAmount
    extra = 1
    min_num = 1


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    """Настройка Dish для панели Admin"""

    list_display = ('pk', 'name', 'description', 'cost', 'ccal', 'weight', 'type', 'dish_ingredients')
    search_fields = ('name',)
    list_filter = ('name', 'type')
    inlines = [IngredientInline, ]
    list_editable = ('name','description', 'cost', 'ccal', 'weight')

    def dish_ingredients(self, obj):
        ingredients = (
            IngredientAmount.objects
            .filter(recipes=obj)
            .order_by('ingredient__name').values('ingredient')
            .annotate(amount=Sum('amount'))
            .values_list(
                'ingredient__name', 'amount',
                'ingredient__measurement_unit'
            )
        )
        ingredient_list = []
        [ingredient_list.append('{} - {} {}.'.format(*ingredient)) for ingredient in ingredients]
        return ingredient_list

    dish_ingredients.short_description = 'Ингредиенты'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Настройка Order для панели Admin"""

    list_display = ('pk', 'count_dish', 'total_cost', 'payment', 'user')
    search_fields = ('user',)
    list_editable = ('total_cost', 'payment')
