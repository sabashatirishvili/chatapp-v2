from django.urls import path
from .views import *


app_name = "api"

urlpatterns = [
    path("users/", UserViewSet.as_view({"post": "create"})),
    path("users/login/", login_view),
    path("users/logout/", logout_view),
    path("users/check-auth/", check_auth),
    path("users/auth-user/", get_authenticated_user),
    path("friendships/", FriendshipList.as_view(), name="friendship-list"),
    path(
        "friendships/<uuid:pk>/", FriendshipDetail.as_view(), name="friendship-detail"
    ),
    path(
        "messages/",
        MessageViewSet.as_view(
            {
                "get": "list",
                "post": "create",
            }
        ),
    ),
    path(
        "chats/",
        ChatViewSet.as_view(
            {
                "get": "list",
                "post": "create",
            }
        ),
    ),
    # path("chatgroups/", ChatGroupViewSet.as_view()),
    # path("channels/", ChatGroupViewSet.as_view())
]
