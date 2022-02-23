class CddHit():

    def __init__(self, evalue, name, accession, superfamily):
        self.evalue = evalue
        self.name = name
        self.accession = accession
        self.superfamily = superfamily
        self.keywords = []
        self.penalty_keywords = []
        self.percentage = 0

    def get_superfamily(self):
        return self.superfamily

    def get_evalue(self):
        return self.evalue

    def get_accession(self):
        return self.accession

    def set_keywords(self, keywords):
        self.keywords = keywords

    def get_keywords(self):
        return self.keywords

    def set_penalty_keywords(self, penalty_keywords):
        self.penalty_keywords = penalty_keywords

    def get_penalty_keywords(self):
        return self.penalty_keywords

    def get_name(self):
        return self.name

    def set_percentage(self, perc):
        self.percentage = perc

    def get_percentage(self):
        return self.percentage
        
    def has_keywords(self):
        return len(self.keywords) > 0

    def has_penalty_keywords(self):
        return len(self.penalty_keywords) > 0