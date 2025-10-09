from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Post, Comment

User = get_user_model()

class PostTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='testpass123'
        )
        self.post = Post.objects.create(
            author=self.user,
            title='Test Post',
            content='This is a test post content'
        )
        self.client.force_authenticate(user=self.user)
    
    def test_create_post(self):
        url = '/api/posts/'
        data = {
            'title': 'New Test Post',
            'content': 'Content of new test post'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 2)
    
    def test_update_own_post(self):
        url = f'/api/posts/{self.post.id}/'
        data = {'title': 'Updated Title'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Updated Title')
    
    def test_cannot_update_others_post(self):
        self.client.force_authenticate(user=self.other_user)
        url = f'/api/posts/{self.post.id}/'
        data = {'title': 'Unauthorized Update'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class CommentTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.post = Post.objects.create(
            author=self.user,
            title='Test Post',
            content='Test content'
        )
        self.comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            content='Test comment'
        )
        self.client.force_authenticate(user=self.user)
    
    def test_add_comment_to_post(self):
        url = f'/api/posts/{self.post.id}/add_comment/'
        data = {'content': 'New test comment'}
        response = self.client.post(url, data)
        print(f"Response status: {response.status_code}")  # Debug line
        print(f"Response data: {response.data}")  # Debug line
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.post.comments.count(), 2)
    
    def test_create_comment_directly(self):
        url = '/api/comments/'
        data = {
            'post': self.post.id,
            'content': 'Direct comment'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 2)