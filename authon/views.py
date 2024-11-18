from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer,UpdateUserSerializer,UpdateUserProfileSerializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
# Create your views here.




@swagger_auto_schema(
    method='post',
    operation_summary="Register a new user",
    operation_description=(
        "This endpoint allows users to register by providing their account details. "
        "The registration requires necessary fields such as username, password, and email. "
        "Upon successful registration, the new user's data is returned as a response."
    ),
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, description="Username of the user"),
            'email': openapi.Schema(type=openapi.TYPE_STRING, description="Email address of the user"),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description="Password for the user"),
            'first_name': openapi.Schema(type=openapi.TYPE_STRING, description="First name of the user"),
            'last_name': openapi.Schema(type=openapi.TYPE_STRING, description="Last name of the user"),
        },
        required=['username', 'email', 'password'],
    ),
    responses={
        201: openapi.Response(
            description="User successfully registered",
            examples={
                "application/json": {
                    "id": 1,
                    "username": "new_user",
                    "email": "user@example.com",
                    "first_name": "John",
                    "last_name": "Doe"
                }
            }
        ),
        400: openapi.Response(
            description="Bad request, validation errors",
            examples={
                "application/json": {
                    "username": ["This field is required."],
                    "password": ["This field is required."]
                }
            }
        ),
    }
)

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



@swagger_auto_schema(
    method='get',
    operation_summary="Delete a user",
    operation_description=(
        "This endpoint allows administrators to delete a user by their ID. "
        "Only users with admin permissions are authorized to perform this action."
    ),
    responses={
        200: openapi.Response(
            description="User successfully deleted",
            examples={
                "application/json": {
                    "message": "deleted successfully"
                }
            }
        ),
        400: openapi.Response(
            description="Bad Request",
            examples={
                "application/json": {
                    "error": "User matching query does not exist."
                }
            }
        ),
    },
    manual_parameters=[
        openapi.Parameter(
            name="id",
            in_=openapi.IN_PATH,
            type=openapi.TYPE_INTEGER,
            description="ID of the user to delete",
            required=True,
        ),
    ],
)
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



@swagger_auto_schema(
    method='get',
    operation_summary="Retrieve user profile",
    operation_description=(
        "This endpoint allows authenticated users to retrieve their own profile information. "
        "The profile includes details such as username, email, first name, and last name."
    ),
    responses={
        200: openapi.Response(
            description="User profile retrieved successfully",
            examples={
                "application/json": {
                    "id": 1,
                    "username": "john_doe",
                    "email": "john@example.com",
                    "first_name": "John",
                    "last_name": "Doe",
                }
            },
        ),
        400: openapi.Response(
            description="Bad request",
            examples={
                "application/json": {
                    "error": "An unexpected error occurred while retrieving the user profile."
                }
            },
        ),
    },
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    try:
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data ,status=status.HTTP_200_OK)
    except Exception as ex:
        return Response({'error':f'{str(ex)}'},status=status.HTTP_400_BAD_REQUEST)
    



@swagger_auto_schema(
    method='get',
    operation_summary="Retrieve all users",
    operation_description=(
        "This endpoint allows administrators to retrieve a list of all registered users in the system. "
        "The response contains detailed user information such as usernames, emails, and other fields."
    ),
    responses={
        200: openapi.Response(
            description="List of users retrieved successfully",
            examples={
                "application/json": [
                    {
                        "id": 1,
                        "username": "john_doe",
                        "email": "john@example.com",
                        "first_name": "John",
                        "last_name": "Doe",
                    },
                    {
                        "id": 2,
                        "username": "jane_doe",
                        "email": "jane@example.com",
                        "first_name": "Jane",
                        "last_name": "Doe",
                    }
                ]
            },
        ),
        400: openapi.Response(
            description="Bad request",
            examples={
                "application/json": {
                    "error": "An unexpected error occurred while retrieving the users."
                }
            },
        ),
    },
)
@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_all_users(request):
    try:
        users = User.objects.all()
        serializer = UserSerializer(users,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    except Exception as ex:
        return Response({'error':f'{str(ex)}'},status=status.HTTP_400_BAD_REQUEST)
    



@swagger_auto_schema(
    method='put',
    operation_summary="Update a user's information",
    operation_description=(
        "This endpoint allows an admin to update a user's details. "
        "The admin can modify fields like the username, email, and other profile information. "
        "Upon successful update, a new JWT token pair (refresh and access) is generated for the user."
    ),
    request_body=UpdateUserSerializer,
    responses={
        200: openapi.Response(
            description="User updated successfully",
            examples={
                "application/json": {
                    "user": {
                        "id": 1,
                        "username": "updated_user",
                        "email": "updated@example.com",
                        "first_name": "Updated",
                        "last_name": "User"
                    },
                    "refresh": "new_refresh_token",
                    "access": "new_access_token"
                }
            },
        ),
        400: openapi.Response(
            description="Validation error",
            examples={
                "application/json": {
                    "email": ["This field must be a valid email address."]
                }
            },
        ),
        404: openapi.Response(
            description="User not found",
            examples={
                "application/json": {
                    "message": "no such user"
                }
            },
        ),
    },
)
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
    




@swagger_auto_schema(
    method='put',
    operation_summary="Update authenticated user's profile",
    operation_description=(
        "This endpoint allows an authenticated user to update their own profile details, such as "
        "username, email, first name, or last name. Upon successful update, a new JWT token pair "
        "(refresh and access) is issued."
    ),
    request_body=UpdateUserProfileSerializer,
    responses={
        200: openapi.Response(
            description="User profile updated successfully",
            examples={
                "application/json": {
                    "user": {
                        "id": 1,
                        "username": "updated_user",
                        "email": "updated@example.com",
                        "first_name": "Updated",
                        "last_name": "User"
                    },
                    "refresh": "new_refresh_token",
                    "access": "new_access_token"
                }
            },
        ),
        400: openapi.Response(
            description="Validation error",
            examples={
                "application/json": {
                    "email": ["This field must be a valid email address."]
                }
            },
        ),
    },
)
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