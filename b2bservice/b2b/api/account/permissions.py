from rest_framework import permissions
from rest_framework.permissions import BasePermission
from api.account.models import *

####################### Request User IsSuperuser ################################

from rest_framework.permissions import BasePermission

class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser

class HasRolePermission(BasePermission):
    def __init__(self, perm):
        self.perm = perm

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        user_role = UserRole.objects.filter(user=request.user).first()
        if not user_role:
            return False
        return request.user.is_superuser or user_role.permissions.filter(codename=self.perm).exists()
