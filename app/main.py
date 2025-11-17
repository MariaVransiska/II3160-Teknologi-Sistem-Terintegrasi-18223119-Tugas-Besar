from fastapi import FastAPI
from app.api.performance_router import router as performance_router

app = FastAPI(title="Game Tracker - Performance Analytics")

app.include_router(performance_router, prefix="/performance", tags=["Performance"])

@app.get("/")
def root():
    return {"msg": "Game Tracker Performance Analytics API"}
