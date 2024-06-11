# post_service/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BlogPostViewSet, CommentViewSet


# Individual views for each action on BlogPostViewSet
create_post = BlogPostViewSet.as_view({"post": "create"})
retrieve = BlogPostViewSet.as_view({"get": "retrieve"})
retrieve_all = BlogPostViewSet.as_view({"get": "list"})
delete_post = BlogPostViewSet.as_view({"delete": "destroy"})
update_post = BlogPostViewSet.as_view({"put": "update"})

# Individual views for each action on BlogPostViewSet CommentViewSet
list_comments = CommentViewSet.as_view({"get": "list"})
create_comment = CommentViewSet.as_view({"post": "create"})
retrieve_comment = CommentViewSet.as_view({"get": "retrieve"})
update_comment = CommentViewSet.as_view({"put": "update"})
delete_comment = CommentViewSet.as_view({"delete": "destroy"})


urlpatterns = [
    path("", create_post, name="create_post"),
    path("<int:post_id>/", retrieve, name="retrieve"),
    path("all/", retrieve_all, name="retrieve_all"),
    path("delete/<int:pk>/", delete_post, name="delete_post"),
    path("update/<int:pk>/", update_post, name="update_post"),
    path("comments/", create_comment, name="create_comment"),
    path("comments/all/", list_comments, name="list_comments"),
    path("comments/<int:pk>/", retrieve_comment, name="retrieve_comment"),
    path("comments/update/<int:comment_id>/", update_comment, name="update_comment"),
    path("comments/delete/<int:comment_id>/", delete_comment, name="delete_comment"),
]
