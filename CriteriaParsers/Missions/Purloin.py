from Classes.Parser import Parser
from Constants.Venues import bar_venues


class DelegateTime(Parser):

    def __init__(self, game):
        Parser.__init__(self, "Delegate Take Time")
        if game.venue not in bar_venues:
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
