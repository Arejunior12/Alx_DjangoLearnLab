from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (PostViewSet, CommentViewSet, LikeViewSet, FeedView,
                   PostLikeAPIView, PostUnlikeAPIView)

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'likes', LikeViewSet, basename='like')

urlpatterns = [
    path('', include(router.urls)),
    path('feed/', FeedView.as_view(), name='feed'),
    # Alternative endpoints using generics
    path('posts/<int:pk>/like-alt/', PostLikeAPIView.as_view(), name='post-like-alt'),
    path('posts/<int:pk>/unlike-alt/', PostUnlikeAPIView.as_view(), name='post-unlike-alt'),
]