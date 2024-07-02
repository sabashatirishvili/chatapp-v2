from rest_framework import serializers
from main.models import *
from users.models import *

# User management models
class UserSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'username', 'email']

class FriendshipSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Friendship
    fields = ['user1','user2','status']


###

class MessageSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Message
    fields = ['id', 'content', 'send_time', 'sender']


class ChatSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Chat
    fields = ['id', 'name', 'participants', 'messages']

class ChannelSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Channel
    fields = ['id', 'name', 'members', 'chat_groups', 'creation_date']

class ChatGroupSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = ChatGroup
    fields = ['id', 'name', 'chats']