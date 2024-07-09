from django.shortcuts import render

# Create your views here.
from .models import Post, Comment, CustomUser
from .serializers import *
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import *
from .permissions import IsOwnerOrReadOnly


# 전체 게시글 목록 조회, 게시글 작성
@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
def post_list(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostResponseSerializer(posts, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = PostDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

# 특정 게시물 조회, 수정, 삭제
@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsOwnerOrReadOnly])
def post_detail(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
        if request.method == 'GET':
            serializer = PostDetailSerializer(post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'PUT':
            serializer = PostDetailSerializer(post, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

# # 특정 게시글의 전체 댓글 목록 조회
# @api_view(['GET'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([AllowAny])
# def comment_list(request, post_id):
#     post = Post.objects.get(pk=post_id)
#     comments = Comment.objects.filter(post=post)
#     serializer = CommentWithoutSerializer(comments, many=True)
#     return Response(serializer.data, status=status.HTTP_200_OK)

# # 특정 게시글에 댓글 작성
# @api_view(['POST'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticatedOrReadOnly])
# def create_comment(request, post_id):
#     post = Post.objects.get(pk=post_id)
#     serializer = CommentRequestSerializer(data=request.data)
#     if serializer.is_valid():
#         new_comment = serializer.save(post=post)
#         response = CommentResponseSerializer(new_comment)
#         return Response(response.data, status=status.HTTP_201_CREATED)
    
# 특정 게시글의 전체 댓글 목록 조회, 특정 게시글에 댓글 작성
@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
def about_comment(request, post_id):
    if request.method == 'GET':
        post = Post.objects.get(pk=post_id)
        comments = Comment.objects.filter(post=post)
        serializer = CommentWithoutSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        post = Post.objects.get(pk=post_id)
        serializer = CommentRequestSerializer(data=request.data)
        if serializer.is_valid():
            new_comment = serializer.save(post=post)
            response = CommentResponseSerializer(new_comment)
            return Response(response.data, status=status.HTTP_201_CREATED)


# 특정 게시글의 특정 댓글 삭제
@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsOwnerOrReadOnly])
def delete_comment(request, post_id, comment_id):
    try:
        post = Post.objects.get(pk=post_id)
        comment = Comment.objects.get(pk=comment_id)
        comment.delete()
        serializer = PostDetailSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Comment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

# # 특정 대학교 학생이 작성한 전체 게시물 목록 조회
# @api_view(['GET'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsOwnerOrReadOnly])
# def univ_post(request, )