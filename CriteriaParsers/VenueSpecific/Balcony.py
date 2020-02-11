from Classes.Parser import Parser


class BalconyThreeGreens(Parser):

    def __init__(self):
        Parser.__init__(self, "Balcony Three Green Games")

    def prepare(self, game):
        pass

    def parse(self, event):
        if self.complete:
            return
        # TODO finish; what should this return?
