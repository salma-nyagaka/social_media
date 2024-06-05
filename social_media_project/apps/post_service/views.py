# post_service/views.py
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer

# from social_media_project.apps.notification_service.kafka_utils import send_notification_to_kafka
from ..notification_service.tasks import send_email_task, send_batch_notifications
from ..user_service.models import User
from django.conf import settings


class BlogPostViewSet(viewsets.ViewSet):
    """
    A viewset for viewing and editing blog post instances.
    """

    permission_classes = [IsAuthenticated]

    def list(self, request):
        queryset = Post.objects.all()
        serializer = PostSerializer(queryset, many=True)
        response_data = {
            "message": "Post retrieved successfully",
            "data": serializer.data,
        }

        return Response(response_data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            return self.perform_create(serializer)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist as e:
            error_response = {"message": "Something went wrong", "errors": str(e)}
            return Response(error_response, status=status.HTTP_404_NOT_FOUND)
        serializer = PostSerializer(post)
        response_data = {
            "message": "Post retriEved successfully",
            "data": serializer.data,
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        try:
            post = Post.objects.get(pk=pk)
            serializer = PostSerializer(post, data=request.data)
            if serializer.is_valid():
                serializer.save()
                response_data = {
                    "message": "Post updated successfully",
                    "data": serializer.data,
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                error_response = {
                    "message": "Something went wrong",
                    "errors": serializer.errors,
                }
                return Response(error_response, status=status.HTTP_400_BAD_REQUEST)
        except Post.DoesNotExist as e:
            error_response = {"message": "Something went wrong", "errors": str(e)}
            return Response(error_response, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist as e:
            error_response = {"message": "Something went wrong", "errors": str(e)}
            return Response(error_response, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            error_response = {"message": "Something went wrong", "errors": str(e)}
            return Response(error_response, status=status.HTTP_404_NOT_FOUND)

        post.delete()
        response_data = {"message": "Post deleted successfully"}
        return Response(response_data, status=status.HTTP_204_NO_CONTENT)

    def perform_create(self, serializer):
        """
        Save the post with the current user as the author and send notifications.
        """
        try:
            title = serializer.validated_data.get("title", "No topic")
            post_id = serializer.validated_data.get("id", "No id")
            if title:
                receiver_emails = list(
                    User.objects.filter(is_active=True).values_list("email", flat=True)
                )
                # Send email notification after post is created
                send_batch_notifications.delay(
                    subject="New Post Created",
                    message=f'A new post titled "{title}" has been created.',
                    recipient_list=receiver_emails,
                    context={
                        "post_url": "{}/blogs/{}/".format(settings.DOMAIN_NAME, post_id)
                    },
                    html_template="new_post.html",
                    notification_type="post",
                )
            post = serializer.save(user=self.request.user)
            response_data = {
                "message": "Post created successfully",
                "data": serializer.data,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        except Exception as e:
            error_response = {"message": "Something went wrong", "errors": str(e)}
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(viewsets.ViewSet):
    """
    A viewset for viewing and editing blog comment instances.
    """

    permission_classes = [IsAuthenticated]

    def list(self, request):
        """
        Retrieve all comments.
        """
        queryset = Comment.objects.all()
        serializer = CommentSerializer(queryset, many=True)
        response_data = {
            "message": "Comments retrieved successfully",
            "data": serializer.data,
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def create(self, request):
        """
        Create a new comment.
        """
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            return self.perform_create(serializer)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """
        Retrieve a single comment.
        """
        try:
            comment = Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CommentSerializer(comment)
        response_data = {
            "message": "Comment retrieved successfully",
            "data": serializer.data,
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        """
        Update an existing comment.
        """

        try:
            comment = Comment.objects.get(pk=pk)
            serializer = CommentSerializer(comment, data=request.data)
            if serializer.is_valid():
                serializer.save()
                response_data = {
                    "message": "Comment updated successfully",
                    "data": serializer.data,
                }
                return Response(response_data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Comment.DoesNotExist as e:
            error_response = {"message": "Something went wrong", "errors": str(e)}
            return Response(error_response, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        """
        Delete a comment.
        """
        try:
            comment = Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        comment.delete()
        return Response(
            {"message": "Comment deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )

    def perform_create(self, serializer):
        """
        Save the comment with the current user as the author and send notifications.
        """
        try:
            post = serializer.validated_data.get("post", "no post")
            content = serializer.validated_data.get("content", "no content")
            comment_id = serializer.validated_data.get("id", "no comment")
            # Save the comment and get the ID from the saved instance
            comment = serializer.save(user=self.request.user)
            comment_id = comment.id

            if post.title:
                receiver_emails = list(
                    User.objects.filter(is_active=True).values_list("email", flat=True)
                )
                send_batch_notifications.delay(
                    subject="New comment has been added to the post: {}".format(
                        post.title
                    ),
                    message=content,
                    recipient_list=receiver_emails,
                    context={
                        "post_url": "{}/blogs/{}/".format(
                            settings.DOMAIN_NAME, comment_id
                        )
                    },
                    html_template="new_comment.html",
                    notification_type="comment",
                )
            response_data = {
                "message": "Comment created successfully",
                "data": serializer.data,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        except Exception as e:
            error_response = {
                "message": "Something went wrong",
                "errors": {"detail": str(e)},
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)
