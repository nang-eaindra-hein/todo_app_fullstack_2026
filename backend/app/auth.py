import os
from uuid import UUID

from litestar.connection import ASGIConnection
from litestar.security.jwt import JWTAuth, Token

from .database import SessionLocal
from .models import User


async def retrieve_user_handler(
    token: Token, connection: ASGIConnection
) -> User | None:

    async with SessionLocal() as session:
        return await session.get(User, UUID(token.sub))  # UUID, not int


jwt_auth = JWTAuth[User](
    retrieve_user_handler=retrieve_user_handler,
    token_secret=os.environ.get("JWT_SECRET", "dev-secret-change-me"),
    exclude=["/login", "/register", "/schema"],  # public routes
)
