from Classes.Parser import Parser


class WatchCheckAnimations(Parser):

    def __init__(self, game):
        Parser.__init__(self, "Watch Check Animations")
        self.results = (game.get_characters_in_role("Spy"), [])
        self.ts = 0

    def parse(self, event):
        if event == "watch checked to add time.":
            self.ts = event.time
        elif event == "45 seconds added to match.":
            diff = round(event.time - self.ts, 1)
            self.results[1].append(diff)


# TODO convert to parser
# TODO this can also occur with a spy/civ shot, just never a mission win
def waning_time_add_fails(jason):
    if "TimeOut" not in jason["win_type"]:
        return

    resolved = True
    for event in jason["timeline"]:
        if event["event"] == "spy ran out of time." and not resolved:
            return get_characters_of_role(jason, "Spy")
        elif event["event"] == "watch checked to add time.":
            resolved = False
        elif event["event"] == "45 seconds added to match.":
            resolved = True

