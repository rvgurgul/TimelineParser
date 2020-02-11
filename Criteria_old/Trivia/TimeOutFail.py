from Helpers import get_characters_of_role


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

