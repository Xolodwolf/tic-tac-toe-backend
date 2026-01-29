from typing import Tuple
from web.model.jwt_request_dto import JwtRequestDto
from web.model.jwt_response_dto import JwtResponseDto
from web.model.refresh_jwt_request_dto import RefreshJwtRequestDto


class JwtMapper:
    @staticmethod
    def to_jwt_request(dto: JwtRequestDto) -> Tuple[str, str]:
        return (dto.login, dto.password)

    @staticmethod
    def to_jwt_response_dto(
        type: str, access_token: str, refresh_token: str
    ) -> JwtResponseDto:
        return JwtResponseDto(
            type=type, access_token=access_token, refresh_token=refresh_token
        )

    @staticmethod
    def to_refresh_jwt_request(dto: RefreshJwtRequestDto) -> str:
        return dto.refresh_token

    @staticmethod
    def jwt_response_to_dict(dto: JwtResponseDto) -> dict:
        return {
            "type": dto.type,
            "access_token": dto.access_token,
            "refresh_token": dto.refresh_token,
        }
