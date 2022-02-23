class PrositeHit():

    def __init__(self, score, profile_code, keywords = [], penalty_keywords = []):
        self.score = score
        self.profile_code = profile_code
        self.keywords = keywords
        self.percentage = 0
        self.penalty_keywords = penalty_keywords

    def get_score(self):
        return self.score

    def get_profile_code(self):
        return self.profile_code

    def get_keywords(self):
        return self.keywords

    def get_penalty_keywords(self):
        return self.penalty_keywords

    def set_percentage(self, perc):
        self.percentage = perc

    def get_percentage(self):
        return self.percentage
        
    def has_keywords(self):
        return len(self.keywords) > 0

    def has_penalty_keywords(self):
        return len(self.penalty_keywords) > 0
