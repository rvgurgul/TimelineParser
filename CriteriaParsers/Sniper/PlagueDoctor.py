from Classes.Parser import Parser


class PlagueDoctor(Parser):

    def __init__(self):
        Parser.__init__(self, "Shot for Cough")
        self.cough_timestamp = 0
        self.red_tested = False

    def prepare(self, game):
        if game.specific_win_condition not in ["SpyShot", "CivilianShot"]:
            self.complete = True

    def parse(self, event):
        if self.complete:
            return

        if "ActionTest" in event.categories and event.mission == "Contact" and event.action_test == "Red":
            self.red_tested = True
        elif self.red_tested and "uttered." in event.desc:
            self.cough_timestamp = event.time
        elif event == "banana bread aborted.":
            self.cough_timestamp = event.time
        elif self.cough_timestamp > 0 and "SniperShot" in event.categories:
            diff = round(event.time - self.cough_timestamp, 1)
            self.results = (diff, event.characters[0].role)
