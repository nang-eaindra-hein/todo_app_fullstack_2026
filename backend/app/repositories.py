from advanced_alchemy.repository import SQLAlchemyAsyncRepository

from .models import Todos, User


class TodoRepository(SQLAlchemyAsyncRepository[Todos]):
    model_type = Todos


class UserRepository(SQLAlchemyAsyncRepository[User]):
    model_type = User

    async def get_by_username(self, username: str) -> User | None:
        return await self.get_one_or_none(username=username)

    async def get_by_email(self, email: str) -> User | None:
        return await self.get_one_or_none(email=email)

    async def create(self, user: User) -> User:
        return await self.add(user, auto_commit=True)  # auto_commit = save for real
