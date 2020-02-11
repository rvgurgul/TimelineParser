from Constants.Events import lights
from Helpers import get_character_shot


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
