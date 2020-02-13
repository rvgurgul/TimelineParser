from Classes.Parser import Parser


class ActionTestTimings(Parser):

    def __init__(self, game):
        Parser.__init__(self, "Action Test Timings")
        self.triggered_timestamp = 0

    def parse(self, event):
        if "action triggered:" in event.desc:
            self.triggered_timestamp = event.time
        elif "ActionTest" in event.categories:
            result = event.action_test
            if result != "Canceled":
                mission = event.mission
                if mission != "Fingerprint":
                    if mission == "NoMission":
                        mission = "Time Add"
                    package = round(event["elapsed_time"]-self.triggered_timestamp, 1), result, mission
                    self.results.append(package)
