import re

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async



def get_user_id(path: str):
    pattern = r'/ws/connection-status/(\d+)/'
    user_id = user_id = re.search(pattern, path).group(1)

    return user_id


@database_sync_to_async
def get_user(user_id: int):
    User = get_user_model()
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return AnonymousUser()


class PathAuthMiddleware:
    """
    Custom middleware (insecure) that takes user IDs from the query string.
    """

    def __init__(self, app):
        # Store the ASGI application we were passed
        self.app = app

    async def __call__(self, scope, receive, send):
        # Look up user from query string (you should also do things like
        # checking if it is a valid user ID, or if scope["user"] is already
        # populated).
        user_id = get_user_id(scope['path'])
        scope['user'] = await get_user(int(user_id))

        return await self.app(scope, receive, send)
