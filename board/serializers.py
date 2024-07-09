from rest_framework import serializers
from .models import *
from django.utils import timezone

#전체 게시글 목록 조회
class PostResponseSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    nickname = serializers.ReadOnlyField(source='user.nickname')

    class Meta:
        model = Post
        fields = ['id', 'user', 'nickname', 'title', 'created_at']

    def get_created_at(self, obj):
        time = timezone.localtime(obj.created_at)
        return time.strftime('%Y-%m-%d')
        
        
class CommentRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['comment']

# 게시글 작성, 특정 게시글 조회, 특정 게시글 수정
class PostDetailSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    comments = CommentRequestSerializer(many=True, read_only=True)
    nickname = serializers.ReadOnlyField(source='user.nickname')
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'user', 'nickname', 'title', 'body', 'created_at', 'comments']

    def get_created_at(self, obj):
        time = timezone.localtime(obj.created_at)
        return time.strftime('%Y-%m-%d')
        
#  특정 게시글의 전체 댓글 목록 조회 (title, body 없음)
class CommentWithoutSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    user = serializers.ReadOnlyField()
    nickname = serializers.ReadOnlyField(source='user.nickname')

    class Meta:
        model = Comment
        fields = ['id', 'user', 'nickname', 'comment', 'created_at']

    def get_created_at(self, obj):
        time = timezone.localtime(obj.created_at)
        return time.strftime('%Y-%m-%d')
        
# 특정 게시글에 댓글 작성  # 특정 게시글의 특정 댓글 삭제   #맞는지 모르겠다....ㅜ
class CommentResponseSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    user = serializers.ReadOnlyField()
    nickname = serializers.ReadOnlyField(source='user.nickname')
    comments = CommentRequestSerializer(many=True)

    class Meta:
        model = Post
        fields = ['id', 'user', 'nickname', 'title', 'body', 'created_at', 'comments']

    def get_created_at(self, obj):
        time = timezone.localtime(obj.created_at)
        return time.strftime('%Y-%m-%d')

class UserPostSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    user = serializers.ReadOnlyField()

    class Meta:
        model = Post
        fields = ['id', 'user', 'title', 'created_at']

    def get_created_at(self, obj):
        time = timezone.localtime(obj.created_at)
        return time.strftime('%Y-%m-%d')

# class UnivPostSerializer(serializers.ModelSerializer):
#     nickname = serializers.ReadOnlyField(source='user.nickname')
#     created_at = serializers.SerializerMethodField()

#     class Meta:
#         model = UnivPost
#         fields = ['id', 'user', 'nickname', 'title', 'created_at']

#         def get_created_at(self, obj):
#             time = timezone.localtime(obj.created_at)
#             return time.strftime('%Y-%m-%d')