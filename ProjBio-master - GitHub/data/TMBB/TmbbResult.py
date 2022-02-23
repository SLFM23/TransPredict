class TmbbResult():

    def __init__(self, error, score = -1):
        self.error = error
        self.score = score
        self.reference_score = 2.965
        self.percentage = 0

    def get_score(self):
        return self.score

    def is_error(self):
        return self.error
    
    def get_reference_score(self):
        return self.reference_score

    def is_beta(self):
        if self.score == -1:
            return False
        
        return self.score <= self.reference_score

    def set_percentage(self, perc):
        self.percentage = perc

    def get_percentage(self):
        return self.percentage