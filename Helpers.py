from Constants.Results import *
from Constants.Events import *


def get_specific_win_condition(jason):
    for con in specific_win_conditions:
        if con in jason["win_type"]:
            return con


def get_general_win_condition(jason):
    for con in general_win_conditions:
        if con in jason["win_type"]:
            return con


def get_number_missions_needed(jason):
    return int(jason["game_type"][1])


def get_characters_of_role(jason, roles):
    if type(roles) is str:
        roles = [roles]
    cast = []
    for event in jason["timeline"]:
        if "Cast" in event["category"] and event["role"][0] in roles:
            cast.append(event["cast_name"][0])
        elif "MissionSelected" in event["category"]:
            break
    return cast[0] if len(cast) == 1 else cast


def get_role_of_character(jason, character):
    for event in jason["timeline"]:
        if "Cast" in event["category"] and event["cast_name"] == character:
            return event["role"][0]
        elif event["event"] == "game started.":
            break
    return "Absent"


def get_character_shot(jason):
    if "MissionsWin" in jason["win_type"] or "TimeOut" in jason["win_type"]:
        return "No Shot"
    for event in jason["timeline"][::-1]:
        if event['category'] == ['SniperShot']:
            return event['cast_name']


def get_players_alphabetically(jason):
    return tuple(sorted([jason["spy"], jason["sniper"]]))


def get_match_detail(jason):
    pvp = get_players_alphabetically(jason)
    return get_division_detail(jason) + ": " + pvp[0] + " vs " + pvp[1]


def get_division_detail(jason):
    if jason["division"] is None:
        return jason["event"]
    if len(jason["division"]) == 1:
        return jason["event"] + " Group " + jason["division"]
    return jason["event"] + " " + jason["division"]


def get_most_recent_light_for_character(jason, character, timestamp=0):
    if timestamp <= 0:
        timestamp = jason["timeline"][-1]["elapsed_time"]
    for event in jason["timeline"][::-1]:
        if event["elapsed_time"] <= timestamp and event["category"] == ["SniperLights"]:
            if character in event["cast_name"]:
                return lights[event["event"]]
    return "Neutral Light"

# TODO build light-functions into game class, then deprecate Helpers

def get_most_recent_light_for_role(jason, role, timestamp=0):
    if timestamp <= 0:
        timestamp = jason["timeline"][-1]["elapsed_time"]
    for event in jason["timeline"][::-1]:
        if event["elapsed_time"] <= timestamp and event["category"] == ["SniperLights"]:
            if role in event["role"]:
                return lights[event["event"]]
    return "Neutral Light"


def event_sequence(jason, seq, first=True):
    deltas = []
    timestamp = 0
    stage = 0
    for event in jason["timeline"]:
        if event["event"] in seq[stage]:
            if stage == 0:
                timestamp = event["elapsed_time"]
            stage += 1
            if stage == len(seq):
                difference = round(event["elapsed_time"] - timestamp, 1)
                if first:
                    return difference
                deltas.append(difference)
                timestamp = 0
            stage %= len(seq)
    if len(deltas) > 0:
        return deltas


def event_look_ahead(jason, index, time_limit=10):
    events = []
    timestamp = jason["timeline"][index]["elapsed_time"] + time_limit
    for event in jason["timeline"][index + 1::]:
        if event["elapsed_time"] < timestamp:
            events.append(event)
        else:
            return events


def event_look_behind(jason, index, time_limit=10):
    events = []
    timestamp = jason["timeline"][index]["elapsed_time"] - time_limit
    for event in jason["timeline"][index-1:0:-1]:
        if event["elapsed_time"] > timestamp:
            events.append(event)
        else:
            return events


def get_first_mission_completed(jason):
    for event in jason["timeline"]:
        if "MissionComplete" in event["category"]:
            return event["mission"]


def get_last_mission_completed(jason):
    for event in jason["timeline"][::-1]:
        if "MissionComplete" in event["category"]:
            return event["mission"]


def get_mission_completion_order(jason):
    completed = []
    needed = get_number_missions_needed(jason)
    for event in jason["timeline"]:
        if "MissionComplete" in event["category"]:
            completed.append(event["mission"])
            if len(completed) >= needed:
                return completed
    return completed
