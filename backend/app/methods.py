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
    TodoStatusEnum,
    TodoLists,
    TodoCountsDTO,
)
from sqlalchemy import select, func
from advanced_alchemy.filters import OrderBy
from sqlalchemy.ext.asyncio import AsyncSession
from collections.abc import AsyncGenerator
from .database import Base, SessionLocal, engine


async def provide_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session


async def provide_user_repo(db_session: AsyncSession) -> UserRepository:
    return UserRepository(session=db_session)


async def provide_todo_repo(
    db_session: AsyncSession,
) -> TodoRepository:
    return TodoRepository(session=db_session)


@asynccontextmanager
async def lifespan(app: Litestar):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


# register
@post("/register")
async def register(data: RegisterDTO, user_repo: UserRepository) -> UserResponseDTO:

    if await user_repo.get_by_username(data.username):
        raise ClientException("Username already exists.", status_code=409)
    if await user_repo.get_by_email(data.email):
        raise ClientException("Email already exists.", status_code=409)

    user = User(
        username=data.username,
        email=data.email,
        password=bcrypt.hash(data.password),
    )
    await user_repo.create(user)
    return UserResponseDTO.model_validate(user)


# login
@post("/login", status_code=200)
async def login(data: LoginDTO, user_repo: UserRepository) -> Response:

    user = await user_repo.get_by_username(data.username)

    if not user or not bcrypt.verify(data.password, user.password):
        raise NotAuthorizedException("Username or password is wrong.")

    return jwt_auth.login(
        identifier=str(user.id),
        send_token_as_response_body=True,
    )


# create todo list
@post("/todo")
async def create_todo_list(
    data: TodoListDTO, todo_repo: TodoRepository
) -> TodoListResponseDTO:

    todo = Todos(title=data.title, description=data.description, status=data.status)
    await todo_repo.add(todo, auto_commit=True)
    return TodoListResponseDTO.model_validate(todo)


# get lists
@get("/todos")
async def get_todos(
    db_session: AsyncSession,
    todo_repo: TodoRepository,
    status: TodoStatusEnum | None = None,
) -> TodoLists:
    statement = select(Todos).order_by(Todos.id.desc())

    # lists
    if status is not None:
        statement = statement.where(Todos.status == status)
    todos = await todo_repo.list(statement=statement)

    # count
    rows = await db_session.execute(
        select(Todos.status, func.count()).group_by(Todos.status)
    )
    by_status = {s: n for s, n in rows.all()}

    return TodoLists(
        items=[TodoListResponseDTO.model_validate(t) for t in todos],
        count=TodoCountsDTO(
            all=sum(by_status.values()),
            todo=by_status.get(TodoStatusEnum.TODO, 0),
            in_progress=by_status.get(TodoStatusEnum.IN_PROGRESS, 0),
            done=by_status.get(TodoStatusEnum.DONE, 0),
        ),
    )


# update status
@patch("/update_status/{todo_id:int}")
async def update_status(
    todo_repo: TodoRepository, todo_id: int, data: TodoStatusUpdateDTO
) -> TodoListResponseDTO:

    todo = await todo_repo.get_one_or_none(id=todo_id)
    if not todo:
        raise NotFoundException("Todo not found.")

    todo.status = data.status

    await todo_repo.update(todo, auto_commit=True)
    return TodoListResponseDTO.model_validate(todo)


# update all data in a list
@put("/todos/{todo_id:int}")
async def update_todo(
    todo_id: int, data: TodoData, todo_repo: TodoRepository
) -> TodoListResponseDTO:

    todo = await todo_repo.get_one_or_none(id=todo_id)
    if not todo:
        raise NotFoundException("Todo not found.")

    other = await todo_repo.get_one_or_none(title=data.title)
    if other and other.id != todo_id:
        raise ClientException("Todo title already exists.", status_code=409)

    todo.title = data.title
    todo.description = data.description
    todo.status = data.status
    await todo_repo.update(todo, auto_commit=True)
    return TodoListResponseDTO.model_validate(todo)


# delete by id
@delete("/delete_todo/{todo_id:int}")
async def delete_todo(todo_id: int, todo_repo: TodoRepository) -> None:

    if not await todo_repo.get_one_or_none(id=todo_id):
        raise NotFoundException("Todo not found.")

    await todo_repo.delete(todo_id, auto_commit=True)


# delete all lists
@delete("/delete_todos")
async def delete_todos(todo_repo: TodoRepository) -> None:
    await todo_repo.delete_where(auto_commit=True)
