from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, branches

class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    class Meta:
        model = Profile
        fields = ('user', 'first_name', 'last_name', 'student_number', 'branch', )

class RegistrationSerializer(serializers.ModelSerializer):
    
    password2 = serializers.CharField(style={'input_type':  'password'}, write_only=True)
    first_name = serializers.CharField(required=True)
    email  = serializer.CharField(required=True)
    student_number = serializers.IntegerField(max_value=1980000, min_value=1910000)
    branch = serializers.ChoiceField(choices = branches)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'student_number', 'branch', 'email', 'password', 'password2')
        extra_kwargs = {
            'password' : {'write_only' : True}
        }