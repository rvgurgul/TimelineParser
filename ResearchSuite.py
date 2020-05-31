from Constants.Triple_Agent import player_list_scl_5
from ParallelParser import parse_games, query_games, NamedFunction
from Stats import statistic_report, average_report
from ListUnpacker import occurrence_report

from CriteriaParsers.Books import *
from CriteriaParsers.Bug import *
from CriteriaParsers.Characters import *
from CriteriaParsers.Contact import *
from CriteriaParsers.Conversations import *
from CriteriaParsers.Drinks import *
from CriteriaParsers.Seduce import *
from CriteriaParsers.Statues import *
from CriteriaParsers.Sniper import *
from CriteriaParsers.Time import *
from CriteriaParsers.Fingerprint import *


def prompt_user():
    player = input("Who would you like to research?\n")
    while player not in player_list_scl_5:
        if f"{player}/steam" in player_list_scl_5:  # optional /steam
            # TODO case insensitive
            player = f"{player}/steam"
            break
        confirm = input(f"Replays for '{player}' may not be available, continue?")
        if confirm[0] == 'y':
            break
        else:
            player = input("Who would you like to research?\n")
    research_player(player)


def research_player(name):
    qg = query_games(constraints=lambda jason: jason["spy"] == name or jason["sniper"] == name,
                     categorization_function=lambda game: "Sniper" if game.sniper == name else "Spy")

    sniper_games = qg["Sniper"]
    spy_games = qg["Spy"]

    sniper_functions = (
        NamedFunction("BB LLs", contact_lowlights, occurrence_report),
        NamedFunction("Cast LL Time", lowlight_quickdraw, statistic_report),
        NamedFunction("Latency", shot_latency, statistic_report),

    )
    spy_functions = (
        NamedFunction("Spy Selection", lambda game: game.cast.spy.name, occurrence_report),
        # TODO ugh, ST can be none if flirt is off...
        NamedFunction("ST Choice", (lambda game: game.cast.seduction_target.name
            if game.cast.seduction_target is not None else None), occurrence_report),
        NamedFunction("Amba Choice", lambda game: game.cast.ambassador.name, occurrence_report),
        NamedFunction("DA Choice", lambda game: game.cast.double_agent.name, occurrence_report),
        # NamedFunction("Flirt Pairs", flirt_pair, occurrence_report),
        NamedFunction("Flirt Waits", flirt_waits, statistic_report),
        NamedFunction("Flirt CDs", flirt_cooldowns, statistic_report),
        NamedFunction("Flirt DTs", flirt_downtime, statistic_report),
        NamedFunction("BB Waits", contact_waits, statistic_report),
        NamedFunction("BB LLs", contact_lowlights, occurrence_report),  # also a good spy stat!
        NamedFunction("BB Split Times", split_times, statistic_report),
        NamedFunction("Bug Attempts", describe_bug_attempts, occurrence_report),
        NamedFunction("PSVs", personal_space_violation_descriptors, occurrence_report),
        NamedFunction("Contact Attempts", contact_initiations, occurrence_report),
        NamedFunction("Statues", describe_statues, occurrence_report),
        NamedFunction("Books", describe_books, occurrence_report),
        NamedFunction("Drinks", describe_purloin, occurrence_report),
        NamedFunction("Fingerprints", fingerprints, occurrence_report),
        NamedFunction("Sip Rate", sip_vs_gulp, average_report),
        NamedFunction("Sips per Drink", sips_per_drink, statistic_report),
        NamedFunction("Bar Sips", sip_at_bar, average_report),
        NamedFunction("Drink Durations", drink_durations, statistic_report),
        NamedFunction("Toby Response Time", offer_response_time, statistic_report),
        NamedFunction("Delegate vs Direct", delegate_vs_direct, average_report),
        NamedFunction("Drink Accept Rate", accept_vs_reject, average_report),
    )

    sniper_results = {}
    spy_results = {}

    print(f"\nSniper Stats: (n={len(sniper_games)})")
    for func in sniper_functions:
        sniper_results[func.description] = func.parse_games(sniper_games)
        print()

    print(f"\nSpy Stats: (n={len(spy_games)})")
    for func in spy_functions:
        spy_results[func.description] = func.parse_games(spy_games)
        print()

    # TODO change result reporting to be passable here
    # dump_results_to_dossier(name, {})

    # for stat in sniper_results:
    #     print("", stat)
    #     print(" ", sniper_results[stat])
    #
    # for stat in spy_results:
    #     print("", stat)
    #     print(" ", spy_results[stat])

    # SPY:
    # conversation
    #  seduce wait
    #  contact wait
    #  innocent talks?
    #  contact init.
    # progress delay
    # book cook
    # no-control time
    # timer flirt frequency
    # time add ratio
    # inspect behavior
    # common fingerprints
    # drink behavior

    # SNIPER:
    #


# y = parse_games([], fl)
# for x in y:
#     print(x)
#     print(y[x])
#
# from Stats import statistic_dump, average
# from ListUnpacker import occurrence_report
#
# # statistic_dump(y["Latency"])
# # statistic_dump(y["Convo Time after BB"])
# # statistic_dump(y["PSVs"])
#
# # occurrence_report(y["PSVs"])
# occurrence_report(y["Bugs"])
# # statistic_dump(y["Cooldowns"])
#
# # print(average(y["Bar Sips"]))
# print(y["Statue Anims"])
# statistic_dump(y["Statue Anims"])
def dump_results_to_dossier(player, results_dict):
    if player[-6:] == "/steam":
        player = player[:-6]

    # overwrites the file if it exists to include new data
    with open(f"Dossiers/{player}.txt", "w") as outfile:
        outfile.write(f"Dossier: {player}\n\n")
        for result in results_dict:
            outfile.write(result)


prompt_user()
