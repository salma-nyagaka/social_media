from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.db import transaction
from django.contrib.sites.shortcuts import get_current_site
from .utils import send_activation_email
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "is_active"]
        read_only_fields = ["id", "is_active"]


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "first_name", "last_name"]
        extra_kwargs = {"password": {"write_only": True}}

    @transaction.atomic()
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        send_activation_email(user)
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "username", "first_name", "last_name"]


class UserLoginAPIViewSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        if not username:
            raise serializers.ValidationError(
                {"message": "Something went wrong", "errors": "Username is required"}
            )
        if not password:
            raise serializers.ValidationError(
                {"message": "Something went wrong", "errors": "Password is required"}
            )

        user = authenticate(
            request=self.context.get("request"), username=username, password=password
        )
        # import pdb
        # pdb.set_trace(  )

        if not user:
            raise serializers.ValidationError(
                {"message": "Something went wrong", "errors": "Invalid credentials"}
            )
        if not user.is_active:
            raise serializers.ValidationError(
                {
                    "message": "Something went wrong",
                    "errors": "User account is disabled",
                }
            )

        refresh = RefreshToken.for_user(user)
        context = {
            "message": "You have successfully logged in",
            "data": {
                "username": user.username,
                "email": user.email,
                "token": str(refresh.access_token),
            },
        }

        return context
