from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import Http404
from django.views.decorators import authentication_classes
from django.db.models import Q
from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from users.models import *
from .serializers import *


# Create your views here.
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDestroy(generics.RetrieveDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@authentication_classes([])
@api_view(["POST"])
def login_view(request):
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(request, username=username, password=password)
    print(user)
    print(f"Username: {username}")
    print(f"Password: {password}")
    if user is not None:
        login(request, user)
        return Response(
            {"message": "Logged in successfully."}, status=status.HTTP_200_OK
        )
    else:
        return Response(
            {"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["POST"])
def logout_view(request):
    logout(request)
    return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)


class FriendshipList(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]

    def get(self, request, format=None):
        user = request.user
        friendships = Friendship.objects.filter(Q(user1=user) | Q(user2=user))
        serializer = FriendshipSerializer(
            friendships, many=True, context={"request": request}
        )
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = FriendshipSerializer(
            data=request.data,
            context={"request": request},
        )
        print(request.data['user2'])
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Friendship request sent."}, status=status.HTTP_201_CREATED
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FriendshipDetail(APIView):
    def get_object(self, request, pk, format=None):
        try:
            return Friendship.objects.get(pk=pk)
        except Friendship.DoesNotExist:
            return Http404

    def get(self, request, pk, format=None):
        pass

    def put(self, request, pk, format=None):
        pass

    def delete(self, request, *args, **kwargs):
        pass
