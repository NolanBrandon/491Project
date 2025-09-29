from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, UserMetrics, Goals

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirm')

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user

class UserMetricsSerializer(serializers.ModelSerializer):
    bmr = serializers.SerializerMethodField()
    tdee = serializers.SerializerMethodField()

    class Meta:
        model = UserMetrics
        fields = '__all__'

    def get_bmr(self, obj):
        return obj.calculate_bmr()

    def get_tdee(self, obj):
        return obj.calculate_tdee()

class GoalsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goals
        fields = '__all__'
