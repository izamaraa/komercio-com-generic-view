from rest_framework import permissions


# class ReviewIsSellerPermission(permissions.BasePermission):
#     from rest_framework import permissions


# get e post normal
class ProductPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if not request.user.is_authenticated:
            return False

        return request.user.is_authenticated and request.user.is_seller


# se nao for o dono vai ser barrado
class ProductActivePermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if not request.user.is_authenticated:
            return False

        return request.user.id == obj.seller_id
