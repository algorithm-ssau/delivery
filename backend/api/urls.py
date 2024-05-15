"""
Определяет маршрутизацию URL для операций:
    - пользователя;
    - ...;

Маршруты:
    - /users: операции с пользователями;
    - ...;
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register('users', views.UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path(r'auth/', include('djoser.urls')),
    path(r'auth/', include('djoser.urls.authtoken')),
]
