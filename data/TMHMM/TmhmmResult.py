class TmhmmResult():

    def __init__(self, error, tmhs = 0):
        self.error = error
        self.tmhs = tmhs
        self.percentage = 0

    def get_tmhs(self):
        return self.tmhs
    
    def has_helix(self):
        return self.tmhs > 0

    def is_error(self):
        return self.error

    def set_percentage(self, perc):
        self.percentage = perc

    def get_percentage(self):
        return self.percentage