from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, LikeViewSet, FeedView, PostLikeGenericView

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'likes', LikeViewSet, basename='like')

urlpatterns = [
    path('', include(router.urls)),
    path('feed/', FeedView.as_view(), name='feed'),
    path('posts/<int:pk>/like-generic/', PostLikeGenericView.as_view(), name='post-like-generic'),
]