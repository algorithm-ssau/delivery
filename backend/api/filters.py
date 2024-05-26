from dish.models import Ingredient
from django_filters.rest_framework import FilterSet, filters


class IngredientFilter(FilterSet):
    """Поиск ингредиента по полю name регистронезависимо
        начиная с указанного значения"""

    name = filters.CharFilter(
        field_name='name',
        lookup_expr='istartswith',
    )

    class Meta:
        model = Ingredient
        fields = ('name',)
