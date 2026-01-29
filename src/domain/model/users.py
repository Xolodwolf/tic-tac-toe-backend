from uuid import UUID


class User:
    def __init__(self, user_id: UUID, login: str, password: str):
        self.user_id = user_id
        self.login = login
        self.password = password
