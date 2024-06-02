from rest_framework import permissions


class CanModifyOrder(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj.user == request.user and not obj.payment


class IsAdminOrOwnerAndPaymentTrue(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_staff:
            return True

        if obj.user == request.user and obj.payment:
            return True

        return False