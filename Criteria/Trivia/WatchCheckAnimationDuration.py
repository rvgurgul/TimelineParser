from Helpers import get_characters_of_role


def watchCheckAnimation(jason):
    spy = get_characters_of_role(jason, "Spy")
    durs = []
    ts = 0
    for event in jason["timeline"]:
        if event["event"] == "watch checked to add time.":
            ts = event["elapsed_time"]
        elif event["event"] == "45 seconds added to match.":
            diff = round(event["elapsed_time"] - ts, 1)
            durs.append(diff)
    if len(durs) > 0:
        return durs
