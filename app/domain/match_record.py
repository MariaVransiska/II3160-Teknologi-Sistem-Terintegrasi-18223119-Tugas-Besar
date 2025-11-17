from datetime import datetime
from app.domain.player_id import PlayerId

class MatchRecord:
    def __init__(self, match_id: str, player_id: PlayerId, game_name: str,
                 kills: int, deaths: int, assists: int, score: float,
                 accuracy: float, timestamp: datetime):
        self.match_id = match_id
        self.player_id = player_id
        self.game_name = game_name
        self.kills = int(kills)
        self.deaths = int(deaths)
        self.assists = int(assists)
        self.score = float(score)
        self.accuracy = float(accuracy)
        self.timestamp = timestamp
