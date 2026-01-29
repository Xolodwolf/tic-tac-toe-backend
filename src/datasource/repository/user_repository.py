from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Session
from datasource.model.user_entity import UserEntity


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def save(self, user: UserEntity) -> UserEntity:
        self.session.add(user)
        self.session.commit()
        return user

    def find_by_login(self, login: str) -> Optional[UserEntity]:
        return self.session.query(UserEntity).filter(UserEntity.login == login).first()

    def find_by_id(self, user_id: UUID) -> Optional[UserEntity]:
        return (
            self.session.query(UserEntity).filter(UserEntity.user_id == user_id).first()
        )
