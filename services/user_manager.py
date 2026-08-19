from models import User
from typing import Annotated

from fastapi import Depends, Request

from repositories.user import UserRepository, get_user_repository
from fastapi_users import BaseUserManager, IntegerIDMixin
from core.config import settings


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = settings.access_token.RESET_PASSWORD_TOKEN_SECRET
    verification_token_secret = settings.access_token.VERIFICATION_TOKEN_SECRET

    async def on_after_register(self, user: User, request: Request | None = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(self, user: User, token: str, request: Request | None = None):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(self, user: User, token: str, request: Request | None = None):
        print(f"Verification requested for user {user.id}. Verification token: {token}")


async def get_user_manager(repo: Annotated[UserRepository, Depends(get_user_repository)]):
    return UserManager(repo)
