from contextlib import asynccontextmanager
from litestar import Litestar, post, get, patch, delete, Response
from litestar.exceptions import ClientException, NotAuthorizedException
from passlib.hash import bcrypt
from .auth import jwt_auth
from .models import User
from .repositories import UserRepository, TodoRepository
from .schemas import RegisterDTO, UserResponseDTO, LoginDTO
from sqlalchemy.ext.asyncio import AsyncSession
from collections.abc import AsyncGenerator
from .database import Base, SessionLocal, engine


async def provide_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session


async def provide_todo_repo(db_session: AsyncSession) -> TodoRepository:
    return TodoRepository(session=db_session)


@asynccontextmanager
async def lifespan(app: Litestar):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


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
async def login(data: LoginDTO, db_session: AsyncSession) -> Response:
    repo = UserRepository(session=db_session)
    user = await repo.get_by_username(data.username)

    if not user or not bcrypt.verify(data.password, user.password):
        raise NotAuthorizedException("Username or password is wrong.")

    return jwt_auth.login(
        identifier=str(user.id),
        send_token_as_response_body=True,
    )
