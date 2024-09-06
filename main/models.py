from django.db import models
from django.utils import timezone
from users.models import User
import uuid

# Create your models here.


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField(max_length=750)
    send_time = models.DateTimeField(default=timezone.now)
    # chat = models.ForeignKey("Chat", on_delete=models.CASCADE)
    # channel = models.ForeignKey(
    #     "Channel", on_delete=models.CASCADE, blank=True, null=True
    # )
    sender = models.ForeignKey(User, on_delete=models.CASCADE)


class Chat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=30, blank=True, null=True)
    participants = models.ManyToManyField(User, related_name="members")
    messages = models.ManyToManyField("Message", blank=True, verbose_name=("messages"))

    def __str__(self):
        return str(self.id)


class Channel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="owned_channels",
        blank=True,
        null=True,
    )
    icon = models.ImageField(upload_to="images/", null=True, blank=True)
    members = models.ManyToManyField(User, blank=False, related_name="channels")
    chat_groups = models.ManyToManyField("ChatGroup")
    creation_date = models.DateTimeField(default=timezone.now)


class ChatGroup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=20)
    chats = models.ManyToManyField(Chat)
