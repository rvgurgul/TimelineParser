
def clock_usage(game):
    # if timeout, return start + timeadds
    # if misswin, return time elapsed of "missions successfull..."
    # if spyshot, return time until "took shot"
    # if civshot, "
    if game.specific_win_condition == "TimeOut":
        return game.clock + game.time_added
    elif game.specific_win_condition == "MissionsWin":
        for event in game.timeline.events[::-1]:
            if event == "missions completed successfully.":
                return event.time
    else:
        for event in game.timeline.events[::-1]:
            if event == "took shot.":
                return event.time
    return None


def time_add_usage(game):
    if game.time_added == 0:
        return None
    if game.specific_win_condition == "TimeOut":
        return game.time_added
    elif game.specific_win_condition == "MissionsWin":
        for event in game.timeline.events[::-1]:
            if event == "missions completed successfully.":
                return round(event.time - game.clock, 1)
    else:
        for event in game.timeline.events[::-1]:
            if event == "took shot.":
                return round(event.time - game.clock, 1)
    # todo alternative strategy which uses timeadd time immediately, rather than at the end


