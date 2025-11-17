from app.domain.external_player_id import ExternalPlayerID

class ExternalGameAccount:
    def __init__(self, game_name: str, external_player_id: ExternalPlayerID):
        self.game_name = game_name
        self.external_player_id = external_player_id
