class CddResult():

    def __init__(self, error, numhits = 0, hits = []):
        self.error = error
        self.numhits = numhits
        self.hits = hits
        self.percentage = 0

    def is_error(self):
        return self.error

    def get_numhits(self):
        return self.numhits
        
    def get_hits(self):
        return self.hits

    def set_percentage(self, perc):
        self.percentage = perc

    def get_percentage(self):
        return self.percentage