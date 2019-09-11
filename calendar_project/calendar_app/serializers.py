from django.contrib.auth.models import User
from .models import Request
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ['id', 'username', 'time_submitted', 'date_start',
            'date_end', 'all_day', 'status',
            'supervisor', 'reason', 'notes', 'denial_notes', 'authorized_by']

    def create(self, validated_data):
        supervisor = validated_data.pop('supervisor')
        request = Request.objects.create(**validated_data)
        request.supervisor.set(supervisor)
        request.save()
        return request

class CreateRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ['username', 'date_start',
            'date_end', 'all_day',
            'supervisor', 'reason', 'notes']

class UpdateRequestStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ['status', 'denial_notes']

class EditRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ['date_start',
            'date_end', 'all_day',
            'supervisor', 'reason', 'notes']

class SupervisorSerializer(serializers.Serializer):
    username = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()

class UserSerializer(serializers.Serializer):
    username = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    is_staff = serializers.BooleanField()

class CreateUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(max_length=32, required=True)
    first_name = serializers.CharField(max_length=52, required=True)
    last_name = serializers.CharField(max_length=64, required=True)

class SetAdminSerializer(serializers.Serializer):
    is_staff = is_staff = serializers.BooleanField(required=True)

class ForgotPasswordSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100, required=True)

class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=32, required=True)
    new_password = serializers.CharField(max_length=32, required=True)

class CustomerTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['isAuthenticated'] = True
        token['isAdminUser'] = user.is_staff
        token['has_tempPassword'] = user.has_tempPassword
        return token