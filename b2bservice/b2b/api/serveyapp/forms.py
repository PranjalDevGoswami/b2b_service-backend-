from django import forms
from django.contrib import admin
from .models import UserRole, Permission

class UserRoleForm(forms.ModelForm):
    class Meta:
        model = UserRole
        fields = '__all__'

    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        required=False,
        widget=admin.widgets.FilteredSelectMultiple('Permissions', False)
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['permissions'].initial = self.instance.permissions.all()

    def save(self, commit=True):
        user_role = super().save(commit=False)
        if commit:
            user_role.save()
        if user_role.pk:
            user_role.permissions.set(self.cleaned_data['permissions'])
            self.save_m2m()
        return user_role
