from Classes.Parser import Parser


class ModerneFourEight(Parser):

    def __init__(self):
        Parser.__init__(self, "Moderne 4/8 Retroactive Result")
        self.missions = 0
        self.countdown = 0

    def prepare(self, game):
        self.results = game.specific_win_condition
        if game.venue != "Moderne" or game.mode != "a5/8" or game.specific_win_condition == "MissionsWin":
            self.complete = True

    def parse(self, event):
        if self.complete:
            return

        if "MissionComplete" in event.categories:
            self.missions += 1
            if self.missions == 4:
                self.countdown = event.time + 10
        elif self.countdown > 0:
            if event.time <= self.countdown:
                if "SniperShot" in event.categories:
                    self.complete = True
                    if event.characters[0].role == "Spy":
                        self.results = "SpyShot during Retroactive Countdown"
                    else:
                        self.results = "CivilianShot during Retroactive Countdown"
            else:  # event.time > self.countdown (spy has survived countdown)
                self.results = "Retroactive MissionsWin before " + self.results
                self.complete = True
