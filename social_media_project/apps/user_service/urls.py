from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import UserViewSet, UserLoginAPIView, activate_account

create_user = UserViewSet.as_view({"post": "create"})
list_users = UserViewSet.as_view({"get": "list"})
retrieve_user = UserViewSet.as_view({"get": "retrieve"})
update_user = UserViewSet.as_view({"put": "update"})
partial_update_user = UserViewSet.as_view({"patch": "partial_update"})
delete_user = UserViewSet.as_view({"delete": "destroy"})
get_current_user = UserViewSet.as_view({"get": "me"})

urlpatterns = [
    # path('admin/', admin.site.urls),
    path("create_user/", create_user, name="create_user"),
    path("login/", UserLoginAPIView.as_view(), name="user_login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("all/", list_users, name="list_users"),
    path("<int:pk>/", retrieve_user, name="retrieve_user"),
    # path('<int:pk>/', update_user, name='update_user'),
    path("update/<int:pk>/", partial_update_user, name="partial_update_user"),
    path("delete/<int:pk>/", delete_user, name="delete_user"),
    path("users/me/", get_current_user, name="get_current_user"),
    path("email_confirmation/<str:token>/", activate_account, name="activate_account"),
]
