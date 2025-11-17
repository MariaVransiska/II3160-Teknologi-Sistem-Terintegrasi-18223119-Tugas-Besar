from datetime import datetime, timezone
from app.domain.performance_summary import PerformanceSummary
from app.domain.player_id import PlayerId

class PerformanceUpdated:
    def __init__(self, player_id: PlayerId, new_summary: PerformanceSummary):
        self.player_id = player_id
        self.new_summary = new_summary
        self.timestamp = datetime.now(timezone.utc)