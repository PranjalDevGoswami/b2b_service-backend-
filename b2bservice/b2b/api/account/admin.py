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
        ('Personal info', {'fields': ('first_name','middle_name','groups','last_name','mobile','industry','linked_profile','gender')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
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
    list_display = ('id', 'name','company', 'created_by', 'created_at', 'updated_at')    
    
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('id', 'title','created_by', 'created_at', 'updated_at')    
    

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','industry','created_by', 'created_at', 'updated_at')      
    

admin.site.register(Profile)
admin.site.register(UserActiveDetail)
