from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def player_profile_stub():
    return {"msg": "Player Profile Context — Stub Endpoint"}
