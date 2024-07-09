from django.shortcuts import render
from .serializers import *
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import *
from board.permissions import IsOwnerOrReadOnly
from board.models import Post
from board.serializers import UserPostSerializer

# 회원가입
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([AllowAny])
def sign_up(request):
    serializer = CustomRegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        response = {
            'access': '엑세스 토큰',
            'refresh': '리프레시 토큰',
            'user': {
                serializer.data
            }
        }
        return Response(response, status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)

# 로그인

# POST로 전달된 데이터를 AccessUserSerializer에 넣고
# username_변수에 AccessUser의 username 객체를 불러오고 password_변수에는 AccessUser의 password 객체를 불러오고
# un_serializer 변수를 만들어서 CustomRegisterSerializer(회원가입 때 사용)에 username 객체를 넣어주고 ps_serializer 변수에는 password 객체를 넣어주고
# username_(로그인한 사용자의 username)과 CustomRegisterSeriliazer의 username 데이터(회원가입한 사용자의 username)가 같으면 아래를 response
# response : response_serializer에 모든 CustomUser의 객체를 넣어줌

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([AllowAny])

def log_in(request, username, password):
    serializer = AccessUserSerializer(data=request.data)
    response_data = CustomUser.objects.all()
    username_ = AccessUser.objects.get(pk=username)
    password_ = AccessUser.objects.get(pk=password)
    un_serializer = CustomRegisterSerializer(username_)
    ps_serializer = CustomRegisterSerializer(password_)
    response_serializer = CustomUserDetailSerializer(response_data, many=True)
    if username_ == un_serializer.data['username'] and password_ == ps_serializer.data['password']: # if 회원가입 시 username, password == 로그인 시 username, password
        response = {
            'access': '엑세스 토큰',
            'refresh': '리프레시 토큰',
            'user': {
                response_serializer.data
            }
        }
        return Response(response, status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)

# 유저 정보 조회
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])

def user_info(request, user_id):
    try:
        user = CustomUser.objects.get(pk=user_id)
        serializer = UserInfoSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except CustomUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

# 유저가 작성한 게시글 목록 조회
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])

def user_post(request, user_id):
    user = CustomUser.objects.get(pk=user_id)
    posts = Post.objects.filter(user=user)
    serializer = UserPostSerializer(posts, many=True)
    return Response(serializer.data, status=status.HTTP_201_CREATED)