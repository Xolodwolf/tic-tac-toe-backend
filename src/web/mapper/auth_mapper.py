from domain.model.sign_up_request import SignUpRequest
from domain.model.users import User
from web.model.sign_up_request_dto import SignUpRequestDto
from web.model.user_info_dto import UserInfoDto


class AuthMapper:
    @staticmethod
    def to_sign_up_request(dto: SignUpRequestDto) -> SignUpRequest:
        return SignUpRequest(login=dto.login, password=dto.password)

    @staticmethod
    def to_user_info_dto(user: User) -> UserInfoDto:
        return UserInfoDto(user_id=str(user.user_id), login=user.login)
