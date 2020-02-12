from Constants.Events import lights
from Classes.Parser import Parser


class HighlightTension(Parser):

    def __init__(self, game):
        Parser.__init__(self, "Highlight Tension")
        if game.specific_win_condition == "TimeOut" or game.specific_win_condition == "MissionsWin":
            self.complete = True
        else:
            self.chara = game.character_shot
            self.light = lights[game.get_most_recent_light_for(name=self.chara.name)]
            self.light_timestamp = 0

    def parse(self, event):
        if self.complete:
            return

        if "SniperLights" in event.categories and event.characters[0] == self.chara:
            self.light_timestamp = event.time
        elif event == "took shot.":
            self.results = (self.light, self.chara.role, round(event.time-self.light_timestamp, 1))



def highlight_tension(jason):
    if "TimeOut" in jason["win_type"] or "MissionsWin" in jason["win_type"]:
        return
    bullet = 1,
    shotTime = 0
    for event in jason["timeline"][::-1]:
        if "SniperShot" in event["category"]:
            bullet = event["cast_name"], event["role"][0]
            shotTime = event["elapsed_time"]
        elif event["category"] == ["SniperLights"] and event["cast_name"] == bullet[0]:
            return round(shotTime-event["elapsed_time"], 1), lights[event["event"]], bullet[1]
    return shotTime, "Default Light",  bullet[1]
