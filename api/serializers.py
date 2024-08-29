from django.shortcuts import get_object_or_404
import requests
from io import BytesIO
from django.core.files import File
from rest_framework import serializers
from main.models import *
from users.models import *


# User management models
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    username = serializers.CharField(required=False, allow_blank = False)

    class Meta:
        model = User
        fields = ["id", "username", "email", "profile_picture", "password"]

    def create(self, validated_data):
        avatar_url = f"https://ui-avatars.com/api/?background=random&color=fff&name={validated_data["username"]}"
        response = requests.get(avatar_url)
        
        if response.status_code == 200:
          image_file = BytesIO(response.content)
          django_file = File(image_file, name=f"{validated_data['username']}.png")
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            profile_picture = django_file
        )
        return user


class FriendshipSerializer(serializers.ModelSerializer):

    class Meta:
        model = Friendship
        fields = ["user1", "user2", "status"]
        read_only_fields = ["user1"]

    def create(self, validated_data):
        requester = self.context["request"].user
        receiver_id = validated_data.get("user2")

        if requester == receiver_id:
            raise serializers.ValidationError(
                "You cannot send friendship request to yourself"
            )
        return Friendship.objects.create(user1=requester, user2=receiver_id)




class MessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Message
        fields = ["id", "content", "send_time", "sender"]

    def create(self, validated_data):
        sender = self.context["request"].user
        return Friendship.objects.create(sender=sender, **validated_data)


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ["id", "name", "participants"]
    
    


class ChannelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Channel
        fields = ["id", "name", "members", "chat_groups", "creation_date", "icon"]
        
    def create(self, validated_data):
        channel = Channel.objects.create(**validated_data)

        icon_url = f"https://ui-avatars.com/api/?background=random&color=fff&name={validated_data["name"]}"
        response = requests.get(icon_url)
      
        if response.status_code == 200:
          image_file = BytesIO(response.content)
          filename = f"{channel.id}.png"
          django_file = File(image_file, name=filename)
          channel.icon.save(filename, django_file)
          


class ChatGroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ChatGroup
        fields = ["id", "name", "chats"]

