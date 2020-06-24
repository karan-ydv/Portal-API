from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

from rest_framework_jwt.views import ObtainJSONWebToken
from rest_framework_jwt.settings import api_settings

from django.contrib.auth.models import User
from .models import Profile
from exam.models import Test
from .serializers import ProfileSerializer, RegistrationSerializer

from django.contrib.auth import authenticate

class ProfileView(APIView):
    """
    Lists profile info
    """

    def get(self, request, format=None):
        try:
            profile = request.user.profile
        except:
            return Response(data={"profile" : "user does not have a profile"},
             status=status.HTTP_404_NOT_FOUND)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)
    
@api_view(['POST'])
@permission_classes([IsAdminUser])
def RegistrationView(request):
    """
    Register API
    """
    permission_classes = [AllowAny]
    serializer = RegistrationSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        password = serializer.validated_data['password']
        password2 = serializer.validated_data['password2']

        if( password!=password2 ):
            data['password']="passwords don't match"
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        form_data = serializer.validated_data
        user = User(
            username=form_data['student_number'],
            first_name = form_data['first_name'],
            last_name = form_data.get('last_name',''),
            email = form_data['email']
        )
        user.set_password(password)
        user.username = serializer.validated_data['student_number']
        try:
            user.save()
        except:
            return Response(data={'data':'failed', 'student_number':'already exists'}, status=status.HTTP_400_BAD_REQUEST)
    
        profile = Profile(user=user)
        profile.branch = serializer.validated_data['branch']
        profile.student_number = serializer.validated_data['student_number']
        profile.save()

        try:
            test = Test.objects.all()[0]
            profile.tests.add(test)
        except:
            pass

        data['response'] = "successfully registered new user"
        data['studentNumber'] = profile.student_number
        data['email'] = profile.user.email
    else:
        data = serializer.errors
    return Response(data)

@api_view(['POST'])
@permission_classes([AllowAny])
def AdminLoginView(request):
    errors = {}
    try:
        username = request.data.get('username', 0)
        assert username
    except:
        errors['username'] = "username is required"
    try:
        password = request.data.get('password', 0)
        assert password
    except:
        errors['password'] = "password is required"
    
    if errors:
        return Response(data=errors,status=status.HTTP_400_BAD_REQUEST)
    try:
        user = authenticate(username=username, password=password)
        if user is not None and user.is_staff:
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            return Response(data = {"token" : token})
        else:
            errors['data'] = 'failed'
            errors['message'] = 'unable to authenticate with given credentials'
    except:
            errors['data'] = 'failed'
            errors['message'] = 'unable to authenticate with given credentials'
    return Response(data=errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated&IsAdminUser])
def StudentLoginView(request):
    errors = {}
    try:
        username = request.data.get('rollNo', 0)
        assert username
    except:
        errors['rollNo'] = "rollNo is required"
    try:
        password = request.data.get('password', 0)
        assert password
    except:
        errors['password'] = "password is required"
    
    if errors:
        return Response(data=errors,status=status.HTTP_400_BAD_REQUEST)
    try:
        user = authenticate(username=username, password=password)
        if user is not None :
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            return Response(data = {"token" : token})
        else:
            errors['data'] = 'failed'
            errors['message'] = 'unable to authenticate with given credentials'
    except:
            errors['data'] = 'failed'
            errors['message'] = 'unable to authenticate with given credentials'
    return Response(data=errors,status=status.HTTP_400_BAD_REQUEST)  
    