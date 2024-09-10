from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer,UpdateUserSerializer,UpdateUserProfileSerializer
# Create your views here.


@api_view(['POST'])
def register_user(request):
    data = request.data
    serializer = UserSerializer(data = data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_user(request,id):
    try:
        user = User.objects.get(id = id)
        user.delete()
        return Response({'message':'deleted successfully'},status=status.HTTP_200_OK)
    except Exception as ex:
        return Response({'error':f'{str(ex)}'},status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_user_by_id(request,id):
    try:
        user = User.objects.get(id = id)
        serializer = UserSerializer(user)
        return Response(serializer.data,status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'message':'no such user'},status=status.HTTP_404_NOT_FOUND)
    except Exception as ex:
        return Response({'error':f'{str(ex)}'},status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    try:
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data ,status=status.HTTP_200_OK)
    except Exception as ex:
        return Response({'error':f'{str(ex)}'},status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_all_users(request):
    try:
        users = User.objects.all()
        serializer = UserSerializer(users,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    except Exception as ex:
        return Response({'error':f'{str(ex)}'},status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['PUT'])
@permission_classes([IsAdminUser])
def update_user(request,id):
    try:
        user = User.objects.get(id = id)
        serializer = UpdateUserSerializer(data=request.data,instance=user,partial=True)
        if serializer.is_valid():
            updated_data = serializer.save()
            refresh = RefreshToken.for_user(updated_data)
            return Response({'user': serializer.data,'refresh': str(refresh),'access': str(refresh.access_token)}, status=status.HTTP_200_OK)
        else :
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    except Exception as ex:
        return Response({'error':f'{str(ex)}'})
    except User.DoesNotExist:
        return Response({'message':'no such user'},status=status.HTTP_404_NOT_FOUND)
    

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUserProfile(request):
    try:
        user = request.user
        serializer = UpdateUserProfileSerializer(data = request.data,instance=user,partial=True)
        if serializer.is_valid():
            updated_data = serializer.save()
            refresh = RefreshToken.for_user(updated_data)
            return Response({'user': serializer.data,'refresh': str(refresh),'access': str(refresh.access_token)}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    except Exception as ex:
        return Response({'error':f'{str(ex)}'})