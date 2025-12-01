from pydantic import BaseModel
from datetime import datetime

class MatchIn(BaseModel):
    match_id: str
    player_id: str
    game_name: str
    kills: int
    deaths: int
    assists: int
    score: float
    accuracy: float
    timestamp: datetime

class KdaOut(BaseModel):
    kills: int
    deaths: int
    assists: int
    ratio: float
    
class SummaryOut(BaseModel):
    kda: KdaOut
    win_rate: float
    accuracy: float
    avg_score: float
    trend: str

class PerformanceOut(BaseModel):
    player_id: str
    summary: dict
    last_updated: datetime | None
