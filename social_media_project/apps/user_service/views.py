from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import User
from rest_framework import status, views
from rest_framework.response import Response
from .serializers import UserLoginAPIViewSerializer
from .serializers import UserSerializer, UserCreateSerializer, UserUpdateSerializer,UserLoginAPIViewSerializer
from rest_framework.decorators import action

class UserViewSet(viewsets.ViewSet):
    queryset = User.objects.all()

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserSerializer

    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        context = {"message": "You have successfully fetched all the users", "data": serializer.data}
        return Response(context, status=status.HTTP_200_OK)

   
    def create(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            context = {"message": "Your account has been created successfuly", "data": serializer.data}
            return Response(context, status=status.HTTP_201_CREATED)
        context = {"message": "Something went wrong", "errors": serializer.errors}
        return Response(context, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            context = {"message": "Something went wrong", "error":"The user does not exist" }
            return Response(context, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        context = {"message": "You have successfully fetched user data", "data": serializer.data}
        return Response(context, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UserUpdateSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            serializer = UserSerializer(user)
            context = {"message": "You have successfully updated user data", "data": serializer.data}
            return Response(context, status=status.HTTP_200_OK)
        context = {"message": "Something went wrong", "error":serializer.errors}
        return Response(context, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            context = {"message": "Something went wrong", "error":"User does not exist"}
            return Response(context, status=status.HTTP_404_NOT_FOUND)
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            context = {"message": "You have successfully updated user data", "data": serializer.data}
            return Response(context, status=status.HTTP_200_OK)
        context = {"message": "Something went wrong", "error":serializer.errors}
        return Response(context, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    


class UserLoginAPIView(views.APIView):
    # permission_classes = ['AllowAny']
    def post(self, request, *args, **kwargs):
        serializer = UserLoginAPIViewSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

