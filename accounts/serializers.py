from rest_framework import serializers
from django.contrib.auth.models import User


class RegisterSerializer(serializers.ModelSerializer):
    # it basically used to take the values or inout from the usr or frontend from req.body
    name = serializers.CharField(max_length=255, required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['name', 'email', 'password']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("user already exists")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['email'],  
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['name'],
        )
        return user


class LoginSerializer(serializers.Serializer):
    #this serializer is used to login the users
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
