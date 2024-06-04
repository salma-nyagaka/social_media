# post_service/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
# from social_media_project.apps.notification_service.kafka_utils import send_notification_to_kafka
from ..notification_service.tasks import send_email_task
from ..user_service.models import User
from django.conf import settings

class BlogPostViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing blog post instances.
    """
    
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Save the post with the current user as the author.
        """

        title = serializer.validated_data.get('title', 'No topic')  
        post_id = serializer.validated_data.get('post_id', 'No id')  
        if title:
            receiver_emails = list(User.objects.filter(is_active=True).values_list('email', flat=True))
            # Send email notification after post is created
            send_email_task.delay(
                subject='New Post Created',
                message=f'A new post titled "{title}" has been created.',
                from_email='salmanyagaka@gmail.com',
                recipient_list=[],
                html_template='new_post.html',
                context={'post_url': '{}/posts/posts/{}/'.format(settings.DOMAIN_NAME,post_id)},
                bcc=receiver_emails
            )
        serializer.save(user=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing blog comment instances.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]


    def perform_create(self, serializer):
        """
        Save the comment with the current user as the author.
        """
        post =  serializer.validated_data.get('post', 'no post')
        content = serializer.validated_data.get('content', 'no content')
        comment_id = serializer.validated_data.get('id', 'no comment')
        # Save the comment and get the ID from the saved instance
        comment = serializer.save(user=self.request.user)
        comment_id = comment.id
        
        if post.title:
            receiver_emails = list(User.objects.filter(is_active=True).values_list('email', flat=True))
            send_email_task.delay(
                subject='New comment has been added to the post: {}'.format(post.title),
                message=content,
                from_email='salmanyagaka@gmail.com',
                recipient_list=[],
                html_template='new_comment.html',
                context={'post_url': '{}/blogs/comments/{}/'.format(settings.DOMAIN_NAME, comment_id)},
                bcc=receiver_emails
            )

