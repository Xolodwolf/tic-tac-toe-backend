from uuid import UUID
from dataclasses import dataclass


@dataclass
class LeaderStats:
    user_id: UUID
    login: str
    win_ratio: float

    def __repr__(self):
        return f"<LeaderStats(user_id={self.user_id}, login={self.login}, win_ratio={self.win_ratio:.3f})>"
