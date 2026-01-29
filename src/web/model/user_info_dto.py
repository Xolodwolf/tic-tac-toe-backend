from dataclasses import dataclass


@dataclass
class UserInfoDto:
    user_id: str
    login: str
