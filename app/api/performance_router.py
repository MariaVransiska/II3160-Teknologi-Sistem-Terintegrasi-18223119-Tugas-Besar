from fastapi import APIRouter, HTTPException
from datetime import timezone
from app.schema.performance_schemas import MatchIn, PerformanceOut, KdaOut
from app.domain.player_id import PlayerId
from app.domain.match_record import MatchRecord
from app.service.performance_service import PerformanceService

router = APIRouter()
service = PerformanceService()

@router.post("/ingest", response_model=PerformanceOut)
def ingest_match(payload: MatchIn):
    player_id = PlayerId(payload.player_id)
    match = MatchRecord(
        match_id=payload.match_id,
        player_id=player_id,
        game_name=payload.game_name,
        kills=payload.kills,
        deaths=payload.deaths,
        assists=payload.assists,
        score=payload.score,
        accuracy=payload.accuracy,
        timestamp=payload.timestamp
    )

    performance, event = service.ingest_match(match)
    if not performance or not performance.performance_summary:
        raise HTTPException(status_code=500, detail="failed to compute performance")

    k = performance.performance_summary.kda
    kda_out = {
        "kills": k.kills,
        "deaths": k.deaths,
        "assists": k.assists,
        "ratio": k.ratio
    }

    summary = {
        "kda": kda_out,
        "win_rate": performance.performance_summary.win_rate,
        "accuracy": performance.performance_summary.accuracy,
        "avg_score": performance.performance_summary.avg_score,
        "trend": performance.performance_summary.trend,
    }

    return {
        "player_id": performance.player_id.value,
        "summary": summary,
        "last_updated": performance.last_updated
    }

@router.get("/performance/{player_id}", response_model=PerformanceOut)
def get_performance(player_id: str):
    perf = service.get_performance(player_id)
    if not perf or not perf.performance_summary:
        raise HTTPException(status_code=404, detail="player performance not found")
    k = perf.performance_summary.kda
    kda_out = {
        "kills": k.kills,
        "deaths": k.deaths,
        "assists": k.assists,
        "ratio": k.ratio
    }
    summary = {
        "kda": kda_out,
        "win_rate": perf.performance_summary.win_rate,
        "accuracy": perf.performance_summary.accuracy,
        "avg_score": perf.performance_summary.avg_score,
        "trend": perf.performance_summary.trend,
    }
    return {
        "player_id": perf.player_id.value,
        "summary": summary,
        "last_updated": perf.last_updated
    }