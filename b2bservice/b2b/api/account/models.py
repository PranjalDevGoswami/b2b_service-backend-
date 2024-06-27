from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, _user_has_perm, AbstractUser
)
from django.core.validators import (
    FileExtensionValidator
)
from django.contrib.auth.models import Group, Permission
from django.core.exceptions import PermissionDenied
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import Token
import datetime
from django.utils import timezone
from django.core.validators import URLValidator
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django_userforeignkey.models.fields import UserForeignKey


class Trackable(models.Model):
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='created_%(class)s', on_delete=models.CASCADE, blank=True, null=True)
    updated_by = UserForeignKey(settings.AUTH_USER_MODEL, auto_user_add=True, blank=True, null=True, related_name='modified_%(class)s')
    class Meta:
        abstract = True

class PermissionsMixin(models.Model):
    """
    A mixin class that adds the fields and methods necessary to support
    Django's Group and Permission model using the ModelBackend.
    """
    is_superuser = models.BooleanField(
        _('superuser status'),
        default=False,
        help_text=_(
            'Designates that this user has all permissions without'
            'explicitly assigning them.'
        ),
    )
    groups = models.ForeignKey(
        Group,
        verbose_name=_('Selected Group'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="user_groups_set",
        related_query_name="lims_user",
        on_delete = models.SET_NULL
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="user_permissions_set",
        related_query_name="btob_user",
    )

    class Meta:
        abstract = True
        default_permissions = ()

    def get_group_permissions(self, obj=None):
        """
        Returns a list of permission strings that this user has through their
        groups. This method queries all available auth backends. If an object
        is passed in, only permissions matching this object are returned.
        """
        permissions = set()
        for backend in auth.get_backends():
            if hasattr(backend, "get_group_permissions"):
                permissions.update(backend.get_group_permissions(self, obj))
        return permissions

    def get_all_permissions(self, obj=None):
        return self._user_get_all_permissions(obj)

    def has_perm(self, perm, obj=None):
        """
        Returns True if the user has the specified permission. This method
        queries all available auth backends, but returns immediately if any
        backend returns True. Thus, a user who has permission from a single
        auth backend is assumed to have permission in general. If an object is
        provided, permissions for this specific object are checked.
        """

        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

        # Otherwise we need to check the backends.
        return _user_has_perm(self, perm, obj)

    def has_perms(self, perm_list, obj=None):
        """
        Returns True if the user has each of the specified permissions. If
        object is passed, it checks if the user has all required perms for this
        object.
        """
        for perm in perm_list:
            if not self.has_perm(perm, obj):
                return False
        return True

    def has_module_perms(self, app_label):
        """
        Returns True if the user has any permissions in the given app label.
        Uses pretty much the same logic as has_perm, above.
        """
        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

        return _user_has_module_perms(self, app_label)


def filter_user_queryset_by_hierarchy(user, queryset, filter_on='assign_to_user__in'):
    if user.is_superuser:
        return queryset
    else:
        all_childrens = user.get_all_child
        return queryset.filter(**{filter_on: all_childrens})


class UserManager(BaseUserManager):
    def create_user(self,email, username=None, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        
        email = self.normalize_email(email)
        user = self.model(username=username,
                          email=email, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self,email, password,username=None, **extra_fields):
        user = self.create_user(
            username=username, email=email, password=password,  **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Country(Trackable):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return self.name
    
class Zone(Trackable):
    name = models.CharField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='zones', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Region(Trackable):
    name = models.CharField(max_length=255)
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, null=True, blank=True, related_name='regions')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    

class State(Trackable):
    name = models.CharField(max_length=255)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=True, blank=True, related_name='states')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name         
    

class City(Trackable):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, null=True, blank=True, related_name='cities')

    def __str__(self):
        return self.name         

class Company(Trackable):
    name = models.CharField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True, related_name="companies")
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True, related_name='company_city')
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return self.name
    
    
    

class Industry(Trackable):
    name = models.CharField(max_length=255,verbose_name="Industry Name")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True, related_name="industries")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Industry Hierarchy"
        verbose_name_plural = "Industry Hierarchies"

    def __str__(self):
        return self.name
    
    
class Category(Trackable):
    name = models.CharField(max_length=255,verbose_name="Category Name")
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE, null=True, blank=True, related_name="categories")
    is_active = models.BooleanField(default=True)    
    
    def __str__(self):
        return self.name
    
    
    
class Job(Trackable):
    title = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
   
    
    
    def __str__(self):
        return self.title


class UserModel(AbstractUser, PermissionsMixin):
    username = None
    gender_choice = (
        (1, 'Male'),
        (2, 'Female')
    )
    date_of_birth = models.DateField(null=True, blank=True)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    middle_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    gender = models.PositiveSmallIntegerField(
        choices=gender_choice, null=True, blank=True)
    username = models.CharField(max_length=60, unique=True, null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    mobile = models.BigIntegerField(null=True, blank=True)
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE,null=True, blank=True,related_name="users_industries")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    linked_profile = models.TextField(validators=[URLValidator()])
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    contact_person_name = models.CharField(max_length=150, blank=True, null=True)
    contact_person_number = models.CharField(max_length=10, blank=True, null=True)
    
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        group = self.groups.all().first()
        if hasattr(group, 'name'):
            role = group.name
        else:
            role = 'N/A'
  
        return str(self.username) + '('+role+')'

    @property
    def profile_pic(self):
        return self.profile

    def has_module_perms(self, app_label):
        return True

    class Meta:
        default_permissions = ()
        permissions = (
            ('can_edit', 'Can Edit'),
            ('can_view', 'Can View'),
            ('can_create', 'Can Create'),
            ('can_delete', 'Can Delete'),
        )

    @property
    def get_user_harkey(self, *args, **kwargs):
        role_names = self.roles().split(',')
        user_filter = User.objects.filter(
            role__name__in=role_names
        ).order_by('order')
        return user_filter

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        Token.objects.get_or_create(user=self)

    def roles(self):
        return ",".join([str(p) for p in self.groups.all()])

    def selected_role(self):
        return self.temp_groups

    def get_has_perms_single_obj(self, mode, model, obj):
        '''
        mode = ('change', 'view', 'add', 'delete')
        model = "Laboratory"
        obj = "Laboratory instance obj"
        '''
        return self.has_perm('{0}_{1}'.format(mode, model.lower()), obj)

    def assign_django_gurdian_obj(self, role_name, mode, model, obj):
        pass

    def has_group(self, group_name):
        # group_name = 'Manak'
        return self.groups.filter(name=group_name).exists()


class Profile(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, null=True, blank=True, related_name="user_job")
    designation = models.CharField(max_length=30, blank=True)
    countries = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True, related_name="user_country")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True, related_name="user_company")
    profile_picture = models.ImageField(
        null=True, blank=True,
        upload_to='profile/', default='profile/default_pic.jpg',
        verbose_name='Recent Photograph',
        validators=[FileExtensionValidator(
            allowed_extensions=['jpg', 'jpeg', 'png'])]
    )
    # birth_date = models.DateField(null=True, blank=True)
    
    
    def __str__(self):
        return self.user.username

@receiver(post_save, sender=UserModel)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=UserModel)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    



class UserActiveDetail(models.Model):
    user= models.OneToOneField(UserModel, related_name='last_active_timestamp', on_delete=models.CASCADE, blank=True, null=True)
    last_active_time= models.DateTimeField(null=True,blank=True)

    def set_last_activity(self):
        self.last_active_time=datetime.datetime.now()
        self.save()
        return True

    def set_last_active_time_null(self):
        self.last_active_time=None
        self.save()
        return True

    def set_lastactive_time(cls,user):
        try:
            useractivity_datail= UserActiveDetail.objects.get(user=user)
            useractivity_datail.set_last_activity()
        except Exception as e:
            UserActiveDetail.objects.create(user=user,last_active_time=datetime.datetime.now())

    def __str__(self):
        return self.user.username
    


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class UserRole(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Industry")


    def __str__(self):
        return f"{self.user.username} - {self.role.name} - {self.user.industry.name}"