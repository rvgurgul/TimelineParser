from EventGroups import *

def shot_time_related_to_progress(game):
    if game.cast.shot is None:
        return  # check against the shot character in case of TLFS
    missions = {}  # will only take the most recent progress for each mission
    for event in game.timeline:
        if event == "took shot.":
            for mission in missions:
                missions[mission] = round(event.time - missions[mission], 1)
            break
        for event_group in (
            mission_completes,
            mission_partials,
            mission_fails,
        ):
            if event in event_group:
                misn = event_group[event]
                if misn in missions:  # by removing the existing entry, the updated value is put at the bottom of
                    del missions[misn]  # the dict, effectively sorting by recency
                missions[misn] = event.time
    return missions

def progress_per_time(game):
    grace_period = 0
    mission_pacing = 0
    flirt_pct = 0
    statu_pct = 0
    print_pct = 0

    light_fluidity = 0
    # duration = game.timeline[-1].time
    for event in game.timeline:
        if event in audible_events:
            grace_period = event.time + 10
        elif event in sniper_lights_down and event.time > grace_period:
            light_fluidity += 1
        # countable soft tell progress is separate
        elif event in flirt_percents:
            flirt_pct = flirt_percents[event]
        elif event in statues_inspected:  # no need for a div. by 0 because you can't inspect on statueless venues
            statu_pct += 1/game.venue.inspects
        elif event in fingerprint_success:
            print_pct += 0.5
        # TODO indirect transfer progress??
        elif event in mission_completes:
            if event in {
                "target seduced.",
                "all statues inspected.",
                "fingerprinted ambassador.",
            }:
                continue
            mission_pacing += 1

    return {
        "absolute_progress": round(mission_pacing + flirt_pct/100 + statu_pct + print_pct, 2),  # /duration,
        "non_alibi_lights": light_fluidity,  # /duration
    }

def probably_a_direct_transfer_shot(game):
    if game.venue.bookshelves == 0:
        return
    if "Transfer" not in game.missions_selected:
        return
    if "Transfer" not in game.missions_complete:
        return
    if "SpyShot" != game.specific_win_condition:
        return
    book_color = "No Book"
    for event in game.timeline[::-1]:
        if event == "get book from bookcase.":
            book_color = event.held_book
            break
        elif event == "put book in bookcase.":
            return  # spy must be holding a book at the end of the game
    return book_color

def retro_result(game, venue, og_mode, decreased_mission_count):
    if game.venue.name != venue or game.mode != og_mode:
        return
    if len(game.missions_complete) < decreased_mission_count:
        return False  # no change to the original result
    if "MissionsWin" == game.specific_win_condition:
        return False  # a mission win would have already been a mission win
    new_countdown = 0
    mc = 0
    for event in game.timeline:
        if 0 < new_countdown:
            if event.time <= new_countdown:
                if event == "took shot.":
                    return "SpyShot" if event.character.role == "Spy" else "CivilianShot"
            else:
                return "MissionsWin"
        elif event in mission_completes:
            mc += 1
            if mc == decreased_mission_count:
                new_countdown = event.time + 10
    return "IDK"  # TODO what causes this?

def inspect_downtime(game):
    statues = []
    statue = []
    puts = 0
    test = None
    for event in game.timeline:
        if event == "picked up statue.":
            puts = event.time
            statue.append({
                "time": 0,
                "type": "Idle"
            })
        elif event == "action triggered: inspect statues":
            statue.append({
                "time": event.time - puts,
                "type": "Action Test"
            })
        elif event in action_test_inspect:
            statue.append({
                "time": event.time - puts,
                "type": f"{test} Inspect"
            })
        elif event in statues_inspected:
            statue.append({
                "time": event.time - puts,
                "type": "Idle"
            })
        elif event in inspect_interrupted:
            statue.append({
                "time": event.time - puts,
                "type": "Idle (Inspect Interrupted)"
            })
        elif event == "put back statue.":
            statues.append(statue)
            statue = []
    # TODO make cool horizontal graphs to describe statue inspects
    return statues

__mission_value = {
    "Bug": 5,
    "Contact": 3,
    "Transfer": 5,
    "Swap": 5,
    "Inspect": 2,
    "Seduce": 3,
    "Purloin": 5,
    "Fingerprint": 3
}

def __product(arr):
    prod = 1
    for x in arr:
        prod *= x
    return prod

# def mission_density(game):  # TODO finish mission_density
#     mct = []
#     for event in game.timeline:
#         if event in mission_completes:
#             mct.append((mission_completes[event], event.time))
#     perms = 1
#     mc = len(mct)
#     densities = []
#     for i in range(mc):
#         for j in range(i + 1, mc):
#             print(perms, mct[i:j + 1])
#             mv = __product([__mission_value[msn[0]] for msn in mct[i:j + 1]])
#             print(f"mission value: {mv}")
#             density = mv/(mct[j][1] - mct[i][1] + 0.1)  # prevents division by 0 in case of two simultaneous missions
#             print(density)
#             densities.append((density, mct[i:j + 1]))
#             perms += 1
#     return densities
#
# from ParallelParser import query_games
# qg = query_games(limit=500)
#
# for game in qg:
#     y = mission_density(game)
#     print(y)
