from pydantic import BaseModel, Field
from typing import List, Optional

class GameAccount(BaseModel):
    game: str
    external_id: str

class ProfileCreate(BaseModel):
    player_id: str
    display_name: Optional[str] = None
    country: Optional[str] = None
    game_accounts: List[GameAccount] = Field(default_factory=list)
    bio: Optional[str] = None

class ProfileOut(ProfileCreate):
    pass