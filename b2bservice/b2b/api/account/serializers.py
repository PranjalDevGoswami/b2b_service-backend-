from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.core.mail import send_mail
import datetime
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import check_password,make_password
User = get_user_model()
from api.account.models import *

#################### Registration API #############################################

class B2BUserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password2', 'username','date_of_birth', 'gender', 'mobile', 'industry', 'category','linked_profile')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user
    
################################### Login Request ###########################################    

class LoginSerializer(serializers.Serializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
    email = serializers.EmailField()

    class Meta:
        fields = ['email', 'password']
        

######################### Reset Password Request ###########################################
        
class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")
        return value

    def save(self):
        email = self.validated_data['email']
        user = User.objects.get(email=email)
        token = default_token_generator.make_token(user)
        from_email = settings.EMAIL_HOST_USER
        uid = user.pk
        reset_link = f"http://127.0.0.1:8000/api/account/reset-password/{uid}/{token}/"
        send_mail(
            'Password Reset Request',
            f'Please use the following link to reset your password: {reset_link}',
            from_email,
            [user.email],
            fail_silently=False,
        )        
        
########################### Reset Password ###########################################

class PasswordResetSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        try:
            uid = attrs['uid']
            print("Decoded UID:", uid)
            self.user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
            raise serializers.ValidationError("Invalid token or user ID.") from e
        
        if not default_token_generator.check_token(self.user, attrs['token']):
            raise serializers.ValidationError("Invalid token or user ID.")
        
        return attrs

    def save(self):
        self.user.set_password(self.validated_data['new_password'])
        self.user.save()
        
########################### Change Password ############################        

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True, required=True)


    def validate(self, value):
        old_password = value.get('old_password')
        new_password = value.get('new_password')
        confirm_password = value.get('confirm_password')
        usr = self.context['request'].user
        user = get_user_model().objects.filter(email=usr.email).first()
        print("user", usr)
        print("UserObject", user)
        
        if not user:
            raise serializers.ValidationError("User is not authenticated.")
        
        if new_password != confirm_password:
            raise serializers.ValidationError("New Password and Confirm Password did'nt Match.")
        
        if not user.check_password(old_password):
            raise serializers.ValidationError("Incorrect old password.")
        
        try:
            validate_password(new_password, user)
        except serializers.ValidationError as e:
            raise serializers.ValidationError(str(e))

        value['user'] = user
        return value

        

    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()


################## Profile Update Serializer ################################################

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'job', 'designation', 'countries', 'company', 
            'profile_picture', 'birth_date'
        ]

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = UserModel
        fields = [
            'email', 'first_name', 'middle_name', 'last_name', 
            'gender', 'date_of_birth', 'mobile', 'industry', 
            'category', 'linked_profile', 'contact_person_name', 
            'contact_person_number', 'profile'
        ]

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        profile = instance.profile

        # Update UserModel instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update Profile instance
        for attr, value in profile_data.items():
            setattr(profile, attr, value)
        profile.save()

        return instance