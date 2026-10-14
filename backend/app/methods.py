from contextlib import asynccontextmanager
from litestar import Litestar, post, get, patch, delete
from litestar.exceptions import ClientException, NotAuthorizedException
from passlib.hash import bcrypt
from .auth import jwt_auth
from .models import User
from .repositories import UserRepository
from .schemas import RegisterDTO, UserResponseDTO, LoginDTO
from sqlalchemy.ext.asyncio import AsyncSession


@post("/register")
async def register(data: RegisterDTO, db_session: AsyncSession) -> UserResponseDTO:
    repo = UserRepository(session=db_session)

    if await repo.get_by_username(data.username):
        raise ClientException("Username already exists.", status_code=409)
    if await repo.get_by_email(data.email):
        raise ClientException("Email already exists.", status_code=409)

    user = User(
        username=data.username,
        email=data.email,
        password=bcrypt.hash(data.password),
    )
    await repo.create(user)
    return UserResponseDTO.model_validate(user)


@post("/login", status_code=200)
async def login(data: LoginDTO, db_session: AsyncSession) -> dict:
    repo = UserRepository(session=db_session)
    user = await repo.get_by_username(data.username)

    if not user or not bcrypt.verify(data.password, user.password):
        raise NotAuthorizedException("Username or password is wrong.")

    return jwt_auth.login(identifier=str(user.id))
