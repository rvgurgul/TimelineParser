import json


with open("json_drafts/s5_drafts.json", "r") as f:
    s5_draft = json.load(f)

new_format = {}
for player_dict in s5_draft:
    player_drafts = player_dict["drafts"]
    new_format[player_dict["name"]] = [{
        "event": f"SCL{draft['season']}",
        "week": draft["week"],  # not int-casted because week is a string-key of event_matches
        "venue": draft["venue"],
        "setup": draft["gametype"],
        "games": -4 if draft["games"] == "0" else int(draft["games"]),
    } for draft in player_drafts]

with open("json_stats/s5_drafts.json", "w") as f:
    json.dump(new_format, f, indent=2)


