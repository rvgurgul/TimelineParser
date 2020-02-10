from Classes.Parser import Parser


class FlirtDowntime(Parser):

    def __init__(self):
        Parser.__init__(self, "Flirt Downtime")
        self.cooldown_timestamp = 0

    def parse(self, event):
        if event.desc == "action triggered: seduce target" and self.cooldown_timestamp > 0:
            self.results.append(round(event.time - self.cooldown_timestamp, 1))
            # print("flirt at", event.time)
        elif event.desc == "flirtation cooldown expired.":
            self.cooldown_timestamp = event.time
            # print("expired at", event.time)
