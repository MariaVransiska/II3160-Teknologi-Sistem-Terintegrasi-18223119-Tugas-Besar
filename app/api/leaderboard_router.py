from fastapi import APIRouter, Query, HTTPException
from typing import Dict, List
from app.schema.leaderboard_schemas import LeaderboardItem

router = APIRouter()

_LEADERBOARD_STORE: Dict[str, Dict] = {}

def _score_key(entry: Dict) -> float:
    summary: Dict = entry.get("summary", {})
    kda: Dict = summary.get("kda", {})
    avg_score = summary.get("avg_score", 0.0)
    ratio = kda.get("ratio", 0.0)
    return avg_score + 0.01 * ratio

@router.post("/upsert", response_model=Dict[str, bool])
def upsert_leaderboard_item(item: LeaderboardItem):
    """
    Upsert item leaderboard menggunakan schema LeaderboardItem.
    """
    pid = item.player_id
    _LEADERBOARD_STORE[pid] = item.model_dump()
    return {"ok": True}

@router.get("/", response_model=List[LeaderboardItem])
def get_leaderboard(limit: int = Query(10, ge=1, le=100)):
    """
    Mengembalikan top-N pemain berdasarkan avg_score (tie-break ratio KDA).
    """
    entries = list(_LEADERBOARD_STORE.values())
    entries.sort(key=_score_key, reverse=True)
    return [LeaderboardItem.model_validate(e) for e in entries[:limit]]

@router.get("/player/{player_id}", response_model=LeaderboardItem)
def get_player_rank(player_id: str):
    """
    Ambil satu item leaderboard berdasarkan player_id.
    """
    entry = _LEADERBOARD_STORE.get(player_id)
    if not entry:
        raise HTTPException(status_code=404, detail="leaderboard item not found")
    return LeaderboardItem.model_validate(entry)