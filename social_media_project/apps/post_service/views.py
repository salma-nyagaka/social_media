# post_service/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer

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
        serializer.save(user=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing blog comment instances.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def add_blog_comment(self, request, pk=None):
        """
        Add a comment to a specific blog post.
        """
        post = self.get_object()
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, post=post)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def perform_create(self, serializer):
        """
        Save the comment with the current user as the author.
        """
        serializer.save(user=self.request.user)
