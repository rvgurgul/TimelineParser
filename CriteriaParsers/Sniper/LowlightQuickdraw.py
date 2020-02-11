from Classes.Parser import Parser


class LowlightQuickdraw(Parser):

    def __init__(self):
        Parser.__init__(self, "Cast Lowlight Time")
        self.cast = {"Toby": False, "Damon": False}

    def prepare(self, game):
        self.cast[game.get_characters_in_role("Ambassador")] = False
        if game.venue != "Balcony":
            sda_list = game.get_characters_in_role("SuspectedDoubleAgent", force_list=True)
            for sda in sda_list:
                self.cast[sda] = False
            self.cast[game.get_characters_in_role("DoubleAgent")] = False

    def parse(self, event):
        if self.complete:
            return

        if "SniperLights" in event.categories:
            # disqualify and game where lowlights occur 'before' the game starts
            if event.time <= 0:
                self.complete = True
                return

            chara = event.characters[0].name
            if chara in self.cast:
                self.cast[chara] = True
                if all(self.cast.values()):
                    self.results = event.time
                    self.complete = True
