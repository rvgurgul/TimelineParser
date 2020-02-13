from Classes.Parser import Parser
from Constants.Events import *


class DrinkOffers(Parser):

    def __init__(self, game):
        Parser.__init__(self, "Drink Accept Ratio")

    def parse(self, event):
        if event.desc in drink_accepts:
            self.results.append(True)
        elif event.desc in drink_rejects:
            self.results.append(False)
        # TODO differentiate purloin and fingerprintable drinks


class DrinkSips(Parser):

    def __init__(self, game):
        Parser.__init__(self, "Drink Gulp Ratio")

    def parse(self, event):
        if event.desc in drink_sips:
            self.results.append(False)
        elif event.desc in drink_gulps:
            self.results.append(True)
