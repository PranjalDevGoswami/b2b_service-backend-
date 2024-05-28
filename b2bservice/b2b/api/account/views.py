from django.shortcuts import render
from api.account.permissions import IsActive
from rest_framework.views import APIView
from rest_framework import permissions, authentication
from rest_framework.permissions import AllowAny,IsAuthenticated
from django.contrib.auth import get_user_model, authenticate, login
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.contrib.auth import logout
from .serializers import *
from rest_framework import status
from rest_framework import generics
from api.account.permissions import IsActive
from django.contrib.auth import logout
# Create your views here.

User = get_user_model()

################### B2B User Registration API Views ####################

class B2bUserRegistration(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = B2BUserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)




################### B2B User Login API Views ############################

class B2BUserLogin(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        status = 0
        errors = []
        data = {}
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(email=email, password=password)
            print("################", user)
            if user:
                data = LoginSerializer(user).data
                print("data", data)
                status = 1
            else:
                errors.append("username or password is not correct")
        else:
            validation_errors = []
            for k in serializer.errors:
                validation_errors.append("{}: {}".format(k,serializer.errors.get(k)[0]))
            errors = validation_errors

        return Response({"status": status, 'data':data, "errors": errors})
    

##################### Password Reset Request API Views ######################################

class PasswordResetRequestView(generics.GenericAPIView):
    serializer_class = PasswordResetRequestSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Password reset email has been sent."}, status=status.HTTP_200_OK)    



###################### Password Reset API Views ############################################


class PasswordResetView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, uid, token, *args, **kwargs):
        print("Received UID:", uid)
        print("Received Token:", token)
        serializer = self.get_serializer(data={
            'uid': uid,
            'token': token,
            'new_password': request.data['new_password']
        })
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)


####################### Change Password API Views ##########################################

class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.AllowAny]

    def get_object(self, queryset=None):
        return self.request.user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password has been changed successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





####################### Profile Update API VIEW ####################################
class UserProfileUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def put(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)




##########################  Logout API VIEW #########################################

class Logout(APIView):
    def post(self, request):
        # Perform logout operation
        logout(request)
        return Response({"message": "Logged out successfully"})