from Classes.Game import TimelineEvent


# Generic Parser class defines functionality for all sub-Parsers
class Parser:

    # Criteria is a string representing the criteria parsed by the class
    # Results is a list (by default) which can hold/be changed to any desired return value
    # Complete is a boolean flag which parsers can use to disable themselves if they have reached a conclusive result
    def __init__(self, criteria):
        self.critera = criteria
        self.results = []
        self.complete = False

    # Parse is an optional overrideable method to perform a state transition given an event from the game's timeline
    def parse(self, event: TimelineEvent):
        pass

    # Returns the result stored by the parser
    def get_results(self):
        return self.results
