from Classes.Parser import Parser


class Overtime(Parser):

    def __init__(self, game):
        Parser.__init__(self, "Overtime")
        if not game.reaches_mwc:
            self.complete = True
        else:
            self.time_limit = game.clock
            self.final = game.missions_complete[-1]

    def parse(self, event):
        if self.complete:
            return

        if event == "45 seconds added to match.":
            self.time_limit += 45
        elif event.time > self.time_limit:
            self.results = (self.final, -1*event.clock)
