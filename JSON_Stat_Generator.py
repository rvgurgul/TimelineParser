import json
from ParallelParser import query_games

from ComprehensiveParsers import *
# from CriteriaParsers.Books import *
# from CriteriaParsers.Bug import *
# from CriteriaParsers.Characters import *
# from CriteriaParsers.Contact import *
# from CriteriaParsers.Conversations import *
# from CriteriaParsers.Drinks import *
# from CriteriaParsers.Random import *
# from CriteriaParsers.Seduce import *
# from CriteriaParsers.Statues import *
# from CriteriaParsers.Sniper import *
# from CriteriaParsers.Time import *

# qg = query_games()[None]
qg = query_games(limit=2500)[None]

functions = {
    # "game_info_bug": all_bug_info,
    "game_info_contact": all_contact_info,  # fixme trigger_time is borked and is sometimes replaced by wait_time
    "game_info_seduce": all_seduce_info,
    # "game_info_fingerprint": all_fingerprints,
    # "game_info_books": all_book_info,
    # "game_info_statues": all_statue_info,
    # "game_info_cast": all_cast_info,
    "game_info_time": all_time_info,
    # "game_info_shot": shot_details,
    # "game_info_watch": all_watch_info,
    # "game_info_header": all_header_info,
    # "game_info_drinks_tray": all_drink_info_tray,  # fixme some offer times are borked.. probably natural toby offers
    "game_info_drinks_bar": all_drink_info_bar,
    "game_info_spy_start": all_spy_start_info,
    "game_info_audibles": all_audible_info,
    "game_info_sips": all_sips_info,



    # "conversation_durations": conversation_durations,
    # "number_of_talks": number_of_talks,
    # "rushed_stoptalks_sens_2": rushed_stop_talk,
    # "full_inspect_duration": time_to_inspect,
    # "lowlight_quickdraw": lowlight_speedrun,

}

for fx in functions:
    results = {}
    print(f"analyzing {fx}")
    for game in qg:
        res = functions[fx](game)
        if res is not None:
            results[game.uuid] = res
    with open(f"json_stats/{fx}.json", "w") as file:
        json.dump(results, file, indent=1)


# conversations:
#  - duration
#  - actions
#  -
