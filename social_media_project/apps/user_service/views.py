import jwt
from rest_framework import viewsets, status, serializers
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime
from django.utils.timezone import make_aware
from django.shortcuts import render
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.core.cache import cache
from rest_framework.decorators import action

from ..notification_service.tasks import send_batch_notifications

from .serializers import (
    UserSerializer,
    UserCreateSerializer,
    UserUpdateSerializer,
    UserLoginAPIViewSerializer,
)
from .models import User, UserFollowing


class UserViewSet(viewsets.ViewSet):
    queryset = User.objects.all()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer
        elif self.action in ["update", "partial_update"]:
            return UserUpdateSerializer
        return UserSerializer

    def create(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete("users_list") 
            context = {
                "message": "Your account has been successfully created. Please activate your account by clicking the link sent to your email.",
                "data": serializer.data,
            }
            return Response(context, status=status.HTTP_201_CREATED)
        context = {"message": "Something went wrong", "errors": serializer.errors}
        return Response(context, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        cache_key = "users_list"
        cached_users = cache.get(cache_key)
        if cached_users is not None:
            return Response(cached_users, status=status.HTTP_200_OK)
        
        queryset = User.objects.filter(is_active=True)  # Filter for active users
        serializer = UserSerializer(queryset, many=True)
        context = {
            "message": "You have successfully fetched all active users",
            "data": serializer.data,
        }
  
        cache.set(cache_key, serializer.data, timeout=60*15)
        return Response(context, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        cache_key = f"user_{pk}"
        cached_user = cache.get(cache_key)
        if cached_user is not None:
            return Response(cached_user, status=status.HTTP_200_OK)

        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            context = {
                "message": "Something went wrong",
                "error": "The user does not exist",
            }
            return Response(context, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        context = {
            "message": "You have successfully fetched user data",
            "data": serializer.data,
        }
        cache.set(cache_key, context, timeout=60*15)  # Cache for 15 minutes
        return Response(context, status=status.HTTP_200_OK)

    def update_user(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
            serializer = UserUpdateSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                # Invalidate cache
                cache.delete(f"user_{pk}") 
                cache.delete("users_list") 
                context = {
                    "message": "You have successfully updated user data",
                    "data": serializer.data,
                }
                cache.set(f"user_{pk}", context, timeout=60*15)
                return Response(context, status=status.HTTP_200_OK)
            context = {"message": "Something went wrong", "error": serializer.errors}
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            context = {
                "message": "Something went wrong",
                "error": "User does not exist",
            }
            return Response(context, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            context = {
                "message": "Something went wrong",
                "error": "The user does not exist",
            }
            return Response(context, status=status.HTTP_404_NOT_FOUND)
        user.delete()
        # Invalidate cache
        cache.delete(f"user_{pk}") 
        cache.delete("users_list") 
        context = {"message": "You have successfully deleted the user data"}
        return Response(context, status=status.HTTP_204_NO_CONTENT)

    def get_current_user(self, request):
        serializer = UserSerializer(request.user)
        context = {
            "message": "You have successfully fetched user data",
            "data": serializer.data,
        }
        return Response(context, status=status.HTTP_200_OK)

    def follow(self, request, pk=None):
        user_to_follow = get_object_or_404(User, pk=pk)
        user = request.user
        if user == user_to_follow:
            return Response(
                {"status": "You cannot follow yourself"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if UserFollowing.objects.filter(
            user_id=user, following_user_id=user_to_follow
        ).exists():
            return Response(
                {"status": "You are already following this user"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if user != user_to_follow:
            UserFollowing.objects.create(user_id=user, following_user_id=user_to_follow)
            context = {
                "message": "You have successfully followed {}".format(
                    user_to_follow.username
                )
            }
            send_batch_notifications.delay(
                subject="New follow alert!",
                message="You have been followed by {}".format(user.email),
                recipient_list=[user_to_follow.email],
                context={},
                html_template="follow.html",
                notification_type="follow",
            )

            return Response(context, status=status.HTTP_200_OK)
        else:
            return Response(
                {"status": "You cannot follow yourself"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def unfollow(self, request, pk=None):
        user_to_unfollow = get_object_or_404(User, pk=pk)
        user = request.user
        if user == user_to_unfollow:
            return Response(
                {"status": "You cannot unfollow yourself"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not UserFollowing.objects.filter(
            user_id=user, following_user_id=user_to_unfollow
        ).exists():
            return Response(
                {"status": "You are not following this user"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if user != user_to_unfollow:
            UserFollowing.objects.filter(
                user_id=user, following_user_id=user_to_unfollow
            ).delete()
            context = {
                "message": "You have successfully unfollowed {}".format(
                    user_to_unfollow.username
                )
            }
            return Response(context, status=status.HTTP_200_OK)
        else:
            return Response(
                {"status": "You cannot unfollow yourself"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def followers(self, request, pk=None):
        user = get_object_or_404(User, pk=4)
        followers = User.objects.filter(following__following_user_id=user)
        serializer = UserSerializer(followers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserLoginAPIViewSerializer(
            data=request.data, context={"request": request}
        )
        try:
            if serializer.is_valid(raise_exception=True):
                return Response(serializer.validated_data, status=status.HTTP_200_OK)
        except serializers.ValidationError as e:
            # Extract the detail of the error
            error_detail = e.detail
            if isinstance(error_detail, list):
                # If it's a list, it means there's a top-level error message
                error_response = {
                    "message": "Something went wrong",
                    "errors": {"non_field_errors": error_detail},
                }
            else:
                error_response = {
                    "message": error_detail.get("message", "Something went wrong"),
                    "errors": error_detail.get("errors", {}),
                }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)


class ActivateAccountAPIView(APIView):
    permission_classes = []  # Allow any

    def get(self, request, token, *args, **kwargs):
        try:
            decoded_token = jwt.decode(token, options={"verify_signature": False})
            user = User.objects.get(pk=decoded_token["user_id"])
        except (jwt.exceptions.DecodeError, User.DoesNotExist):
            user = None

        if user is not None:
            exp = datetime.fromtimestamp(decoded_token["exp"])
            exp_aware = make_aware(exp)

            if timezone.now() <= exp_aware:
                user.is_active = True
                user.save()
                activation_status = {
                    "message": "Your account has been activated successfully.",
                    "status": status.HTTP_200_OK,
                }
            else:
                activation_status = {
                    "message": "Activation link has expired.",
                    "status": status.HTTP_400_BAD_REQUEST,
                }
        else:
            activation_status = {
                "message": "User does not exist",
                "status": status.HTTP_404_NOT_FOUND,
            }

        context = {"activation_status": activation_status}
        return render(request, "activation_status.html", context)
