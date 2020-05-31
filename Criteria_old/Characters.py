

def watch_check_animation_duration(game):
    durs = []
    check_ts = 0
    for event in game.timeline:
        if event == "watch checked to add time.":
            check_ts = event.time
        elif event == "45 seconds added to match.":
            diff = round(event.time - check_ts, 1)
            durs.append(diff)
    return durs


def waning_time_add_fails(game):
    if game.specific_win_condition != "TimeOut":
        return

    resolved = True
    for event in game.timeline.events[-10::]:
        if event == "watch checked to add time.":
            resolved = False
        elif event in {"45 seconds added to match.", "aborted watch check to add time."}:
            resolved = True
    return not resolved


def bug_animation_times(game):
    # returns (True, time) for a connected bug
    # appends (False, time) for a failed bug
    results = []
    plant_ts = 0
    for event in game.timeline:
        if "begin planting bug while walking." in event:
            plant_ts = event.time
        elif plant_ts > 0:
            if "bugged ambassador while walking." in event:
                results.append((game.cast.spy.name, True, round(event.time - plant_ts, 1)))
            elif "failed planting bug while walking." in event:
                results.append((game.cast.spy.name, False, round(event.time - plant_ts, 1)))
            plant_ts = 0
    return results


def statue_animation_times(game):
    # assumptions:
    #  players follow good (enough) statue etiquette
    #  a 2- or 3-cycle statue visit is the sum of two shorter animations
    #  clanks and game ends are irrespective of animation and therefore ignored
    results = []
    pickup_ts = 0
    for event in game.timeline:
        if event == "picked up statue.":
            pickup_ts = event.time
        elif event == "put back statue.":
            results.append(round(event.time - pickup_ts, 1))
    return results




