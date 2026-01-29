from flask import Flask
from flask_jwt_extended import JWTManager
from datetime import timedelta
from web.route.auth_controller import AuthController
from web.route.user_controller import UserController
from web.route.game_controller import GameController
import os


def create_app(container) -> Flask:
    app = Flask(__name__)

    app.config["CONTAINER"] = container

    # JWT конфигурация
    # Используем переменную окружения или дефолтное значение для SECRET_KEY
    app.config["JWT_SECRET_KEY"] = os.getenv(
        "JWT_SECRET_KEY", "your-secret-key-change-in-production"
    )
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)

    jwt = JWTManager(app)

    auth_controller = AuthController(
        container.auth_service, container.user_service, container.authenticator
    )
    app.register_blueprint(auth_controller.bp)

    user_controller = UserController(container.user_service, container.authenticator)
    app.register_blueprint(user_controller.blueprint)

    game_controller = GameController(container.game_service, container.authenticator)
    app.register_blueprint(game_controller.blueprint)

    return app
