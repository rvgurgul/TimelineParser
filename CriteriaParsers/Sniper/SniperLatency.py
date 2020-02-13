from Classes.Parser import Parser


class SniperLatency(Parser):

    def __init__(self, game):
        Parser.__init__(self, "Shot Latency")
        self.timestamp = 0

    def parse(self, event):
        if event == "took shot.":
            self.timestamp = event.time
        # elif event == "sniper shot too late for sync.":
        #     self.results = round(event.time-self.timestamp, 1) * 100
        elif "shot" in event.desc:
            self.results = round(event.time-self.timestamp, 1)
