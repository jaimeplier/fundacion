from rest_framework import permissions


class ConsejeroPermission(permissions.BasePermission):
    """
    Permisos de consejero
    """

    def has_permission(self, request, view):
        if request.user is not None:
            return request.user.rol.pk == 3
        return False