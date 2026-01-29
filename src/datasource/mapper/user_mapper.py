from uuid import UUID
from datasource.model.user_entity import UserEntity
from domain.model.users import User


class UserMapper:
    @staticmethod
    def to_domain(entity: UserEntity) -> User:
        return User(
            user_id=(
                entity.user_id
                if isinstance(entity.user_id, UUID)
                else UUID(entity.user_id)
            ),
            login=entity.login,
            password=entity.password,
        )

    @staticmethod
    def to_entity(user: User) -> UserEntity:
        entity = UserEntity()
        entity.user_id = user.user_id
        entity.login = user.login
        entity.password = user.password
        return entity
