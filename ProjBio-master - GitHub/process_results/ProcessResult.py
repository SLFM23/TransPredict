class ProcessResult():

    def __init__(self, sequence_name):
        self.sequence_name = sequence_name
        self.tmhmm = None
        self.tmbb = None
        self.prosite = None
        self.cdd = None
        self.final_score = None

    def get_tmhmm(self):
        return self.tmhmm

    def get_tmbb(self):
        return self.tmbb

    def get_prosite(self):
        return self.prosite

    def get_cdd(self):
        return self.cdd

    def get_final_score(self):
        return self.final_score

    def get_sequence_name(self):
        return self.sequence_name

    def set_tmhmm(self, tmhmm):
        self.tmhmm = tmhmm

    def set_tmbb(self, tmbb):
        self.tmbb = tmbb

    def set_prosite(self, prosite):
        self.prosite = prosite

    def set_cdd(self, cdd):
        self.cdd = cdd

    def set_final_score(self, final_score):
        self.final_score = final_score