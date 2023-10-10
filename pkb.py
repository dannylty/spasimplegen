class PKB:
    def __init__(self):
        self.relationships = set()

    def add_relationship(self, rs):
        self.relationships.add(rs)