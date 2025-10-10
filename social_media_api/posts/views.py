from rest_framework import viewsets, permissions, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .models import Post, Comment, Like
from .serializers import (PostSerializer, PostCreateSerializer, CommentSerializer, 
                         CommentCreateSerializer, LikeSerializer)
from .permissions import IsAuthorOrReadOnly

# Import notifications only if the app is installed
try:
    from notifications.models import Notification
    NOTIFICATIONS_ENABLED = True
except ImportError:
    NOTIFICATIONS_ENABLED = False

class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and managing posts.
    """
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['title', 'content']
    filterset_fields = ['author']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return PostCreateSerializer
        return PostSerializer
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def add_comment(self, request, pk=None):
        post = self.get_object()
        
        # Simple manual creation
        comment = Comment.objects.create(
            post=post,
            author=request.user,
            content=request.data.get('content', '')
        )
        
        if comment:
            # Create notification for post author if notifications are enabled
            if NOTIFICATIONS_ENABLED and post.author != request.user:
                Notification.objects.create(
                    recipient=post.author,
                    actor=request.user,
                    verb='comment',
                    target=post
                )
            
            serializer = CommentSerializer(comment, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            {'error': 'Could not create comment'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        user = request.user
        
        # Use get_or_create to handle like creation
        like, created = Like.objects.get_or_create(user=user, post=post)
        
        if created:
            # Create notification for post author if notifications are enabled
            if NOTIFICATIONS_ENABLED and post.author != user:
                Notification.objects.create(
                    recipient=post.author,
                    actor=user,
                    verb='like',
                    target=post
                )
            
            serializer = LikeSerializer(like, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {'error': 'You have already liked this post.'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def unlike(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        user = request.user
        
        try:
            like = Like.objects.get(post=post, user=user)
            like.delete()
            return Response(
                {'message': 'Post unliked successfully.'},
                status=status.HTTP_200_OK
            )
        except Like.DoesNotExist:
            return Response(
                {'error': 'You have not liked this post.'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def likes(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        likes = post.likes.all()
        serializer = LikeSerializer(likes, many=True, context={'request': request})
        return Response(serializer.data)

class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and managing comments.
    """
    queryset = Comment.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['post', 'author']
    
    def get_serializer_class(self):
        return CommentSerializer
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    def get_queryset(self):
        queryset = Comment.objects.all()
        post_id = self.request.query_params.get('post_id')
        if post_id:
            queryset = queryset.filter(post_id=post_id)
        return queryset

class LikeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing likes.
    """
    queryset = Like.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LikeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['post', 'user']
    
    def get_queryset(self):
        return Like.objects.filter(user=self.request.user)

class FeedView(APIView):
    """
    View to get posts from users that the current user follows
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Get users that the current user follows
        following_users = request.user.following.all()
        
        # Get posts from followed users, ordered by most recent first
        feed_posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
        
        # Pagination (using DRF's built-in pagination)
        page = self.paginate_queryset(feed_posts)
        if page is not None:
            serializer = PostSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        
        serializer = PostSerializer(feed_posts, many=True, context={'request': request})
        return Response(serializer.data)
    
    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            from rest_framework.pagination import PageNumberPagination
            self._paginator = PageNumberPagination()
            self._paginator.page_size = 10
        return self._paginator

    def paginate_queryset(self, queryset):
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        return self.paginator.get_paginated_response(data)

class PostLikeAPIView(generics.GenericAPIView):
    """
    Alternative API view for liking posts using generics
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LikeSerializer

    def post(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        user = request.user
        
        # Use get_or_create to handle like creation
        like, created = Like.objects.get_or_create(user=user, post=post)
        
        if created:
            # Create notification for post author if notifications are enabled
            if NOTIFICATIONS_ENABLED and post.author != user:
                Notification.objects.create(
                    recipient=post.author,
                    actor=user,
                    verb='like',
                    target=post
                )
            
            serializer = self.get_serializer(like)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {'error': 'You have already liked this post.'},
                status=status.HTTP_400_BAD_REQUEST
            )

class PostUnlikeAPIView(generics.GenericAPIView):
    """
    Alternative API view for unliking posts using generics
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        user = request.user
        
        try:
            like = Like.objects.get(post=post, user=user)
            like.delete()
            return Response(
                {'message': 'Post unliked successfully.'},
                status=status.HTTP_200_OK
            )
        except Like.DoesNotExist:
            return Response(
                {'error': 'You have not liked this post.'},
                status=status.HTTP_400_BAD_REQUEST
            )

class PostDetailView(generics.RetrieveAPIView):
    """
    Generic view for retrieving a single post
    """
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer

class PostLikesListView(generics.ListAPIView):
    """
    Generic view for listing likes of a specific post
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LikeSerializer

    def get_queryset(self):
        post_id = self.kwargs['pk']
        post = get_object_or_404(Post, pk=post_id)
        return post.likes.all()