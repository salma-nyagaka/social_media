# post_service/views.py
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django.conf import settings
from django.core.cache import cache

from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from ..notification_service.tasks import send_batch_notifications
from ..user_service.models import User


class BlogPostViewSet(viewsets.ViewSet):
    """
    A viewset for viewing and editing blog post instances.
    """

    permission_classes = [IsAuthenticated]

    def list(self, request):
        cache_key = "posts_list"
        cached_posts = cache.get(cache_key)
        if cached_posts is not None:
            return Response(cached_posts, status=status.HTTP_200_OK)

        queryset = Post.objects.all()
        serializer = PostSerializer(queryset, many=True)
        response_data = {
            "message": "Post retrieved successfully",
            "data": serializer.data,
        }
        cache.set(cache_key, response_data, timeout=60 * 15)
        return Response(response_data, status=status.HTTP_200_OK)

    def create(self, request):
        """
        Create a new post.

        Args:
            request: The HTTP request containing the post data.

        Returns:
            Response: A response indicating the success or failure of the post creation.
        """
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            return self.perform_create(serializer)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, post_id=None):
        """
        Retrieve a post by its ID.

        Args:
            request: The HTTP request.
            post_id: The ID of the post to retrieve.

        Returns:
            Response: A response containing the post data or an error message.
        """

        cache_key = f"post_{post_id}"
        cached_post = cache.get(cache_key)

        try:
            post = Post.objects.get(pk=post_id)
            serializer = PostSerializer(post)
            response_data = {
                "message": "Post retrieved successfully",
                "data": serializer.data,
            }
            cache.set(cache_key, response_data, timeout=60 * 15)
            return Response(response_data, status=status.HTTP_200_OK)
        except Post.DoesNotExist as e:
            error_response = {"message": "Something went wrong", "errors": str(e)}
            return Response(error_response, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        """
        Update a post by its ID.

        Args:
            request: The HTTP request containing the updated post data.
            pk: The ID of the post to update.

        Returns:
            Response: A response indicating the success or failure of the post update.
        """

        try:
            post = Post.objects.get(pk=pk)
            if post.user != request.user:
                error_response = {"message": "You do not have ownership rights to edit this post."}
                return Response(error_response, status=status.HTTP_403_FORBIDDEN)
        

            serializer = PostSerializer(post, data=request.data)
            if serializer.is_valid():
                serializer.save()
                cache.delete(f"post_{pk}")
                cache.delete("posts_list")
                response_data = {
                    "message": "Post updated successfully",
                    "data": serializer.data,
                }
                cache.set(f"post_{pk}", response_data, timeout=60 * 15)
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
        """
        Delete a post by its ID.

        Args:
            request: The HTTP request.
            pk: The ID of the post to delete.

        Returns:
            Response: A response indicating the success or failure of the post deletion.
        """

        try:
            post = Post.objects.get(pk=pk)
            if post.user != request.user:
                error_response = {"message": "You do not have ownership rights to delete this post."}
                return Response(error_response, status=status.HTTP_403_FORBIDDEN)
        
        except Post.DoesNotExist as e:
            error_response = {"message": "Something went wrong", "errors": str(e)}
            return Response(error_response, status=status.HTTP_404_NOT_FOUND)

        post.delete()

        cache.delete(f"post_{pk}")
        cache.delete("posts_list")
        response_data = {"message": "Post deleted successfully"}
        return Response(response_data, status=status.HTTP_204_NO_CONTENT)

    def perform_create(self, serializer):
        """
        Save the post with the current user as the author and send notifications.

        Args:
            serializer: The serializer instance containing the post data.

        Returns:
            Response: A response indicating the success of the post creation.
        """
        title = serializer.validated_data.get("title", "No topic")
        post_id = serializer.validated_data.get("id", "No id")
        if title:
            # Get the email addresses of the users who follow the author of the post
            receiver_emails = list(
                User.objects.filter(
                    is_active=True,
                    followers__user_id=self.request.user.id
                ).values_list("email", flat=True)
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

        # Invalidate the posts list cache
        cache.delete("posts_list")

        return Response(response_data, status=status.HTTP_201_CREATED)


class CommentViewSet(viewsets.ViewSet):
    """
    A viewset for viewing and editing blog comment instances.
    """

    permission_classes = [IsAuthenticated]

    def list(self, request):
        """
        Retrieve all comments.
        """
        cache_key = "comments_list"
        cached_comments = cache.get(cache_key)
        if cached_comments is not None:
            return Response(cached_comments, status=status.HTTP_200_OK)

        queryset = Comment.objects.all()
        serializer = CommentSerializer(queryset, many=True)
        response_data = {
            "message": "Comments retrieved successfully",
            "data": serializer.data,
        }
        cache.set(cache_key, response_data, timeout=60 * 15)
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
        Retrieves a single comment.
        """

        cache_key = f"comment_{pk}"
        cached_comment = cache.get(cache_key)
        if cached_comment is not None:
            return Response(cached_comment, status=status.HTTP_200_OK)

        try:
            comment = Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CommentSerializer(comment)
        response_data = {
            "message": "Comment retrieved successfully",
            "data": serializer.data,
        }
        cache.set(cache_key, response_data, timeout=60 * 15)
        return Response(response_data, status=status.HTTP_200_OK)

    def update(self, request, comment_id=None):
        """
        Update an existing comment.
        """

        try:
            comment = Comment.objects.get(pk=comment_id)
            if comment.user != request.user:
                error_response = {"message": "You do not have ownership rights to update this comment"}
                return Response(error_response, status=status.HTTP_403_FORBIDDEN)

            serializer = CommentSerializer(comment, data=request.data)
            if serializer.is_valid():
                serializer.save()
                cache.delete(f"comment_{comment_id}")
                cache.delete("comments_list")
                response_data = {
                    "message": "Comment updated successfully",
                    "data": serializer.data,
                }

                cache.set(f"comment_{comment_id}", response_data, timeout=60 * 15)
                return Response(response_data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Comment.DoesNotExist as e:
            error_response = {"message": "Something went wrong", "errors": str(e)}
            return Response(error_response, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, comment_id=None):
        """
        Delete a comment.
        """
        try:
            comment = Comment.objects.get(pk=comment_id)
            if comment.user != request.user:
                error_response = {"message": "You do not have ownership rights to delete this comment"}
                return Response(error_response, status=status.HTTP_403_FORBIDDEN)
        except Comment.DoesNotExist as e:
            error_response = {"message": "Something went wrong", "errors": str(e)}
            return Response(error_response, status=status.HTTP_404_NOT_FOUND)
        comment.delete()
        cache.delete(f"comment_{comment_id}")
        cache.delete("comments_list")
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
                # Get the email addresses of the users who follow the author of the post
                receiver_emails = list(
                    User.objects.filter(
                        is_active=True,
                        followers__user_id=self.request.user.id
                    ).values_list("email", flat=True)
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
            # Invalidate the comments list cache
            cache.delete("comments_list")
            return Response(response_data, status=status.HTTP_201_CREATED)
        except Exception as e:
            error_response = {
                "message": "Something went wrong",
                "errors": {"detail": str(e)},
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)
