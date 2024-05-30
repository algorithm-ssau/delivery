"""
Содержит View-классы реализующие операции моделей:
    - User;
    - ...;

Модули:
    - UserViewSet;
    - ...
"""

from dish.models import Ingredient, Type
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import filters, mixins, viewsets
from user.models import User

from .filters import IngredientFilter
from .serializers import (IngredientSerializer, TypeSerializer,
                          UserReadSerializer)


class UserViewSet(DjoserUserViewSet):
    """View-класс реализующий операции модели User"""

    queryset = User.objects.all()
    serializer_class = UserReadSerializer


class ListRetrieveViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    """Mixins классов Tag и Ingredients."""
    pagination_class = None
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TypeViewSet(ListRetrieveViewSet):
    """View-класс реализующий операции модели Tag"""

    queryset = Type.objects.all()
    serializer_class = TypeSerializer


class IngredientViewSet(ListRetrieveViewSet):
    """View-класс реализующий операции модели Ingredient"""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filterset_class = IngredientFilter


class DishViewSet:
    pass
