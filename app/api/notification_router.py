from fastapi import APIRouter, HTTPException
from typing import List, Dict
from datetime import datetime, timezone

router = APIRouter()

_NOTIF_STORE: Dict[str, List[Dict]] = {}

@router.post("/{player_id}")
def push_notification(player_id: str, payload: Dict):
    """
    Tambah notifikasi untuk player:
    Body contoh:
    { "type": "PERFORMANCE_UPDATED", "message": "Summary updated", "data": {...} }
    """
    notif = {
        "type": payload.get("type", "GENERAL"),
        "message": payload.get("message", ""),
        "data": payload.get("data"),
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    _NOTIF_STORE.setdefault(player_id, []).append(notif)
    return {"ok": True, "count": len(_NOTIF_STORE[player_id])}

@router.get("/{player_id}", response_model=List[Dict])
def list_notifications(player_id: str):
    """
    Ambil semua notifikasi milik player_id.
    """
    return _NOTIF_STORE.get(player_id, [])

@router.delete("/{player_id}")
def clear_notifications(player_id: str):
    """
    Hapus semua notifikasi untuk player_id.
    """
    if player_id not in _NOTIF_STORE:
        raise HTTPException(status_code=404, detail="no notifications for player")
    _NOTIF_STORE[player_id] = []
    return {"ok": True}