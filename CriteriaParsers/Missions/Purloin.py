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


class DelegateTime(Parser):

    def __init__(self, game):
        Parser.__init__(self, "Delegate Take Time")
        if game.venue.tray or "Purloin" not in game.missions_complete:
            self.complete = True
        else:
            self.delegate_timestamp = 0

    def parse(self, event):
        if event == "delegating purloin guest list.":
            self.delegate_timestamp = event.time
        elif event == "delegated purloin timer expired.":
            self.delegate_timestamp = 0
        elif event == "guest list purloined.":
            self.results = round(event.time-self.delegate_timestamp, 1) if self.delegate_timestamp > 0 else None
            self.complete = True


class DescribePurloin(Parser):

    def __init__(self, game):
        Parser.__init__(self, "Purloin Description")
        self.bar = game.venue.bar

    def parse(self, event):
        if self.complete:
            return

        if self.bar:

            pass
        else:


            pass



