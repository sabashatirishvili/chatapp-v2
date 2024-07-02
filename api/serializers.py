from rest_framework import serializers
from main.models import *
from users.models import *

class UserSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'username', 'email']