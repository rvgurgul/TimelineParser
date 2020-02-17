from Classes.Parser import Parser
from Constants.Events import lights_abbreviated


class ContactLowlights(Parser):

    def __init__(self, game):
        Parser.__init__(self, "Contact Lowlights")
        self.cast = {c.name: "DL" for c in game.cast if c.role in ["Spy", "SeductionTarget", "Civilian"]}
        if game.venue.name == "Balcony":  # unknown double agent
            self.cast[game.get_characters_in_role("DoubleAgent")] = "DL"
        self.bb_ts = 0
        self.snapshot = {}

    def parse(self, event):
        if "banana bread uttered" in event:
            self.bb_ts = event.time + 10
            self.snapshot = self.cast.copy()
        elif "SniperLights" in event.categories:
            chara = event.characters[0].name
            if chara in self.cast:
                self.cast[chara] = lights_abbreviated[event.desc]
        elif self.bb_ts > 0 and (event.time > self.bb_ts or "GameEnd" in event.categories):
            for chara in self.cast:
                if self.cast[chara] != self.snapshot[chara]:
                    res = "{}->{}".format(self.snapshot[chara], self.cast[chara])
                    self.results.append(res)
            self.bb_ts = 0

# TODO compare avg library lowlights before and after bookmarking
