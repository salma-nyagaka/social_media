import jwt
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import User
from rest_framework.response import Response
from datetime import datetime
from django.utils.timezone import make_aware
from django.shortcuts import render
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .serializers import (
    UserSerializer,
    UserCreateSerializer,
    UserUpdateSerializer,
    UserLoginAPIViewSerializer,
)
from .models import User


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

    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        context = {
            "message": "You have successfully fetched all the users",
            "data": serializer.data,
        }
        return Response(context, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            context = {
                "message": "Your account has been successfully created. Please activate your account by clicking the link sent to your email.",
                "data": serializer.data,
            }
            return Response(context, status=status.HTTP_201_CREATED)
        context = {"message": "Something went wrong", "errors": serializer.errors}
        return Response(context, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
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
        return Response(context, status=status.HTTP_200_OK)

    # def update(self, request, pk=None):
    #     try:
    #         user = User.objects.get(pk=pk)
    #     except User.DoesNotExist:
    #         return Response(status=status.HTTP_404_NOT_FOUND)
    #     serializer = UserUpdateSerializer(user, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         serializer = UserSerializer(user)
    #         context = {
    #             "message": "You have successfully updated user data",
    #             "data": serializer.data,
    #         }
    #         return Response(context, status=status.HTTP_200_OK)
    #     context = {"message": "Something went wrong", "error": serializer.errors}
    #     return Response(context, status=status.HTTP_400_BAD_REQUEST)

    def update_user(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            context = {
                "message": "Something went wrong",
                "error": "User does not exist",
            }
            return Response(context, status=status.HTTP_404_NOT_FOUND)
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            context = {
                "message": "You have successfully updated user data",
                "data": serializer.data,
            }
            return Response(context, status=status.HTTP_200_OK)
        context = {"message": "Something went wrong", "error": serializer.errors}
        return Response(context, status=status.HTTP_400_BAD_REQUEST)

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
        context = {"message": "You have successfully deleted the user data"}
        return Response(context, status=status.HTTP_204_NO_CONTENT)

    def get_current_user(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserLoginAPIViewSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        context = {"message": "Something went wrong", "errors": serializer.errors}
        return Response(context, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def activate_account(request, token):
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
