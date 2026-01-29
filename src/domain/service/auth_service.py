from typing import Optional
from uuid import UUID
from domain.service.user_service import UserService
from domain.service.jwt_provider import JwtProvider
from domain.model.sign_up_request import SignUpRequest
from web.model.jwt_request_dto import JwtRequestDto
from web.model.jwt_response_dto import JwtResponseDto


class AuthService:
    def __init__(self, user_service: UserService, jwt_provider: JwtProvider):
        self.user_service = user_service
        self.jwt_provider = jwt_provider

    def register(self, sign_up_request: SignUpRequest) -> bool:
        try:
            self.user_service.create_user(sign_up_request)
            return True
        except ValueError:
            return False

    def authenticate(self, jwt_request: JwtRequestDto) -> Optional[JwtResponseDto]:
        try:
            user = self.user_service.find_by_login(jwt_request.login)
            if not user:
                return None

            if not self.user_service.verify_password(user, jwt_request.password):
                return None

            access_token = self.jwt_provider.generate_access_token(user)
            refresh_token = self.jwt_provider.generate_refresh_token(user)

            return JwtResponseDto(
                type="Bearer", access_token=access_token, refresh_token=refresh_token
            )

        except Exception:
            return None

    def refresh_access_token(self, refresh_token: str) -> Optional[JwtResponseDto]:
        try:
            if not self.jwt_provider.validate_refresh_token(refresh_token):
                return None
            user_id = self.jwt_provider.get_uuid_from_token(refresh_token)
            if not user_id:
                return None

            user = self.user_service.find_by_id(user_id)
            if not user:
                return None

            new_access_token = self.jwt_provider.generate_access_token(user)

            return JwtResponseDto(
                type="Bearer",
                access_token=new_access_token,
                refresh_token=refresh_token,
            )

        except Exception:
            return None

    def refresh_refresh_token(self, refresh_token: str) -> Optional[JwtResponseDto]:
        try:
            if not self.jwt_provider.validate_refresh_token(refresh_token):
                return None

            user_id = self.jwt_provider.get_uuid_from_token(refresh_token)
            if not user_id:
                return None

            user = self.user_service.find_by_id(user_id)
            if not user:
                return None

            new_access_token = self.jwt_provider.generate_access_token(user)
            new_refresh_token = self.jwt_provider.generate_refresh_token(user)

            return JwtResponseDto(
                type="Bearer",
                access_token=new_access_token,
                refresh_token=new_refresh_token,
            )

        except Exception:
            return None

    def authenticate_by_token(self, access_token: str) -> Optional[UUID]:
        try:
            if not self.jwt_provider.validate_access_token(access_token):
                return None

            user_id = self.jwt_provider.get_uuid_from_token(access_token)
            return user_id

        except Exception:
            return None
