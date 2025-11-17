from datetime import datetime, timezone
from typing import List
from app.domain.player_id import PlayerId
from app.domain.kda import KDA
from app.domain.performance_summary import PerformanceSummary
from app.domain.match_record import MatchRecord
from app.domain.events import PerformanceUpdated

class PlayerPerformance:
    def __init__(self, player_id: PlayerId):
        self.player_id = player_id
        self.games_played = 0
        self.total_kills = 0
        self.total_deaths = 0
        self.total_assists = 0
        self.total_score = 0.0
        self.accuracy_history: List[float] = []
        self.performance_summary: PerformanceSummary | None = None
        self.match_history: List[MatchRecord] = []
        self.last_updated = None

    def add_match(self, match: MatchRecord) -> PerformanceUpdated:
        # update counters
        self.match_history.append(match)
        self.games_played += 1
        self.total_kills += match.kills
        self.total_deaths += match.deaths
        self.total_assists += match.assists
        self.total_score += match.score
        self.accuracy_history.append(match.accuracy)

        kda_vo = KDA(kills=self.total_kills, deaths=self.total_deaths, assists=self.total_assists)
        avg_acc = sum(self.accuracy_history) / len(self.accuracy_history) if self.accuracy_history else 0.0
        avg_score = self.total_score / self.games_played if self.games_played else 0.0

        win_rate = getattr(self.performance_summary, "win_rate", 0.0)

        prev_ratio = getattr(self.performance_summary.kda, "ratio", None) if self.performance_summary else None
        current_ratio = kda_vo.ratio
        if prev_ratio is None:
            trend = "stable"
        else:
            trend = "up" if current_ratio > prev_ratio else ("down" if current_ratio < prev_ratio else "stable")

        self.performance_summary = PerformanceSummary(
            kda=kda_vo,
            win_rate=win_rate,
            accuracy=avg_acc,
            avg_score=avg_score,
            trend=trend
        )

        self.last_updated = datetime.now(timezone.utc)

        # return domain event
        return PerformanceUpdated(self.player_id, self.performance_summary)
