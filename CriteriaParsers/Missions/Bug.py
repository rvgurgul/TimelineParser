from Classes.Parser import Parser


class BugAttempts(Parser):

    def __init__(self):
        Parser.__init__(self, "Bug Attempts")
        self.bug_type = ""
        self.planting = False
        self.in_convo = False
        self.transit = False

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
            self.results.append(self.bug_type)
            self.complete = True
        elif event == "begin planting bug while walking.":
            self.planting = True
            if self.in_convo:
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
            # failure is implicit to any bug before the last
            # the last bug is a fail if bug is not completed
            self.bug_type += " (Failed)"
            self.results.append(self.bug_type)
            self.bug_type = ""
