from Classes.Parser import Parser


class PendingDurations(Parser):

    def __init__(self, game):
        Parser.__init__(self, "Pending Durations")
        if "Swap" not in game.missions_complete or "Purloin" not in game.missions_complete:
            self.complete = True
        else:
            self.pending_swap = False
            self.pending_list = False

    def parse(self, event):
        if self.complete:
            return

        if not self.pending_swap:
            if event == "statue swap pending.":
                self.pending_swap = event.time
        else:
            if event == "statue swapped.":
                pkg = ("Swap", round(event.time-self.pending_swap, 1))
                self.results.append(pkg)

        if not self.pending_list:
            if event == "action test green: purloin guest list" \
                    or event == "guest list purloin pending." \
                    or "delegated purloin to" in event.desc:
                self.pending_list = event.time
        else:
            # TODO list returns???
            if event == "guest list purloined.":
                pkg = ("Purloin", round(event.time-self.pending_list, 1))
                self.results.append(pkg)
            elif event == "guest list returned.":
                pkg = ("Return", round(event.time-self.pending_list, 1))
                self.results.append(pkg)
            elif event == "delegated purloin timer expired.":
                self.pending_list = False


# if the game goes into pending overtime, what caused the OT, what was the last mission, what was the result?
def pendingOvertime(jason):
    pend_ts = 0
    pend_mi = ""
    pending = False
    for event in jason["timeline"]:
        if event["event"] == "missions completed. countdown pending.":
            print(event)
            pend_ts = event["elapsed_time"]
            pending = True
        elif pending and event["event"] == "missions completed. 10 second countdown.":
            pend_ts = round(event["elapsed_time"] - pend_ts, 1)
            print(pend_mi, "was pending for", pend_ts, "\bs")
        elif "MissionComplete" in event["category"]:
            pend_mi = event["mission"]
