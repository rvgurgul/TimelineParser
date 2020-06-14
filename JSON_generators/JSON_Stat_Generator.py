import json
from ParallelParser import query_games

from AbstractParsers import *
from ComprehensiveParsers import *

# qg = query_games()[None]
qg = query_games(limit=1250)[None]

functions = {
    "game_info/watch": all_watch_info,
    "game_info/statues": all_statue_info,
    "game_info/spy_start": all_spy_start_info,
    "game_info/sips": all_sips_info,
    "game_info/sniper_marks": info_sniper_marks,
    "game_info/sniper_lights": info_sniper_lights,
    "game_info/shot": shot_details,
    "game_info/seduce": all_seduce_info,
    "game_info/psv": all_psv_info,
    "game_info/overtime": all_overtime_info,
    "game_info/header": all_header_info,
    "game_info/fingerprints": all_fingerprints,
    "game_info/drinks_tray": all_drink_info_tray,  # fixme some offer times are borked.. probably natural toby offers
    "game_info/drinks_bar": all_drink_info_bar,
    "game_info/conversations": all_convo_info,
    "game_info/contact": all_contact_info,
    "game_info/clock": all_time_info,
    "game_info/cast": all_cast_info,
    "game_info/bugs": all_bug_info,
    "game_info/briefcases": all_briefcase_info,
    "game_info/books": all_book_info,
    "game_info/audibles": all_audible_info,
    "game_info/action_tests": all_at_info,


    "specific_stats/probable_direct_transfer": probably_a_direct_transfer_shot,
    "specific_stats/progress_to_shot_time": shot_time_related_to_progress,
    "specific_stats/mission_pacing": progress_per_time,

    "venue_info/library_4_8": lambda g: retro_result(g, venue="Library", og_mode="a5/8", decreased_mission_count=4),
    "venue_info/moderne_4_8": lambda g: retro_result(g, venue="Moderne", og_mode="a5/8", decreased_mission_count=4),
    "venue_info/veranda_4_8": lambda g: retro_result(g, venue="Veranda", og_mode="a5/8", decreased_mission_count=4),
    "venue_info/ballroom_3_8": lambda g: retro_result(g, venue="Ballroom", og_mode="a4/8", decreased_mission_count=3),
}

for fx in functions:
    results = {}
    print(f"analyzing {fx}")
    for game in qg:
        res = functions[fx](game)
        if res is not None:
            results[game.uuid] = res
    with open(f"json_outputs/{fx}.json", "w") as file:
        json.dump(results, file, indent=1)

