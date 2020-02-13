from Classes.Parser import Parser


class Overtime(Parser):

    def __init__(self, game):
        Parser.__init__(self, "Overtime")
        self.time_limit = game.clock

    def parse(self, event):
        if event == "45 seconds added to match.":
            self.time_limit += 45
        elif event.time > self.time_limit:
            self.results = -1*event.clock

    # TODO idk where to put this, but find the time between 'banana bread uttered.' and 'double agent contacted.'
    # TODO clock usage as a percent of start time; how to incorporate added time
