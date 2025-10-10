from rest_framework import status, permissions, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from .models import CustomUser
from .serializers import (UserRegistrationSerializer, UserLoginSerializer, 
                         UserProfileSerializer, FollowSerializer)

# Import notifications only if the app is installed
try:
    from notifications.models import Notification
    NOTIFICATIONS_ENABLED = True
except ImportError:
    NOTIFICATIONS_ENABLED = False

class UserRegistrationView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'message': 'User registered successfully',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                },
                'token': token.key
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'message': 'Login successful',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                },
                'token': token.key
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user, context={'request': request})
        return Response(serializer.data)

    def put(self, request):
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        target_user = get_object_or_404(CustomUser, id=user_id)
        
        if target_user == request.user:
            return Response(
                {'error': 'You cannot follow yourself.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if request.user.follow(target_user):
            # Create notification for the followed user using direct creation
            if NOTIFICATIONS_ENABLED:
                Notification.objects.create(
                    recipient=target_user,
                    actor=request.user,
                    verb='follow'
                )
            
            return Response({
                'message': f'You are now following {target_user.username}',
                'following': True,
                'followers_count': target_user.followers_count,
                'following_count': request.user.following_count
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': f'You are already following {target_user.username}'
            }, status=status.HTTP_400_BAD_REQUEST)

class UnfollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        target_user = get_object_or_404(CustomUser, id=user_id)
        
        if request.user.unfollow(target_user):
            return Response({
                'message': f'You have unfollowed {target_user.username}',
                'following': False,
                'followers_count': target_user.followers_count,
                'following_count': request.user.following_count
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': f'You are not following {target_user.username}'
            }, status=status.HTTP_400_BAD_REQUEST)

class UserFollowingListView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get(self, request):
        following_users = request.user.following.all()
        serializer = self.get_serializer(following_users, many=True, context={'request': request})
        return Response({
            'count': following_users.count(),
            'following': serializer.data
        })

class UserFollowersListView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get(self, request):
        followers = request.user.followers.all()
        serializer = self.get_serializer(followers, many=True, context={'request': request})
        return Response({
            'count': followers.count(),
            'followers': serializer.data
        })

class UserListView(generics.GenericAPIView):
    """View for listing all users (for discovery)"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get(self, request):
        users = CustomUser.objects.all().exclude(id=request.user.id)
        serializer = self.get_serializer(users, many=True, context={'request': request})
        return Response({
            'count': users.count(),
            'users': serializer.data
        })

class UserDetailView(generics.GenericAPIView):
    """View for getting specific user details"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        serializer = self.get_serializer(user, context={'request': request})
        return Response(serializer.data)