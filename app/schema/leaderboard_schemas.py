from pydantic import BaseModel
from typing import Optional

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

class LeaderboardItem(BaseModel):
    player_id: str
    summary: SummaryOut
    last_updated: Optional[str] = None