from Classes.Game import TimelineEvent


class Parser:

    def __init__(self, criteria="Default"):
        self.critera = criteria
        self.results = []
        self.complete = False

    def parse(self, event: TimelineEvent):
        pass

    def get_results(self):
        return self.results
