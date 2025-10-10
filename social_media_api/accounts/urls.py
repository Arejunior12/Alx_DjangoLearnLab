from django.urls import path
from .views import (UserRegistrationView, UserLoginView, UserProfileView,
                   FollowUserView, UnfollowUserView, UserFollowingListView,
                   UserFollowersListView, UserListView, UserDetailView, health_check)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('follow/<int:user_id>/', FollowUserView.as_view(), name='follow-user'),
    path('unfollow/<int:user_id>/', UnfollowUserView.as_view(), name='unfollow-user'),
    path('following/', UserFollowingListView.as_view(), name='following-list'),
    path('followers/', UserFollowersListView.as_view(), name='followers-list'),
    path('users/', UserListView.as_view(), name='user-list'),  # New endpoint
    path('users/<int:user_id>/', UserDetailView.as_view(), name='user-detail'),  # New endpoint
    path('health/', health_check, name='health-check'),
]