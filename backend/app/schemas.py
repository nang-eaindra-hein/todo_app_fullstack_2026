from enum import Enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class TodoStatusEnum(str, Enum):
    TODO = "Todo"
    IN_PROGRESS = "In_Progress"
    DONE = "Done"


class TodoData(BaseModel):
    id: int
    title: str
    status: TodoStatusEnum
    model_config = ConfigDict(from_attributes=True)


class RegisterDTO(BaseModel):
    username: str
    email: str
    password: str


class LoginDTO(BaseModel):
    username: str
    password: str


class UserResponseDTO(BaseModel):
    id: UUID
    username: str
    email: str
    model_config = ConfigDict(from_attributes=True)
