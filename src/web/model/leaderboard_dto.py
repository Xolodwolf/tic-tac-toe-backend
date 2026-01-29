from dataclasses import dataclass


@dataclass
class LeaderboardEntryDto:
    user_id: str
    login: str
    win_ratio: float
