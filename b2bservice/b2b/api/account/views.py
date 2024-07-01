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
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import permissions, status as drf_status
import base64
from rest_framework import viewsets

from django.utils.encoding import force_bytes
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

# Create your views here.

User = get_user_model()


###################### Custom Obtain Token #############################

# class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
#     def get_token(self, user):
#         token = super().get_token(user)

#         # Add custom claims
#         token['user_id'] = base64.b64encode(force_bytes(str(user.id))).decode('utf-8')
#         token['email'] = base64.b64encode(force_bytes(user.email)).decode('utf-8')
#         try:
#             profile_image_url = user.profile.profile_picture.url
#         except Profile.DoesNotExist:
#             profile_image_url = None
#         token['profile_image'] = base64.b64encode(force_bytes(profile_image_url)).decode('utf-8')

#         return token

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def get_token(self, user):
        token = super().get_token(user)

        # Add custom claims without base64 encoding
        token['user_id'] = user.id
        token['email'] = user.email
        token['industry'] = user.industry.name
        try:
            profile_image_url = user.profile.profile_picture.url
        except Profile.DoesNotExist:
            profile_image_url = None
        token['profile_image'] = profile_image_url

        return token



class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

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
        response_status = 0
        errors = []
        data = {}

        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(email=email, password=password)

            if user:
                refresh = RefreshToken.for_user(user)
                access = CustomTokenObtainPairSerializer().get_token(user).access_token

                data = {
                    'refresh': str(refresh),
                    'access': str(access)
                }

                response_status = 1
                return Response({"status": response_status, 'data': data, "errors": errors}, status=drf_status.HTTP_200_OK)
            else:
                errors.append("Username or password is not correct")
                return Response({"status": response_status, 'data': data, "errors": errors}, status=drf_status.HTTP_401_UNAUTHORIZED)
        else:
            validation_errors = []
            for k in serializer.errors:
                validation_errors.append("{}: {}".format(k, serializer.errors.get(k)[0]))
            errors = validation_errors
            return Response({"status": response_status, 'data': data, "errors": errors}, status=drf_status.HTTP_400_BAD_REQUEST)



    

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
    
    

class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()   
    
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def current_user(self, request):
        if request.user.is_authenticated:
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)
        else:
            return Response({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)