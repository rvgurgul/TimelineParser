from Classes.Parser import Parser
from Constants.Events import drink_accepts, drink_finishes


class BugAttempts(Parser):

    def __init__(self, game):
        Parser.__init__(self, "Bug Attempts")
        self.bug_type = ""
        self.planting = False
        self.in_convo = False
        self.transit = False
        # while the spy cannot bug with both hands occupied, both objects must be stored
        #  in the case that they bug following a briefcase return/drink finish
        self.holding_left = None
        self.holding_case = False

    def parse(self, event):
        if self.complete:
            return

        if event == "spy enters conversation.":
            if self.transit or self.bug_type == "Exit":
                self.bug_type = "Twitch"
            elif self.planting:
                self.bug_type = "Entry"
            self.in_convo = True
        elif event == "spy leaves conversation.":
            if self.transit or self.bug_type == "Entry":
                self.bug_type = "Twitch"
            elif self.planting:
                self.bug_type = "Exit"
            self.in_convo = False
        elif "bugged ambassador while" in event.desc:
            self.bug_type += self.__held_objects()
            self.results.append(self.bug_type)
            self.complete = True
        elif event == "begin planting bug while walking.":
            self.planting = True
            if self.holding_case:
                self.bug_type = "Briefcase"
            elif self.in_convo:
                self.bug_type = "Reverse"
            else:
                self.bug_type = "Walking"
        elif event == "begin planting bug while standing.":
            self.planting = True
            self.bug_type = "Standing"
        elif event == "bug transitioned from standing to walking.":
            self.transit = True
        elif event == "failed planting bug while walking.":
            self.planting, self.transit = False, False
            self.bug_type += self.__held_objects()
            # failure is implicit to any bug before the last
            #  the last bug is also a fail if bug is not completed
            #  however, this appendition is useful for readability
            self.bug_type += " (Failed)"
            self.results.append(self.bug_type)
            self.bug_type = ""

        elif event.desc in drink_accepts:
            self.holding_left = "Drink"
        elif event.desc in drink_finishes:
            self.holding_left = None
        elif event == "get book from bookcase.":
            self.holding_left = "Book"
        elif event == "put book in bookcase.":
            self.holding_left = None
        elif event == "spy picks up briefcase.":
            self.holding_case = True
        elif event == "spy puts down briefcase." or event == "spy returns briefcase.":
            self.holding_case = False

    def __held_objects(self):
        if self.holding_left is not None:
            return " with a "+self.holding_left if not self.holding_case else " with BOTH HANDS FULL???"
        elif self.holding_case:
            return " with the Briefcase"
        return ""
