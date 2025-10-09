from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from posts.models import Post

User = get_user_model()

class FollowTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user1)
    
    def test_follow_user(self):
        url = f'/api/auth/follow/{self.user2.id}/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.user1.is_following(self.user2))
        self.assertEqual(response.data['following'], True)
    
    def test_cannot_follow_self(self):
        url = f'/api/auth/follow/{self.user1.id}/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_unfollow_user(self):
        # First follow the user
        self.user1.follow(self.user2)
        
        url = f'/api/auth/unfollow/{self.user2.id}/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(self.user1.is_following(self.user2))
        self.assertEqual(response.data['following'], False)

class UserListViewTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user1)
    
    def test_user_list_view(self):
        url = '/api/auth/users/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)  # Should exclude current user
        self.assertEqual(response.data['users'][0]['username'], 'user2')
    
    def test_user_detail_view(self):
        url = f'/api/auth/users/{self.user2.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'user2')

class FeedTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='testpass123'
        )
        self.user3 = User.objects.create_user(
            username='user3',
            email='user3@example.com',
            password='testpass123'
        )
        
        # Create posts
        self.post1 = Post.objects.create(
            author=self.user2,
            title='Post from user2',
            content='Content from user2'
        )
        self.post2 = Post.objects.create(
            author=self.user3,
            title='Post from user3',
            content='Content from user3'
        )
        
        self.client.force_authenticate(user=self.user1)
    
    def test_feed_with_followed_users(self):
        # User1 follows user2 but not user3
        self.user1.follow(self.user2)
        
        url = '/api/feed/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Should only see post from user2
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Post from user2')
    
    def test_empty_feed(self):
        # User1 doesn't follow anyone
        url = '/api/feed/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)