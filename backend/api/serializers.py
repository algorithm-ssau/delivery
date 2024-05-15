"""
Содержит сериализаторы для преобразования данных:
- Пользователя;
- ...
"""

from djoser.serializers import UserSerializer
from rest_framework import serializers
from user.models import User


class UserReadSerializer(UserSerializer):
    """Преобразование данных класса User на чтение"""

    email = serializers.ReadOnlyField()
    first_name = serializers.ReadOnlyField()
    phone = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'phone',
        )
