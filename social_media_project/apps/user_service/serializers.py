from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.db import transaction
from django.conf import settings
import datetime
from datetime import datetime, timedelta
import jwt

from .models import User
from ..notification_service.tasks import send_email_task, send_batch_notifications
# ["id", "username", "email", "first_name", "last_name", "is_active",

class UserSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()


    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "is_active",'followers_count', 'following_count', 'followers', 'following']

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count()

    def get_followers(self, obj):
        followers = obj.followers.all()
        return [{'user_id': follower.following_user_id.id, 'username': follower.following_user_id.username, "user_follow_id": follower.id} for follower in followers]

    def get_following(self, obj):
        following = obj.following.all()
        return [{'user_id': followee.following_user_id.id, 'username': followee.following_user_id.username, "user_follow_id": followee.id} for followee in following]
    
    
class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "first_name", "last_name"]
        extra_kwargs = {"password": {"write_only": True}}

    @transaction.atomic()
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        exp = datetime.utcnow() + timedelta(hours=24)
        token = jwt.encode(
            {"user_id": user.id, "exp": exp}, settings.SECRET_KEY, algorithm="HS256"
        )

        domain = settings.DOMAIN_NAME
        send_batch_notifications.delay(
            subject="New account created",
            message="",
            recipient_list=[user.email],
            context={
                "context": "{}/users/email_confirmation/{}".format(domain, str(token))
            },
            html_template="activation_email.html",
            notification_type="registration",
        )

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
                {
                    "message": "Something went wrong",
                    "errors": {"username": ["Username is required"]},
                }
            )
        if not password:
            raise serializers.ValidationError(
                {
                    "message": "Something went wrong",
                    "errors": {"password": ["Password is required"]},
                }
            )

        user = authenticate(
            request=self.context.get("request"), username=username, password=password
        )

        if not user:
            raise serializers.ValidationError(
                {
                    "message": "Something went wrong",
                    "errors": {
                        "username": ["Invalid credentials or user account is disabled"]
                    },
                }
            )

        if not user.is_active:
            raise serializers.ValidationError(
                {
                    "message": "Something went wrong",
                    "errors": {"username": ["User account is disabled"]},
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
