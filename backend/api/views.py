"""
Содержит View-классы реализующие операции моделей:
    - User;
    - ...;

Модули:
    - UserViewSet;
    - ...
"""

from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import filters, mixins, viewsets

from dish.models import Dish, Ingredient, Type
from user.models import User

from .filters import DishFilter, IngredientFilter
from .serializers import (DishReadSerializer, DishWriteSerializer,
                          IngredientSerializer, TypeSerializer,
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


class DishViewSet(viewsets.ModelViewSet):
    """View-класс реализующий операции модели Dish"""

    queryset = Dish.objects.all()
    # permissions = [IsAuthorOrReadOnly]
    filter_backends = (filters.SearchFilter, DjangoFilterBackend, )
    search_fields = ('name',)
    filterset_class = DishFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return DishReadSerializer
        return DishWriteSerializer
