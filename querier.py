from TimerFunction import time_a_function
from json import load
from datetime import datetime


def stat_loader(filename):
    a = datetime.now()
    try:
        with open(f"json_stats/{filename}.json", "r") as f:
            print(f"loading {filename} took {datetime.now() - a}.")
            return load(f)
    except:
        print(f"loading {filename} failed.")
        return {}



# def select(from_file, grab_data, on_condition):
#     a = datetime.now()
#     results = []
#     with open(f"json_stats/{from_file}.json", "r") as f:
#         games = load(f)
#     for game in games:
#         for blip in games[game]:
#             if on_condition(blip):
#                 results.append(grab_data(game, blip))
#     print(f"Function took {datetime.now() - a}")
#     return results
#
# games = select(from_file="game_info_bugs",
#                grab_data=lambda game, attempt: (attempt["success"], game),
#                on_condition=lambda attempt: attempt["type"] == "Twitch")
#
# print(len(games))
# for g in games:
#     print("", g)


events = stat_loader("events_matches")
casts = stat_loader("game_info_cast")
shots = stat_loader("game_info_shot")
heads = stat_loader("game_info_header")

# single_roles = ("Spy", "SeductionTarget")
#
# from collections import Counter
# overall_repeats = Counter()
#
# for event in events:
#     for div in events[event]:
#         for match in events[event][div]:
#             # print(match)
#             repeats = []
#             for i, game in enumerate(match["games"]):
#                 print(f"Game {i+1}: {heads[game]['venue']}")
#                 curr_head = heads[game]
#                 curr_cast = casts[game]
#                 spy, st = curr_cast["Spy"], curr_cast["SeductionTarget"]
#                 for j, prev_game in enumerate(match["games"][:i]):
#                     prev_cast = casts[prev_game]
#                     prev_shot = shots[prev_game]["shot"] if prev_game in shots else None
#                     found_spy, found_st = False, False
#                     for role in single_roles:
#                         if spy == prev_cast[role]:
#                             repeats.append(f"{heads[game]['spy']}'s Spy was the {role} from {i - j} games ago")
#                             found_spy = True
#                             break
#                     for role in single_roles:
#                         if st == prev_cast[role]:
#                             repeats.append(f"{heads[game]['spy']}'s ST was the {role} from {i - j} games ago")
#                             found_st = True
#                             break
#                     if not found_spy:
#                         if spy == prev_shot:
#                             repeats.append(f"{heads[game]['spy']}'s Spy was shot in game {i - j} games ago")
#                     if not found_st:
#                         if st == prev_shot:
#                             repeats.append(f"{heads[game]['spy']}'s ST was shot in game {i - j} games ago")
#             print(repeats)
#             overall_repeats.update(repeats)
#
#             # shot = shots[game]['shot'] if game in shots else None
#             # print(f" {game}\t{casts[game]}\t{shot}")
#
#
# for x in overall_repeats:
#     count = overall_repeats[x]
#     if count > 1:
#         print(f"{overall_repeats[x]}x {x}")



