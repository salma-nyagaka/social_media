# post_service/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from social_media_project.apps.notification_service.kafka_utils import send_notification_to_kafka

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
        title = serializer.validated_data.get('title', 'No topic provided')  
        if title:
            notification_data = {
                'type': 'post',
                'receiver_id': self.request.user.username,
                'message': f'New post created with title: {title}' 
            }
            send_notification_to_kafka(notification_data)
        serializer.save(user=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing blog comment instances.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    # @action(detail=True, methods=['post'])
    # def add_blog_comment(self, request, pk=None):
    #     """
    #     Add a comment to a specific blog post.
    #     """
    #     post = self.get_object()
    #     serializer = CommentSerializer(data=request.data)

    #     if serializer.is_valid():
    #         # title =  serializer.validated_data.get('post', 'no post')
    #         # notification_data = {
    #         #     'type': 'post',
    #         #     'receiver_id': self.request.user.username,
    #         #     'message': f'New post created with title: {title}' 
    #         # }
    #         # send_notification_to_kafka(notification_data)
        
    #         serializer.save(user=request.user, post=post)
    #         return Response(serializer.data, status=201)
    #     return Response(serializer.errors, status=400)

    def perform_create(self, serializer):
        """
        Save the comment with the current user as the author.
        """
        post =  serializer.validated_data.get('post', 'no post')
        if post.title:
            notification_data = {
                'type': 'post',
                'receiver_id': self.request.user.username,
                'message': f'New comments has been created for post with title: {post.title}' 
            }
        
            # import pdb
            # pdb.set_trace()
            send_notification_to_kafka(notification_data)
    
        serializer.save(user=self.request.user)
