from Classes.Parser import Parser


class BugExterminator(Parser):

    def __init__(self, game):
        Parser.__init__(self, "Bug Exterminations")
        self.spy, self.amba = game.get_characters_in_role("Spy"), game.get_characters_in_role("Ambassador")
        self.spylight, self.ambalight = "unmarked", "unmarked"
        self.bug_ts = 0
        self.outcome = "no reaction"
        self.light_pair = ("",)

    def parse(self, event):
        if "SniperLights" in event.categories:
            if event.characters[0].name == self.spy:
                self.spylight = event.desc
            elif event.characters[0].name == self.amba:
                self.ambalight = event.desc
        elif "begin planting bug while" in event:
            # assuming the bug takes about 1 second to land, the sniper gets 10 seconds to shoot
            self.bug_ts = event.time + 11
            self.light_pair = (self.spylight, self.ambalight)

        if event.time < self.bug_ts:
            if event == [
                "marked spy suspicious.",
                "marked spy neutral suspicion.",
                "marked spy less suspicious.",
            ]:
                self.outcome = event.desc
            elif event == [
                "sniper shot spy.",
                "missions completed successfully.",
                "spy ran out of time.",
            ]:
                # must separate game ending outcomes because no events follow to push to results
                self.results.append((self.light_pair, event.desc))
        elif event.time > self.bug_ts > 0:  # PogChamp I didn't know this could be done
            self.results.append((self.light_pair, self.outcome))
            self.bug_ts = 0
            self.outcome = "no reaction"
