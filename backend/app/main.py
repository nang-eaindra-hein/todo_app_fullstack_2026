from litestar import Litestar
from litestar.config.cors import CORSConfig
from litestar.di import Provide

from .auth import jwt_auth
from .methods import (
    login,
    register,
    lifespan,
    provide_db_session,
    provide_todo_repo,
)

app = Litestar(
    route_handlers=[register, login],
    dependencies={
        "db_session": Provide(provide_db_session),
        "todo_repo": Provide(provide_todo_repo),
    },
    on_app_init=[jwt_auth.on_app_init],
    cors_config=CORSConfig(allow_origins=["http://localhost:5173"]),
    lifespan=[lifespan],
    debug=True,
)
