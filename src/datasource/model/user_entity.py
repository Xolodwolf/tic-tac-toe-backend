from sqlalchemy import Column, String
from datasource.database import Base
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4


class UserEntity(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    login = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)
