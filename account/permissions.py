from rest_framework import permissions

# se for o dono da conta fazer edicoes
class IsOwnerAccount(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        return request.user.id == obj.id


# se for adm mudar is active pra true
class IsAdmAccount(permissions.BasePermission):
    def has_permission(self, request, view):

        if not request.user.is_authenticated:
            return False

        return request.user.is_superuser
