from rest_framework import serializers
from main.models import *
from users.models import *


# User management models
class UserSerializer(serializers.HyperlinkedModelSerializer):
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
    


class FriendshipSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Friendship
        fields = ["user1", "user2", "status"]
    
    def create(self, validated_data):
      user = self.context['request'].user
      return Friendship.objects.create(user1=user, **validated_data)

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
