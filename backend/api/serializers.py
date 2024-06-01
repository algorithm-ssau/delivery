"""
Содержит сериализаторы для преобразования данных:
    - Пользователя;
    - ...
"""

from djoser.serializers import UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from dish.models import (Dish, Ingredient, IngredientAmount, Type,
                         Order, OrderDish)
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
    is_in_order = serializers.SerializerMethodField()
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
            'is_in_order',
        )

    @staticmethod
    def dishes_ingredients_add(ingredients, dish):
        ingredients_amount = [
            IngredientAmount(
                ingredient=Ingredient.objects.get(
                    id=ingredient['ingredient']['id']
                ),
                dish=dish,
                amount=ingredient['amount']
            ) for ingredient in ingredients
        ]
        IngredientAmount.objects.bulk_create(ingredients_amount)

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredientamount_set')
        dish = Dish.objects.create(**validated_data)
        self.dishes_ingredients_add(ingredients, dish)
        return dish

    def update(self, instance, validated_data):
        IngredientAmount.objects.filter(dish=instance).delete()
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
    is_in_order = serializers.SerializerMethodField()

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
            'is_in_order',
        )

    def get_is_in_order(self, obj):
        request = self.context.get('request')
        return (request and request.user.is_authenticated
                and Order.objects.filter(
                    user=request.user, dishes=obj
                ).exists())


class OrderDishSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='dish.id')
    name = serializers.ReadOnlyField(source='dish.name')
    image = serializers.SerializerMethodField()
    cost = serializers.IntegerField(read_only=True)
    quantity = serializers.IntegerField(read_only=True)

    class Meta:
        model = OrderDish
        fields = ['id', 'name', 'image', 'cost', 'quantity']

    def get_image(self, obj):
        return obj.dish.image.url if obj.dish.image else None


class OrderSerializer(serializers.ModelSerializer):
    dishes = OrderDishSerializer(source='orderdish_set', many=True)
    user = UserReadSerializer(read_only=True)
    total_cost = serializers.IntegerField(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'dishes', 'total_cost', 'payment']
    @staticmethod
    def order_dish_add(dishes, order):
        for dish_data in dishes:
            OrderDish.objects.create(
                dish=Dish.objects.get(
                    id=dish_data['dish']['id']
                ),
                order=order,
                quantity=1)

    def create(self, validated_data):
        dishes = validated_data.pop('orderdish_set')
        order = Order.objects.create(**validated_data,
                                     user=self.context['request'].user)
        self.order_dish_add(dishes, order)
        order.calculate_total_cost()
        order.save()
        return order

    def update(self, instance, validated_data):
        OrderDish.objects.filter(order=instance).delete()
        dishes = validated_data.pop('orderdish_set')
        self.order_dish_add(dishes, instance)
        instance.calculate_total_cost()
        return super().update(instance, validated_data)
