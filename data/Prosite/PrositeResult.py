class PrositeResult():

    def __init__(self, error, total_hits = 0, hits = []):
        self.error = error
        self.total_hits = total_hits
        self.hits = hits
        self.percentage = 0

    def is_error(self):
        return self.error

    def get_total_hits(self):
        return self.total_hits

    def get_hits(self):
        return self.hits

    def set_percentage(self, perc):
        self.percentage = perc

    def get_percentage(self):
        return self.percentage
        