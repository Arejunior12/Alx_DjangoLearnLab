from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils import timezone

class Notification(models.Model):
    # Notification types
    FOLLOW = 'follow'
    LIKE = 'like'
    COMMENT = 'comment'
    MENTION = 'mention'
    
    NOTIFICATION_TYPES = [
        (FOLLOW, 'Follow'),
        (LIKE, 'Like'),
        (COMMENT, 'Comment'),
        (MENTION, 'Mention'),
    ]
    
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='actions'
    )
    verb = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    read = models.BooleanField(default=False)
    
    # Generic Foreign Key for the target object (post, comment, etc.)
    target_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    target_object_id = models.PositiveIntegerField(null=True, blank=True)
    target = GenericForeignKey('target_content_type', 'target_object_id')
    
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['recipient', 'read']),
            models.Index(fields=['timestamp']),
        ]
    
    def __str__(self):
        return f"{self.actor.username} {self.verb} - {self.recipient.username}"
    
    def mark_as_read(self):
        self.read = True
        self.save()
    
    @classmethod
    def create_notification(cls, recipient, actor, verb, target=None):
        """Helper method to create notifications"""
        notification = cls(
            recipient=recipient,
            actor=actor,
            verb=verb,
            target=target
        )
        notification.save()
        return notification