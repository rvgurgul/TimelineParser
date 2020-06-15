

def paws(game, require_inspects=True):
    if not game.reaches_mwc or "Swap" not in game.missions_complete:
        return
    inspected = False
    swap_ts = 0
    # returns the time on the clock when the spy triggers the swap as a finishing mission
    for event in game.timeline[::-1]:
        if event == "all statues inspected.":
            inspected = True
        elif event.action_test != "NoAT" and event.mission == "Swap":
            swap_ts = event.clock
        elif event == "picked up statue.":
            return swap_ts if swap_ts and (inspected or not require_inspects) else None



def time_to_inspect(game, all_in_one=True):
    first_inspect = None
    inspect_ats = []
    for event in game.timeline:
        if first_inspect is None and event == "action triggered: inspect statues":
            first_inspect = event.time
        elif all_in_one and event == "put back statue.":
            return
        elif event == "all statues inspected.":
            return {
                "time": round(event.time - first_inspect, 1),
                # "venue": game.venue.name,
                # "spy": game.spy,
                # "needed": game.venue.inspects,
                "tests": inspect_ats
            }
        elif event.mission == "Inspect" and event.action_test is not None:
            inspect_ats.append(event.action_test)


def inspect_deadtime(game):
    deadtime = 0
    last_ts = 0
    for event in game.timeline:
        if event == "picked up statue.":
            last_ts = event.time
        elif event == "action triggered: inspect statues":
            deadtime += event.time - last_ts
        # elif event == "a"
        # TODO sum times between statue action tests
