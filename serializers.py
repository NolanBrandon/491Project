from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, UserProfile, UserMetrics, Goals

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password', 'password_confirm')

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        # Create empty profile
        UserProfile.objects.create(user=user)
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'bio']

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile']

class UserMetricsSerializer(serializers.ModelSerializer):
    bmr = serializers.SerializerMethodField()

    class Meta:
        model = UserMetrics
        fields = ['id', 'user', 'weight', 'height', 'age', 'bmr']
        read_only_fields = ['user']

    def get_bmr(self, obj):
        return obj.calculate_bmr()

class GoalsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goals
        fields = ['id', 'user', 'goal_type', 'target_value']
        read_only_fields = ['user']

