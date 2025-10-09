from rest_framework import serializers
from .models import Notification
from accounts.serializers import UserProfileSerializer

class NotificationSerializer(serializers.ModelSerializer):
    actor_details = UserProfileSerializer(source='actor', read_only=True)
    target_object = serializers.SerializerMethodField()
    
    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'actor', 'actor_details', 'verb', 
                 'read', 'target_object', 'timestamp']
        read_only_fields = ['id', 'timestamp']
    
    def get_target_object(self, obj):
        """Serialize the target object based on its type"""
        if obj.target:
            # You can customize this based on your target models
            if hasattr(obj.target, 'title'):  # For posts
                return {
                    'type': 'post',
                    'id': obj.target.id,
                    'title': obj.target.title
                }
            elif hasattr(obj.target, 'content'):  # For comments
                return {
                    'type': 'comment',
                    'id': obj.target.id,
                    'content': obj.target.content[:50] + '...' if len(obj.target.content) > 50 else obj.target.content
                }
        return None

class NotificationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['read']