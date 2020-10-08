class IScore:
    def __init__(self,weight):
        self.weight = weight

    def getScore(self):
        pass
class Score(IScore):
    # def __init__(self,weight):
    #     super().__init__(weight)
    def getScore(self):
        return self.weight
class ScoreDecorator(IScore):
    def __init__(self,I_Score):
        self._Score = I_Score
    def getScore(self):
        return self._Score.weight

class BadScore(ScoreDecorator):
    def getScore(self):
        return super().getScore() + 1
a = Score(2)

a = BadScore(a)
print(type(a))


