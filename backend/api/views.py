"""
Содержит View-классы реализующие операции моделей:
    - User;
    - ...;

Модули:
    - UserViewSet;
    - ...
"""

from djoser.views import UserViewSet as DjoserUserViewSet

from user.models import User

from .serializers import UserReadSerializer


class UserViewSet(DjoserUserViewSet):
    """View-класс реализующий операции модели User"""

    queryset = User.objects.all()
    serializer_class = UserReadSerializer
