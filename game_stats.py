import json

class GameStats():
    def __init__(self, settings):
        self.settings = settings
        self.game_active = False
        self.reset_stats()
        self.high_score = None
        self.level = 1
        self.high_scores_all = None
        self.initialize_high_score()

    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
        self.score = 0

    def initialize_high_score(self):
        """Read the saved high score from the json file"""
        with open('high_score_data.json', 'r') as file:
            self.top_high_scores = json.load(file)
            self.top_high_scores.sort(reverse=True)
            self.high_score = self.top_high_scores[0]

    def save_high_score(self):
        """Save the high score to a json file"""
        for i in range(len(self.top_high_scores)):
            if self.score >= self.top_high_scores[i]:
                self.top_high_scores[i] = self.score
                break
        with open('high_score_data.json', 'w') as file:
            json.dump(self.top_high_scores, file)