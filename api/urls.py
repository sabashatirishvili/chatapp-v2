from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *


app_name = "api"

urlpatterns = [
    path("users/", UserList.as_view()),
    path("users/<uuid:pk>/", UserDetail.as_view()),
    path("users/create/", UserCreate.as_view()),
    path("users/login/", login_view),
    path("users/logout/", logout_view),
    path("friendships/", FriendshipList.as_view(), name="friendship-detail"),
    path("friendships/<uuid:pk>/", FriendshipDetail.as_view(), name="friendship-detail"),
]
