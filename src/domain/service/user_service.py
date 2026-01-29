from typing import Optional
from uuid import UUID
import hashlib
from datasource.repository.user_repository import UserRepository
from datasource.mapper.user_mapper import UserMapper
from datasource.model.user_entity import UserEntity
from domain.model.users import User
from domain.model.sign_up_request import SignUpRequest


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        self.user_mapper = UserMapper()

    def create_user(self, sign_up_request: SignUpRequest) -> User:
        existing_user = self.user_repository.find_by_login(sign_up_request.login)
        if existing_user:
            raise ValueError(
                f"User with login '{sign_up_request.login}' already exists"
            )

        hashed_password = self._hash_password(sign_up_request.password)

        user_entity = UserEntity()
        user_entity.login = sign_up_request.login
        user_entity.password = hashed_password

        saved_entity = self.user_repository.save(user_entity)

        return self.user_mapper.to_domain(saved_entity)

    def find_by_login(self, login: str) -> Optional[User]:
        entity = self.user_repository.find_by_login(login)
        return self.user_mapper.to_domain(entity) if entity else None

    def find_by_id(self, user_id: UUID) -> Optional[User]:
        entity = self.user_repository.find_by_id(str(user_id))
        return self.user_mapper.to_domain(entity) if entity else None

    def verify_password(self, user: User, password: str) -> bool:
        hashed_password = self._hash_password(password)
        return user.password == hashed_password

    @staticmethod
    def _hash_password(password: str) -> str:
        return hashlib.sha256(password.encode("utf-8")).hexdigest()
