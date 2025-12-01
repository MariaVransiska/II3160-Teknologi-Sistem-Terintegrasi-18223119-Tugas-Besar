from fastapi import FastAPI

from app.api.performance_router import router as performance_router
from app.auth.auth_router import router as auth_router
from app.api.player_profile_router import router as profile_router
from app.api.leaderboard_router import router as leaderboard_router
from app.api.notification_router import router as notification_router

app = FastAPI(title="Game Tracker - Performance Analytics")

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(performance_router, prefix="/performance", tags=["Performance"])
app.include_router(profile_router, prefix="/profile", tags=["Player Profile"])
app.include_router(leaderboard_router, prefix="/leaderboard", tags=["Leaderboard"])
app.include_router(notification_router, prefix="/notification", tags=["Notification"])

@app.get("/")
def root():
    return {"msg": "Game Tracker Performance Analytics API"}
