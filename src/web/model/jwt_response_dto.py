class JwtResponseDto:
    def __init__(self, type: str, access_token: str, refresh_token: str):
        self.type = type  # "Bearer"
        self.access_token = access_token
        self.refresh_token = refresh_token
