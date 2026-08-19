from services.user_manager import get_user_manager
from core.constants import UserIdType
from models import User
from fastapi_users import FastAPIUsers
from services.access_token import get_access_token_service
from fastapi_users.authentication import BearerTransport, AuthenticationBackend

bearer_transport = BearerTransport(tokenUrl="api/auth/v1/login")

auth_backend = AuthenticationBackend(
    name="access_tokens",
    transport=bearer_transport,
    get_strategy=get_access_token_service,
)

fastapi_users = FastAPIUsers[User, UserIdType](
    get_user_manager=get_user_manager,
    auth_backends=[auth_backend],
)
