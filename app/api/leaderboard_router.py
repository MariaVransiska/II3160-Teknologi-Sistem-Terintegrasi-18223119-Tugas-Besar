from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def leaderboard_stub():
    return {"msg": "Leaderboard Context — Stub Endpoint"}