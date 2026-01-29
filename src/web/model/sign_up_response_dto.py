from dataclasses import dataclass


@dataclass
class SignUpResponseDto:
    success: bool
    message: str
