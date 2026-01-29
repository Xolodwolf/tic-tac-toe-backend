from sqlalchemy.orm import Session
from datetime import timedelta
from datasource.database import get_db_session, init_db
from datasource.repository.game_repository import GameRepository
from datasource.repository.user_repository import UserRepository
from domain.service.game_service_impl import GameServiceImpl
from domain.service.game_service_interface import GameServiceInterface
from domain.service.user_service import UserService
from domain.service.auth_service import AuthService
from domain.service.jwt_provider import JwtProvider
from web.module.user_authenticator import UserAuthenticator


class Container:
    def __init__(self):
        init_db()

        self._session: Session = get_db_session()

        self._game_repository = GameRepository(self._session)
        self._user_repository = UserRepository(self._session)

        self._jwt_provider = JwtProvider(
            access_token_expires=timedelta(minutes=15),
            refresh_token_expires=timedelta(days=30),
        )

        self._user_service = UserService(self._user_repository)

        self._game_service: GameServiceInterface = GameServiceImpl(
            self._game_repository, self._user_service
        )

        self._auth_service = AuthService(self._user_service, self._jwt_provider)
        self._authenticator = UserAuthenticator(self._auth_service)

    @property
    def session(self) -> Session:
        return self._session

    @property
    def repository(self) -> GameRepository:
        return self._game_repository

    @property
    def game_repository(self) -> GameRepository:
        return self._game_repository

    @property
    def user_repository(self) -> UserRepository:
        return self._user_repository

    @property
    def service(self) -> GameServiceInterface:
        return self._game_service

    @property
    def game_service(self) -> GameServiceInterface:
        return self._game_service

    @property
    def user_service(self) -> UserService:
        return self._user_service

    @property
    def auth_service(self) -> AuthService:
        return self._auth_service

    @property
    def authenticator(self) -> UserAuthenticator:
        return self._authenticator

    @property
    def jwt_provider(self) -> JwtProvider:
        return self._jwt_provider

    def close(self):
        if self._session:
            self._session.close()
