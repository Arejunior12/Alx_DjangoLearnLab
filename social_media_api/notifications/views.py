from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from django.db.models import Q
from .models import Notification
from .serializers import NotificationSerializer, NotificationUpdateSerializer

class NotificationViewSet(GenericViewSet):
    """
    ViewSet for managing notifications.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NotificationSerializer
    
    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)
    
    def list(self, request):
        """Get all notifications for the current user"""
        notifications = self.get_queryset()
        
        # Filter by read status if provided
        read_param = request.query_params.get('read')
        if read_param is not None:
            if read_param.lower() == 'true':
                notifications = notifications.filter(read=True)
            elif read_param.lower() == 'false':
                notifications = notifications.filter(read=False)
        
        # Pagination
        page = self.paginate_queryset(notifications)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(notifications, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def unread(self, request):
        """Get unread notifications count and list"""
        unread_notifications = self.get_queryset().filter(read=False)
        unread_count = unread_notifications.count()
        
        # Get recent unread notifications
        recent_unread = unread_notifications[:10]  # Last 10 unread
        
        serializer = self.get_serializer(recent_unread, many=True)
        return Response({
            'unread_count': unread_count,
            'notifications': serializer.data
        })
    
    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        """Mark a specific notification as read"""
        notification = self.get_object()
        notification.mark_as_read()
        return Response({'message': 'Notification marked as read.'})
    
    @action(detail=False, methods=['post'])
    def mark_all_as_read(self, request):
        """Mark all notifications as read"""
        updated_count = self.get_queryset().filter(read=False).update(read=True)
        return Response({
            'message': f'Marked {updated_count} notifications as read.'
        })
    
    def retrieve(self, request, pk=None):
        """Get a specific notification and mark it as read"""
        notification = self.get_object()
        if not notification.read:
            notification.mark_as_read()
        serializer = self.get_serializer(notification)
        return Response(serializer.data)
    
    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            from rest_framework.pagination import PageNumberPagination
            self._paginator = PageNumberPagination()
            self._paginator.page_size = 20
        return self._paginator

    def paginate_queryset(self, queryset):
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        return self.paginator.get_paginated_response(data)