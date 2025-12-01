from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.auth.auth_service import create_token, authenticate_user

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
def login(req: LoginRequest):
    user = authenticate_user(req.username, req.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token({"sub": user["username"]})
    return {"access_token": token, "token_type": "bearer"}
