from app.domain.kda import KDA

class PerformanceSummary:
    def __init__(self, kda: KDA, win_rate: float, accuracy: float, avg_score: float, trend: str):
        self.kda = kda
        self.win_rate = float(win_rate)
        self.accuracy = float(accuracy)
        self.avg_score = float(avg_score)
        self.trend = trend
