from datetime import timedelta
from typing import Optional
from uuid import UUID
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    decode_token,
)
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError, DecodeError
from domain.model.users import User


class JwtProvider:
    def __init__(
        self,
        access_token_expires: timedelta = timedelta(minutes=15),
        refresh_token_expires: timedelta = timedelta(days=30),
    ):
        self.access_token_expires = access_token_expires
        self.refresh_token_expires = refresh_token_expires

    def generate_access_token(self, user: User) -> str:
        return create_access_token(
            identity=str(user.user_id), expires_delta=self.access_token_expires
        )

    def generate_refresh_token(self, user: User) -> str:
        return create_refresh_token(
            identity=str(user.user_id), expires_delta=self.refresh_token_expires
        )

    def validate_access_token(self, token: str) -> bool:
        try:
            decoded = decode_token(token)
            if decoded.get("type") != "access":
                return False
            return True
        except (InvalidTokenError, ExpiredSignatureError, DecodeError, Exception):
            return False

    def validate_refresh_token(self, token: str) -> bool:
        try:
            decoded = decode_token(token)
            if decoded.get("type") != "refresh":
                return False
            return True
        except (InvalidTokenError, ExpiredSignatureError, DecodeError, Exception):
            return False

    def get_uuid_from_token(self, token: str) -> Optional[UUID]:
        try:
            decoded = decode_token(token)
            identity = decoded.get("sub")
            if identity:
                return UUID(identity)
            return None
        except (
            InvalidTokenError,
            ExpiredSignatureError,
            DecodeError,
            ValueError,
            Exception,
        ):
            return None
