from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import Http404
from django.db.models import Q, Count
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework import viewsets
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
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
    permission_classes = [AllowAny]


class UserDestroy(generics.RetrieveDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(["POST"])
@permission_classes([AllowAny])
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
        print(request.data["user2"])
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Friendship request sent."}, status=status.HTTP_201_CREATED
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FriendshipDetail(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]

    def get_object(self, request, pk, format=None):
        try:
            return Friendship.objects.get(pk=pk)
        except Friendship.DoesNotExist:
            return Http404

    def get(self, request, pk, format=None):
        friendship = self.get_object(pk=pk)
        if friendship:
            return Response(friendship, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Friendship not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, pk, format=None):
        friendship = self.get_object(pk=pk)
        serializer = FriendshipSerializer(friendship, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        friendship = self.get_object(pk=pk)

        if friendship:
            friendship.delete()
            return Response(
                {"message": "Successfully deleted."}, status=status.HTTP_204_NO_CONTENT
            )
        return Response(
            {"error": "Friendship not found"}, status=status.HTTP_404_NOT_FOUND
        )


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False)
    def list(self, serializer):
        pass


class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

    @action(detail=False)
    def list(self, request):
        user = request.user
        chats = Chat.objects.annotate(participants_count=Count("participants")).filter(
            Q(participants=user) & Q(participants_count=2)
        )
        serializer = self.get_serializer(chats, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
          serializer.save()
          return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_)


class ChannelViewSet(viewsets.ModelViewSet):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer


class ChatGroupViewSet(viewsets.ModelViewSet):
    queryset = ChatGroup.objects.all()
    serializer_class = ChatGroupSerializer
