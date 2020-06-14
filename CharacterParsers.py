from Constants.EventGroups import action_test_timeadd


def watch_check_durations(game):
    wcs = []
    wcts = 0
    for event in game.timeline:
        if event == "watch checked to add time.":
            wcts = event.time
        elif event == "45 seconds added to match.":
            wcs.append(round(event.time - wcts, 1))
    return wcs

def waning_time_add_fail(game):
    if game.specific_win_condition != "TimeOut":
        return
    for event in game.timeline[::-1]:
        # if event == "watch checked to add time.":
        #     return True
        if event == "action triggered: check watch":
            return "Triggered"
        elif event == "45 seconds added to match.":
            return
        elif event == "aborted watch check to add time.":
            return "Canceled"
        elif event in action_test_timeadd:
            return action_test_timeadd[event]

def statue_hold_times(game):
    shs = []
    spts = 0
    # assumptions:
    #  players follow good (enough) statue etiquette
    #  a 2- or 3-cycle statue visit is the sum of two shorter animations
    #  clanks and game ends are irrespective of animation and therefore ignored
    for event in game.timeline:
        if event == "picked up statue.":
            spts = event.time
        elif event == "put back statue.":
            shs.append(round(event.time - spts, 1))
    return shs

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
                break
            elif "failed planting bug while walking." in event:
                results.append((game.cast.spy.name, False, round(event.time - plant_ts, 1)))
            plant_ts = 0
    return results



