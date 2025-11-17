class KDA:
    def __init__(self, kills: int = 0, deaths: int = 0, assists: int = 0):
        self.kills = int(kills)
        self.deaths = int(deaths)
        self.assists = int(assists)

    @property
    def ratio(self) -> float:
        return (self.kills + self.assists) / max(1, self.deaths)
