from fastapi import APIRouter, HTTPException
from typing import Dict
from app.schema.profile_schemas import ProfileCreate, ProfileOut

router = APIRouter()

_PROFILE_STORE: Dict[str, Dict] = {}

@router.post("/", response_model=ProfileOut)
def create_profile(profile: ProfileCreate):
    pid = profile.player_id
    if not pid:
        raise HTTPException(status_code=400, detail="player_id required")
    if pid in _PROFILE_STORE:
        raise HTTPException(status_code=409, detail="profile already exists")
    _PROFILE_STORE[pid] = {
        "player_id": pid,
        "display_name": profile.display_name or pid,
        "country": profile.country,
        "game_accounts": profile.game_accounts or [],
        "bio": profile.bio,
    }
    return ProfileOut.model_validate(_PROFILE_STORE[pid])

@router.get("/{player_id}", response_model=ProfileOut)
def get_profile(player_id: str):
    prof = _PROFILE_STORE.get(player_id)
    if not prof:
        raise HTTPException(status_code=404, detail="profile not found")
    return ProfileOut.model_validate(prof)

@router.put("/{player_id}", response_model=ProfileOut)
def update_profile(player_id: str, updates: ProfileCreate):
    """
    Update profil pemain (upsert field yang dikirim).
    """
    prof = _PROFILE_STORE.get(player_id)
    if not prof:
        raise HTTPException(status_code=404, detail="profile not found")

    upd = updates.model_dump(exclude_unset=True)
    for key in ("display_name", "country", "game_accounts", "bio"):
        if key in upd:
            prof[key] = upd[key]

    _PROFILE_STORE[player_id] = prof
    return ProfileOut.model_validate(prof)

@router.delete("/{player_id}")
def delete_profile(player_id: str):
    if player_id not in _PROFILE_STORE:
        raise HTTPException(status_code=404, detail="profile not found")
    del _PROFILE_STORE[player_id]
    return {"ok": True}