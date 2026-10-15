from contextlib import asynccontextmanager
from litestar import Litestar, post, get, patch, delete, Response, put
from litestar.exceptions import (
    ClientException,
    NotAuthorizedException,
    NotFoundException,
)
from passlib.hash import bcrypt
from .auth import jwt_auth
from .models import User, Todos
from .repositories import UserRepository, TodoRepository
from .schemas import (
    RegisterDTO,
    UserResponseDTO,
    LoginDTO,
    TodoListResponseDTO,
    TodoListDTO,
    TodoStatusUpdateDTO,
    TodoData,
)
from advanced_alchemy.filters import OrderBy
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


# register
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


# login
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


# create todo list
@post("/todo")
async def create_todo_list(
    data: TodoListDTO, db_session: AsyncSession
) -> TodoListResponseDTO:
    repo = TodoRepository(session=db_session)

    todo = Todos(title=data.title, description=data.description, status=data.status)
    await repo.add(todo, auto_commit=True)
    return TodoListResponseDTO.model_validate(todo)


# get lists
@get("/todos")
async def get_todos(db_session: AsyncSession) -> list[TodoListResponseDTO]:
    repo = TodoRepository(session=db_session)
    todos = await repo.list(OrderBy(field_name="id", sort_order="desc"))
    return [TodoListResponseDTO.model_validate(t) for t in todos]


# update status
@patch("/update_status/{todo_id:int}")
async def update_status(
    db_session: AsyncSession, todo_id: int, data: TodoStatusUpdateDTO
) -> TodoListResponseDTO:
    repo = TodoRepository(session=db_session)

    todo = await repo.get_one_or_none(id=todo_id)
    if not todo:
        raise NotFoundException("Todo not found.")

    todo.status = data.status

    await repo.update(todo, auto_commit=True)
    return TodoListResponseDTO.model_validate(todo)


# update all data in a list
@put("/todos/{todo_id:int}")
async def update_todo(
    todo_id: int, data: TodoData, db_session: AsyncSession
) -> TodoListResponseDTO:
    repo = TodoRepository(session=db_session)

    todo = await repo.get_one_or_none(id=todo_id)
    if not todo:
        raise NotFoundException("Todo not found.")

    other = await repo.get_one_or_none(title=data.title)
    if other and other.id != todo_id:
        raise ClientException("Todo title already exists.", status_code=409)

    todo.title = data.title
    todo.description = data.description
    todo.status = data.status
    await repo.update(todo, auto_commit=True)
    return TodoListResponseDTO.model_validate(todo)


# delete by id
@delete("/delete_todo/{todo_id:int}")
async def delete_todo(todo_id: int, db_session: AsyncSession) -> None:
    repo = TodoRepository(session=db_session)

    if not await repo.get_one_or_none(id=todo_id):
        raise NotFoundException("Todo not found.")

    await repo.delete(todo_id, auto_commit=True)


# delete all lists
@delete("/delete_todos")
async def delete_todos(db_session: AsyncSession) -> None:
    repo = TodoRepository(session=db_session)
    await repo.delete_where(auto_commit=True)
