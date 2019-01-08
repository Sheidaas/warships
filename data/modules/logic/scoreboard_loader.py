import json


class ScoreLoader:

    def __init__(self, path):
        self.score = {}
        self.file_destination = path + '/scoreboard.json'

    def load_score(self):
        with open(self.file_destination, 'r') as file:
            data = file.read()
            self.score = json.loads(data)

    def save_score(self):
        with open(self.file_destination, 'w') as file:
            file.write(json.dumps(self.score, indent=4))

    def return_scoreboard(self):
        self.load_score()
        score = Scoreboard()
        score.score = self.score
        return score

class Scoreboard:

    def __init__(self):
        self.score = {}
