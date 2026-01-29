from typing import List
from domain.model.leader_stats import LeaderStats
from web.model.leaderboard_dto import LeaderboardEntryDto


class LeaderboardMapper:
    @staticmethod
    def to_dto(leader_stats: LeaderStats) -> LeaderboardEntryDto:
        return LeaderboardEntryDto(
            user_id=str(leader_stats.user_id),
            login=leader_stats.login,
            win_ratio=round(leader_stats.win_ratio, 3),
        )

    @staticmethod
    def to_dto_list(leaders: List[LeaderStats]) -> List[dict]:
        return [
            {
                "user_id": str(leader.user_id),
                "login": leader.login,
                "win_ratio": round(leader.win_ratio, 3),
            }
            for leader in leaders
        ]
