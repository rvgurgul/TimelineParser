from Classes.Parser import Parser


class ContactInitiations(Parser):

    def __init__(self):
        Parser.__init__(self, "Contact Attempts")
        self.joiner, self.atr, self.outcome = "Neither", "NoAT", ""
        self.dough, self.bread = "", ""
        self.da_in_with_spy = False
        self.baking = None

    def parse(self, event):
        if event == "action triggered: contact double agent":
            self.baking = True
        elif event == "real banana bread started.":
            self.dough = "Real"
        elif event == "fake banana bread started.":
            self.dough = "Fake"

        elif event == "double agent contacted.":  # "banana bread uttered.":
            self.bread = "Real"
            self.baking = False
        elif event == "fake banana bread uttered.":
            self.bread = "Fake"
            self.baking = False
        elif event == "banana bread aborted.":
            self.bread = "Cough"
            self.baking = False
            if self.atr == "Red":
                self.bread = "*Cough Cough Cough Cough*"
            self.atr += " (Canceled)"

        elif event == "spy joined conversation with double agent.":
            self.joiner = "Spy joins Double Agent"
            self.da_in_with_spy = True
        elif event == "double agent joined conversation with spy.":
            self.joiner = "Double Agent joins Spy"
            self.da_in_with_spy = True
        elif event == "double agent left conversation with spy.":
            self.da_in_with_spy = False
            if self.baking:
                self.atr += " (Sunshined)"
            else:
                self.joiner += ", Double Agent leaves"
        elif event == "spy left conversation with double agent.":
            self.da_in_with_spy = False
            self.joiner += ", Spy leaves"
        elif event == "left alone while attempting banana bread.":
            self.baking = False
            self.bread = "Raw"

        elif "ActionTest" in event.categories and event.mission == "Contact":
            self.atr = event.action_test

        if self.baking is False:
            self.baking = None
            if self.dough == self.bread:
                self.outcome = self.bread
            else:
                self.outcome = self.dough + " turned " + self.bread
            package = self.joiner, self.atr, self.outcome
            self.results.append(package)
            # if package[1] == '':
            #     print(self.jason["uuid"], jason["spy"])
            #     print(contacts)
            self.joiner, self.atr, self.outcome = "Neither", "", ""
