from Classes.Parsers.Parser import Parser


class WatchChecks(Parser):

    def __init__(self, game):
        Parser.__init__(self, "Watch Check Ratio")

    def parse(self, event):
        if event == "watch checked to add time.":
            self.results.append(True)
        elif event == "watch checked.":
            self.results.append(False)
