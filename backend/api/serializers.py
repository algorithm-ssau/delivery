"""
Содержит сериализаторы для преобразования данных:
    - Пользователя;
    - ...
"""

from dish.models import Dish, Ingredient, IngredientAmount, Type
from djoser.serializers import UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from user.models import User


class UserReadSerializer(UserSerializer):
    """Преобразование данных класса User на чтение"""

    email = serializers.ReadOnlyField()
    username = serializers.ReadOnlyField()
    phone = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "phone",
        )


class IngredientSerializer(serializers.ModelSerializer):
    """Преобразование данных класса Ingredient"""

    class Meta:
        model = Ingredient
        fields = (
            "id",
            "name",
            "measurement_unit",
        )


class TypeSerializer(serializers.ModelSerializer):
    """Преобразование данных класса Type"""

    class Meta:
        model = Type
        fields = (
            "id",
            "name",
            "slug",
        )


class IngredientAmountSerializer(serializers.ModelSerializer):
    """Преобразование данных класса IngredientAmount"""

    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientAmount
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount',
        )


class DishWriteSerializer(serializers.ModelSerializer):
    """Преобразование данных класса Dish на запись"""

    ingredients = IngredientAmountSerializer(
        many=True,
        source='ingredientamount_set'
    )
    type = serializers.SlugRelatedField(
        queryset=Type.objects.all(),
        slug_field='slug',
    )
    image = Base64ImageField()
    # is_in_order = serializers.SerializerMethodField()
    cost = serializers.IntegerField()
    ccal = serializers.IntegerField()
    weight = serializers.IntegerField()

    class Meta:
        model = Dish
        fields = (
            'id',
            'name',
            'description',
            'cost',
            'ccal',
            'weight',
            'image',
            'type',
            'ingredients',
            # 'is_in_order',
        )

    @staticmethod
    def dishes_ingredients_add(ingredients, recipe):
        ingredients_amount = [
            IngredientAmount(
                ingredient=Ingredient.objects.get(
                    id=ingredient['ingredient']['id']
                ),
                recipes=recipe,
                amount=ingredient['amount']
            ) for ingredient in ingredients
        ]
        IngredientAmount.objects.bulk_create(ingredients_amount)

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredientamount_set')
        recipes = Dish.objects.create(**validated_data)
        self.dishes_ingredients_add(ingredients, recipes)
        return recipes

    def update(self, instance, validated_data):
        IngredientAmount.objects.filter(recipes=instance).delete()
        ingredients = validated_data.pop('ingredientamount_set')
        self.dishes_ingredients_add(ingredients, instance)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        return DishReadSerializer(
            instance,
            context={'request': self.context.get('request')}
        ).data


class DishReadSerializer(serializers.ModelSerializer):
    """Преобразование данных класса Dish на чтение"""

    type = TypeSerializer(read_only=True)
    ingredients = IngredientAmountSerializer(
        many=True,
        source='ingredientamount_set'
    )
    # is_in_order = serializers.SerializerMethodField()

    class Meta:
        model = Dish
        fields = (
            'id',
            'name',
            'description',
            'cost',
            'ccal',
            'weight',
            'image',
            'type',
            'ingredients',
            # 'is_in_order',
        )

    # def get_is_in_order(self, obj):
    #     request = self.context.get('request')
    #     return (request and request.user.is_authenticated
    #             and Order.objects.filter(
    #                 user=request.user, dishes=request.obj
    #             ))
