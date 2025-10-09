from rest_framework import serializers
from .models import Post, Comment, Like
from accounts.serializers import UserProfileSerializer

class LikeSerializer(serializers.ModelSerializer):
    user_details = UserProfileSerializer(source='user', read_only=True)
    
    class Meta:
        model = Like
        fields = ['id', 'user', 'user_details', 'post', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']

class CommentSerializer(serializers.ModelSerializer):
    author_details = UserProfileSerializer(source='author', read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'author_details', 'content', 
                 'created_at', 'updated_at']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)

class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content']
    
    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        validated_data['post'] = self.context['post']
        return super().create(validated_data)

class PostSerializer(serializers.ModelSerializer):
    author_details = UserProfileSerializer(source='author', read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    likes = LikeSerializer(many=True, read_only=True)
    
    class Meta:
        model = Post
        fields = ['id', 'author', 'author_details', 'title', 'content',
                 'created_at', 'updated_at', 'comments', 'comments_count',
                 'likes_count', 'is_liked', 'likes']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']
    
    def get_comments_count(self, obj):
        return obj.comments.count()
    
    def get_likes_count(self, obj):
        return obj.likes.count()
    
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False

class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'content']
    
    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)