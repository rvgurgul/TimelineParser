
from Helpers import get_number_missions_needed


# TODO translate to parser
def spy_inspect_swaps(jason):
    mc, mn = 0, get_number_missions_needed(jason)
    inspected, swapped = False, False
    for event in jason["timeline"]:
        if "MissionComplete" in event["category"]:
            mc += 1
            if event["mission"] == "Inspect":
                if mc <= mn - 2:
                    return False
                inspected = True
            elif event["mission"] == "Swap":
                if mc <= mn - 2:
                    return False
                swapped = True
            if mc == mn:
                return inspected and swapped

        # if event["event"] == "put back statue.":
        #     if inspected and swapped:
        #         return True
        #     if inspected or swapped:
        #         return False
        # elif event["event"] == "all statues inspected.":
        #     if swapped:
        #         return True
        #     inspected = True
        # elif event["event"] == "statue swapped." or event["event"] == "statue swap pending.":
        #     if inspected:
        #         return True
        #     swapped = True
    return inspected and swapped
