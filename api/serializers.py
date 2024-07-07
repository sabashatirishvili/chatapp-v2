from django.shortcuts import get_object_or_404
from rest_framework import serializers
from main.models import *
from users.models import *


# User management models
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user


class FriendshipSerializer(serializers.ModelSerializer):
    user2 = serializers.UUIDField()

    class Meta:
        model = Friendship
        fields = ["user1", "user2", "status"]
        read_only_fields = ["user1"]

    def create(self, validated_data):
        requester = self.context["request"].user
        receiver_id = validated_data.get("user2")
        receiver = get_object_or_404(User, pk=receiver_id)

        if requester == receiver:
            raise serializers.ValidationError(
                "You cannot send friendship request to yourself"
            )
        return Friendship.objects.create(user1=requester, user2=receiver.id)


###


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Message
        fields = ["id", "content", "send_time", "sender"]


class ChatSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Chat
        fields = ["id", "name", "participants", "messages"]


class ChannelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Channel
        fields = ["id", "name", "members", "chat_groups", "creation_date"]


class ChatGroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ChatGroup
        fields = ["id", "name", "chats"]
