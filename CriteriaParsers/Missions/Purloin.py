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
        self.pending = False
        self.current = ""
        if self.bar:
            self.took_drink = False
        else:
            self.list_on_tray = True

    def parse(self, event):
        if self.complete:
            return

        if self.bar:
            if event == "delegating purloin guest list.":
                self.took_drink = False
                self.pending = True
                self.current += "Delegate"
            elif event.desc in drink_accepts:
                self.took_drink = True
            elif event == "guest list purloined.":
                if not self.pending:
                    self.results.append("Direct Purloin.")
                else:
                    self.results.append(self.current+" took.")
                    self.current = ""
                self.complete = True
            elif "delegated purloin to" in event.desc:
                if not self.took_drink:
                    self.current += " cheese"
                self.current += " to "+event.characters[0].role
            elif event == "delegated purloin timer expired.":
                self.pending = False
                if not self.took_drink:
                    self.current += " cheese"
                self.results.append(self.current+" expired.")
                self.current = ""
            elif self.pending and "GameEnd" in event.categories:
                self.results.append(self.current+" pending...")

        else:  # tray toby
            if "ActionTest" in event.categories and event.mission == "Purloin":
                self.current = event.action_test
                self.current += " purloin" if self.list_on_tray else " return"
            elif event == "guest list purloin pending.":
                self.pending = True
            elif event == "guest list return pending.":
                self.pending = True
            elif self.pending and event.desc in drink_accepts:
                self.current += " cheese"
            elif event == "guest list purloined.":
                if self.pending:
                    self.current += " completed by "+event.characters[0].role
                self.results.append(self.current)
                self.list_on_tray = False
                self.pending = False
                self.current = ""
                # TODO with parameterization, disallow list returns
                # if only_take:
                #     self.complete = True
            elif event == "guest list returned.":
                if self.pending:
                    self.current += " completed by "+event.characters[0].role
                self.results.append(self.current)
                self.list_on_tray = True
                self.pending = False
                self.current = ""
            # TODO resolve the crash dilemma
            # elif event == "purloin guest list aborted.":
            #     if self.current == "":
            #         if len(self.results) == 0:
            #             self.results.append("*CRASH*")
            #         else:
            #             self.results[-1] += " *CRASH*"
            #     else:
            #         self.results.append(self.current+" *CRASH*")
            #     self.current = ""
            # TODO incorporate prints
            # elif not self.list_on_tray and event == "started fingerprinting drink.":
            #     self.results[-1] += " + fingerprint"
            elif "GameEnd" in event.categories:
                if self.pending:
                    self.results.append(self.current+" pending...")
                # elif self.current != "":
                #     self.results.append(self.current+"...")
                #     print(self.current + "...")

# TODO where are spies when a green purloin goes off? in cc, at statues/bar/books?

