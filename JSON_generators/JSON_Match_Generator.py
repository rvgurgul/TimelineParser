import json
from ParallelParser import query_games

qg = query_games()

events = {}

for game in qg:
    mtch = game.match
    player_tuple = (mtch.playerA, mtch.playerB)
    if mtch.event not in events:
        events[mtch.event] = {mtch.division: [{
            "players": player_tuple,
            "week": mtch.week,
            "games": [game],
            "draft": None,
        }]}
        # print(f"created event {mtch.event} with division {mtch.division}")
    else:
        if mtch.division not in events[mtch.event]:
            events[mtch.event][mtch.division] = [{
                "players": player_tuple,
                "week": mtch.week,
                "games": [game],
                "draft": None,
            }]
            # print(f"created division {mtch.division} in {mtch.event}")
        else:
            found_existing = False
            for match in events[mtch.event][mtch.division]:
                if player_tuple == match["players"]:
                    match["games"].append(game)
                    # print(f"added game to existing match {player_tuple}")
                    found_existing = True
                    break
            if found_existing:
                continue  # double break
            events[mtch.event][mtch.division].append({
                "players": player_tuple,
                "week": mtch.week,
                "games": [game],
                "draft": None,
            })
            # print(f"added game to new match {player_tuple}")

for event in events:
    for div in events[event]:
        for match in events[event][div]:  # sort games by date then select the UUID
            match["games"] = [game.uuid for game in sorted(match["games"], key=lambda g: g.date, reverse=True)]

with open(f"json_outputs/events_matches.json", "w") as file:
    json.dump(events, file, indent=3)

