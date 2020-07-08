import json
from datetime import datetime
from ParallelParser import query_games

from AbstractParsers import *
from ComprehensiveParsers import *

way_before = datetime.now()

qg = query_games()
# qg = query_games(limit=1500)

functions = {
    "game_info/watch": all_watch_info,
    # "game_info/statues": all_statue_info,  # fixme consider adding confirm_time to inspects
    # "game_info/spy_start": all_spy_start_info,
    "game_info/sniper_marks": info_sniper_marks,    # todo apply the de-doubler to marks
    # "game_info/sniper_lights": info_sniper_lights,
    # "game_info/sips": all_sips_info,
    "game_info/shot": shot_details,
    "game_info/seduce": all_seduce_info,
    # "game_info/psv": all_psv_info,
    "game_info/overtime": all_overtime_info,      # TODO handle hanging GTAs
    "game_info/missions": all_mission_info,
    "game_info/header": all_header_info,
    # "game_info/fingerprints": all_fingerprints,
    "game_info/drinks_tray": all_drink_info_tray,  # todo purloins don't exist
    "game_info/drinks_bar": all_drink_info_bar,
    # "game_info/da_convos": all_da_intersects,  # todo maybe worth embedding in conversations.json
    # "game_info/conversations": all_convo_info,
    # "game_info/contact": all_contact_info,
    "game_info/clock": all_time_info,  # TODO overhaul: "time": float, "spy_clock": float, "sni_clock": float,
        # remove "event" -> it is assumed this file logs time changes
        # also remove OT events, as those do not influence the time
    "game_info/cast": all_cast_info,
    "game_info/bugs": all_bug_info,
    # "game_info/briefcases": all_briefcase_info,
    "game_info/books": all_book_info,  # fixme consider adding confirm_time to microfilm
    # "game_info/audibles": all_audible_info,
    "game_info/action_tests": all_at_info,  # fixme consider adding trigger time?

    # "specific_stats/possible_direct_transfer": probably_a_direct_transfer_shot,  # fixme output seems wrong
    # "specific_stats/progress_to_shot_time": shot_time_related_to_progress,
    # "specific_stats/mission_pacing": progress_per_time,
    # "specific_stats/mission_density": mission_density,

    # "venue_info/library_4_8": lambda g: retro_result(g, venue="Library", og_mode="a5/8", decreased_mission_count=4),
    # "venue_info/moderne_4_8": lambda g: retro_result(g, venue="Moderne", og_mode="a5/8", decreased_mission_count=4),
    # "venue_info/veranda_4_8": lambda g: retro_result(g, venue="Veranda", og_mode="a5/8", decreased_mission_count=4),
    # "venue_info/ballroom_3_8": lambda g: retro_result(g, venue="Ballroom", og_mode="a4/8", decreased_mission_count=3),
}

for fx in functions:
    results = {}
    before = datetime.now()
    print(f"analyzing {fx}...", end="")
    for game in qg:
        res = functions[fx](game)
        if res is not None:
            results[game.uuid] = res
    with open(f"json_outputs/{fx}.json", "w") as file:
        json.dump(results, file, indent=1)
    print(f"done (took {datetime.now() - before})")
print(f"DONE (took {datetime.now() - way_before} overall)")
