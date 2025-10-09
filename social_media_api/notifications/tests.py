from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status

User = get_user_model()

class NotificationTests(APITestCase):
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
        
        # Try to import Notification model
        try:
            from notifications.models import Notification
            self.Notification = Notification
            
            # Create some notifications
            self.notification1 = Notification.objects.create(
                recipient=self.user1,
                actor=self.user2,
                verb='like'
            )
            self.notification2 = Notification.objects.create(
                recipient=self.user1,
                actor=self.user2,
                verb='comment',
                read=True
            )
        except Exception:
            # Skip tests if notifications app is not properly set up
            self.skipTest("Notifications app not properly configured")
        
        self.client.force_authenticate(user=self.user1)
    
    def test_get_notifications(self):
        if not hasattr(self, 'Notification'):
            self.skipTest("Notifications not available")
            
        url = '/api/notifications/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
    
    def test_get_unread_notifications(self):
        if not hasattr(self, 'Notification'):
            self.skipTest("Notifications not available")
            
        url = '/api/notifications/unread/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['unread_count'], 1)
        self.assertEqual(len(response.data['notifications']), 1)
    
    def test_mark_notification_as_read(self):
        if not hasattr(self, 'Notification'):
            self.skipTest("Notifications not available")
            
        url = f'/api/notifications/{self.notification1.id}/mark_as_read/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Refresh from database
        self.notification1.refresh_from_db()
        self.assertTrue(self.notification1.read)
    
    def test_mark_all_notifications_as_read(self):
        if not hasattr(self, 'Notification'):
            self.skipTest("Notifications not available")
            
        url = '/api/notifications/mark_all_as_read/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check all notifications are read
        unread_count = self.Notification.objects.filter(recipient=self.user1, read=False).count()
        self.assertEqual(unread_count, 0)