from django.contrib import admin
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.admin import UserAdmin

from api.account.models import *



class UserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = UserChangeForm
    model = UserModel
    list_display = ('email', 'is_staff', 'is_active','is_superuser')
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username','groups','last_name','mobile','industry','linked_profile','gender')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(UserModel, UserAdmin)    
    

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display=('id', 'name','created_by', 'created_at', 'updated_at')

@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display=('id', 'name', 'country','created_by', 'created_at', 'updated_at')

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display=('id', 'name', 'zone', 'created_by', 'created_at', 'updated_at')
    
    
@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display=('id', 'name', 'region', 'created_by', 'created_at', 'updated_at')
    
    
@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display=('id', 'name', 'state', 'created_by', 'created_at', 'updated_at')
    
    
    
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'country', 'city','created_by', 'created_at', 'updated_at')    
    
    
@admin.register(Industry)
class IndustryAdmin(admin.ModelAdmin):
    list_display = ('id','parent', 'name','company', 'created_by', 'created_at', 'updated_at')    
    
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('id', 'title','created_by', 'created_at', 'updated_at')    
    

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','industry','created_by', 'created_at', 'updated_at')      
    

admin.site.register(Profile)
admin.site.register(UserActiveDetail)


# admin.site.register(Role)
# admin.site.register(Department)
# admin.site.register(UserRole)


from django.contrib import admin
from django.contrib.auth.models import Permission
from .models import UserRole, UserModel, Role, Department

class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'department')
    list_filter = ('role', 'department')
    search_fields = ('user__username', 'role__name', 'department__name')
    filter_horizontal = ('permissions',)

    fieldsets = (
        (None, {
            'fields': ('user', 'role', 'department')
        }),
        ('Permissions', {
            'fields': ('permissions',),
        }),
    )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Add permissions to the user when UserRole is saved
        user = obj.user
        for perm in obj.permissions.all():
            user.user_permissions.add(perm)
        user.save()

    def delete_model(self, request, obj):
        user = obj.user
        # Remove permissions from the user when UserRole is deleted
        for perm in obj.permissions.all():
            user.user_permissions.remove(perm)
        user.save()
        super().delete_model(request, obj)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # Ensure that we have the permissions available in the queryset
        return queryset.prefetch_related('permissions')

admin.site.register(UserRole, UserRoleAdmin)
admin.site.register(Role)
admin.site.register(Department)
admin.site.register(Permission)

