from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import UserViewSet, UserLoginAPIView, ActivateAccountAPIView

create_user = UserViewSet.as_view({"post": "create"})
list_users = UserViewSet.as_view({"get": "list"})
retrieve_user = UserViewSet.as_view({"get": "retrieve"})
update_user = UserViewSet.as_view({"patch": "update_user"})
delete_user = UserViewSet.as_view({"delete": "destroy"})
get_current_user = UserViewSet.as_view({"get": "get_current_user"})
get_current_user = UserViewSet.as_view({"get": "get_current_user"})
follow = UserViewSet.as_view({"post": "follow"})
unfollow = UserViewSet.as_view({"post": "unfollow"})
followers = UserViewSet.as_view({"get": "followers"})


urlpatterns = [
    path("create_user/", create_user, name="create_user"),
    path("login/", UserLoginAPIView.as_view(), name="user_login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("update/<int:pk>/", update_user, name="update_user"),
    path("all/", list_users, name="list_users"),
    path("<int:pk>/", retrieve_user, name="retrieve_user"),
    path("delete/<int:pk>/", delete_user, name="delete_user"),
    path("users/my_profile/", get_current_user, name="get_current_user"),
    path(
        "email_confirmation/<str:token>/",
        ActivateAccountAPIView.as_view(),
        name="activate_account",
    ),
    path("get_current_user/", get_current_user, name="get_current_user"),
    path("follow/<int:pk>/", follow, name="follow"),
    path("unfollow/<int:pk>/", unfollow, name="unfollow"),
    path("followers/<int:pk>/", followers, name="followers"),
]
