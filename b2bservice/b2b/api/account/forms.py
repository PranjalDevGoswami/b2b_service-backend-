from django import forms
from django.contrib.auth.forms import UserCreationForm
from api.account.models import UserModel
# from django.contrib.auth import get_user_model

# User = get_user_model()
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ('email', 'username', 'password')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.set_password(self.cleaned_data["password"])
            user.save()
        return user
