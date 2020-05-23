class Score :

    def __init__(self):
        self.travel_score = []
        self.score = 0.0


    def evaluate(self, distance_):
        self.score += distance_

    def share_by_position(self,id):
        return self.travel_score[id]