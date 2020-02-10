from Helpers import get_specific_win_condition
from Constants_old import shot_win_conditions

def plagueDoctor(jason):
    if get_specific_win_condition(jason["win_type"]) not in shot_win_conditions:
        return
    coughed = 0
    for event in jason["timeline"]:
        if event["event"]=="banana bread aborted." or event["event"]=="action test red: contact double agent":
            coughed = event["elapsed_time"]
        elif event["elapsed_time"]-coughed<10 and "SniperShot" in event["category"]:
            return event["role"][0], event["cast_name"][0]
