from Classes.Parsers.Parser import Parser


class BalconyThreeGreens(Parser):

    def __init__(self, game):
        Parser.__init__(self, "Balcony Three Green Games")
        self.results = game.specific_win_condition
        if game.venue != "Moderne" or game.mode != "a5/8" or game.specific_win_condition == "MissionsWin":
            self.complete = True
        else:
            self.missions = 0
            self.countdown = 0

    def parse(self, event):
        if self.complete:
            return
        # TODO finish; what should this return?
