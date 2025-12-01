from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def notification_stub():
    return {"msg": "Notification Context — Stub Endpoint"}
