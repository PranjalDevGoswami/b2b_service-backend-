from django.contrib import admin
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.admin import UserAdmin

from api.account.models import *



class UserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = UserChangeForm
    model = UserModel
    list_display = ('id','email', 'is_staff', 'is_active','is_superuser')
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




from django.contrib import admin
from django.contrib.auth.models import Permission
from .models import UserRole, UserModel, Role, Department


class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'department', 'designation')
    list_filter = ('role', 'department', 'designation')
    search_fields = ('user__username', 'role__name', 'department__name', 'designation__name')
    
    # Adding fields to manage permissions directly in the admin panel
    filter_horizontal = ('permissions',)  # For ManyToManyField (permissions)

    def get_form(self, request, obj=None, **kwargs):
        """
        Customize the form to include only relevant permissions for the UserRole.
        """
        form = super().get_form(request, obj, **kwargs)
        # You can filter the permissions here if needed
        form.base_fields['permissions'].queryset = Permission.objects.all()
        return form

    def has_add_permission(self, request):
        """
        Control who can add a new UserRole from the admin panel.
        """
        return request.user.has_perm('your_app.can_create')

    def has_change_permission(self, request, obj=None):
        """
        Control who can edit an existing UserRole from the admin panel.
        """
        return request.user.has_perm('your_app.can_edit')

    def has_delete_permission(self, request, obj=None):
        """
        Control who can delete a UserRole from the admin panel.
        """
        return request.user.has_perm('your_app.can_delete')

    def has_view_permission(self, request, obj=None):
        """
        Control who can view UserRole entries in the admin panel.
        """
        return request.user.has_perm('your_app.can_view')

admin.site.register(UserRole, UserRoleAdmin)
admin.site.register(Role)
admin.site.register(Department)
admin.site.register(Designation)
admin.site.register(Permission)

