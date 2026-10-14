from litestar import Litestar
from litestar.config.cors import CORSConfig
from litestar.di import Provide

from .auth import jwt_auth
from .methods import (
    get_user,
    get_users,
    lifespan,
    login,
    profile,
    provide_db_session,
    provide_todo_repo,
    register,
)

app = Litestar(
    route_handlers=[register, login, profile, get_users, get_user],
    dependencies={
        "db_session": Provide(provide_db_session),
        "todo_repo": Provide(provide_todo_repo),
    },
    on_app_init=[jwt_auth.on_app_init],
    cors_config=CORSConfig(allow_origins=["http://localhost:5173"]),
    lifespan=[lifespan],
    debug=True,
)
