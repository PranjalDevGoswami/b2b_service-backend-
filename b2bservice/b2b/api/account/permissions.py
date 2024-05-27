from rest_framework import permissions

####################### Request User IsActive ################################

class IsActive(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_active:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_active:
            return True
        return False




##################Sales TL####################################################

class IsSalesTL(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.groups.filter(name="Sales TL"):
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name="Sales TL"):
            return True
        return False



################################# Operation ##################################


class IsOperationTl(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.groups.filter(name="Operation Tl").exists():
            return True
        
        return False
    

class IsOperationManager(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.groups.filter(name="Operation Manager").exists():
            return True
        
        return False
    

class IsOperationHod(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.groups.filter(name="Operation Hod").exists():
            return True
        
        return False
            
################################################ Finance ###################################
class IsFinancesHod(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.groups.filter(name="Finance Hod").exists():
            return True
        
        return False
    
    
    