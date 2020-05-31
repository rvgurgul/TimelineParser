
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


def overtime(game):
    for event in game.timeline.events:
        pass
        #



__starter_destinations = {
    "get book from bookcase.": "Book",
    "put book in bookcase.": "Book",
    "picked up statue.": "Statue",
    "put back statue.": "Statue",
    "request drink from bartender.": "Bar",
    "request cupcake from bartender.": "Bar",
    "action triggered: check watch": "Window",
    "spy enters conversation.": "Conversation",
    "spy leaves conversation.": "Conversation",
    "spy picks up briefcase.": "Briefcase",
    "spy puts down briefcase.": "Briefcase",
}
__starter_actions = {
    "action triggered: inspect statues": "Inspect",
    "action triggered: transfer microfilm": "Microfilm",
    "action triggered: fingerprint ambassador": "Fingerprint",
    "action triggered: contact double agent": "Contact",
    "action triggered: seduce target": "Seduce",
    "begin planting bug while standing.": "Standing Bug",
    "begin planting bug while walking.": "Walking Bug",
    "watch checked.": "Watch Check",
    "watch checked to add time.": "Time Add",
    "statue swap pending.": "Green Swap",
    "statue swapped.": "Swap",
    "delegating purloin guest list.": "Delegate",
    "guest list purloin pending.": "Green Purloin",
    "guest list purloined.": "Purloin",
}


def initial_destination(game):
    dest, act = None, None
    for event in game.timeline:
        if dest is None and event in __starter_destinations:
            dest = __starter_destinations[event]
        elif act is None:
            if event == "put book in bookcase." and event.bookshelf != event.held_book:
                act = "Direct Transfer"
            elif event in __starter_actions:
                act = __starter_actions[event]
            if dest is not None:
                break
    if dest is None:
        dest = "Unknown"
    if act is None:
        act = "Idling"
    return dest, act
