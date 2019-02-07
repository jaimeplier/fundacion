from rest_framework import permissions


class ConsejeroPermission(permissions.BasePermission):
    """
    Permisos de consejero
    """

    def has_permission(self, request, view):
        if request.user is not None:
            return request.user.rol.pk == 3
        return False

class CalidadPermission(permissions.BasePermission):
    """
    Permisos de personal de calidad
    """

    def has_permission(self, request, view):
        if request.user is not None:
            return request.user.rol.pk == 6
        return False