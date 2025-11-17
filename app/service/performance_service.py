from app.domain.player_id import PlayerId
from app.domain.match_record import MatchRecord
from app.domain.player_performance import PlayerPerformance

class PerformanceService:
    def __init__(self):
        self.player_performances = {}

    def ingest_match(self, match: MatchRecord):
        player_id = match.player_id
        if player_id.value not in self.player_performances:
            self.player_performances[player_id.value] = PlayerPerformance(player_id=player_id)

        performance = self.player_performances[player_id.value]
        event = performance.add_match(match)
        return performance, event

    def get_performance(self, player_id_str: str):
        player_id = PlayerId(player_id_str)
        return self.player_performances.get(player_id.value)
