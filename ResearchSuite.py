from collections import Counter
from Stats import statistic_report, average_report
from ListUnpacker import occurrence_report

from Reports import *
from JSON_Handler import *


def prompt_user():
    player = input("Who would you like to research?\n")
    res = player_lookup(player)
    while res is None:
        player = input(f"No replays for '{player}' are available.\nWho would you like to research?\n")
        res = player_lookup(player)
    research_player(res)


def count_from_single(stat_dict, games, extract_funx):
    if type(extract_funx) is dict:
        counts = {fx: Counter() for fx in extract_funx}
        for game in games:
            try:
                game_data = stat_dict[game]
                for fx in extract_funx:
                    func = extract_funx[fx]
                    res = func(game_data)
                    if hasattr(res, '__iter__'):
                        counts[fx].update(func(game_data))
                    else:
                        counts[fx][res] += 1
            except KeyError:
                pass
        return counts
    counts = Counter()
    for game in games:
        try:
            game_data = stat_dict[game]
            res = extract_funx(game_data)
            if hasattr(res, '__iter__'):
                counts.update(res)
            else:
                counts[res] += 1
        except KeyError:
            pass
    return counts

def research_player(username):
    spy_games = []
    sni_games = []
    loader = StatLoader()

    game_headers = loader.get_stat("game_info/header")
    for game in game_headers:
        vals = game_headers[game]
        if vals["spy_username"] == username:
            spy_games.append(game)
        elif vals["sniper_username"] == username:
            sni_games.append(game)

    print(f"   Spy games found: {len(spy_games)}")
    print(f"Sniper games found: {len(sni_games)}")

    # TODO what ratio of lowlights (on non-cast) occurs within 10 seconds of BB or 20 seconds of pl/swap

    # TODO shot timing in relation to overtimer (under 10 second left, wait for OT or no?)

    # TODO probability each character is shot given they are in attendance

    # TODO how does a shot coincide with mission progress/completion, eg:
    #  Bug: 100.0  # missed the bug
    #  Purloin: -0.5  # shot during the purloin fade

    # TODO tic-tac-toe event!
    #  players share a 3x3 board of spy objectives
    #  if a spy completes an objective and wins that game, they earn that square
    #  first to win the game of tic-tac-toe wins the set

    cast_info = loader.get_stat("game_info/cast")
    roles = count_from_single(
        stat_dict=cast_info, games=spy_games,
        extract_funx={
            "Spy": lambda cast: cast["Spy"],
            "ST": lambda cast: cast["SeductionTarget"],
            "Amba": lambda cast: cast["Ambassador"],
            "DA": lambda cast: cast["DoubleAgent"],
            "SDA": lambda cast: cast["SuspectedDoubleAgent"],
            "Civs": lambda cast: cast["Civilian"],
        }
    )
    for role in roles:
        bar_chart(roles[role], sort_by="vals", title=f"{role} Choices")

    shot_info = loader.get_stat("json_outputs/game_info/shot.json")
    time_info = loader.get_stat("json_outputs/game_info/clock.json")


    # shots = count_from_single(
    #     stat_dict=shot_info, games=spy_games,
    #     extract_funx={
    #         "Who": lambda shot: shot["shot"],
    #         "Latency": lambda shot: shot["latency"]
    #     }
    # )
    # for datapt in shots:
    #     bar_chart(shots[datapt])

    bug_info = loader.get_stat("json_outputs/game_info/bugs.json")
    bugs = count_from_single(
        stat_dict=bug_info, games=spy_games,
        extract_funx=lambda bug_attempts: ["%s (%s)" % (
            bug["type"], "Hit" if bug["success"] else "Miss"
        ) for bug in bug_attempts]
    )
    bar_chart(bugs, sort_by='vals', title='Bug Types')

    # prints = stat_loader("json_stats/game_info_fingerprints.json")
    # bbs = stat_loader("json_stats/game_info_contact.json")

    def __print_at_converter(at):
        if at is None:
            return "Easy"
        elif at == "Green":
            return "Difficult Success"
        else:
            return "Difficult Failure"

    # bar_chart(fingerprintables, title="Fingerprint Attempts", y_lab="Occurrences", x_lab="Type")

    # sniper_functions = (
    #     NamedFunction("BB LLs", contact_lowlights, occurrence_report),
    #     NamedFunction("Cast LL Time", lowlight_quickdraw, statistic_report),
    #     NamedFunction("Latency", shot_latency, statistic_report),
    #
    # )
    # spy_functions = (
    #     NamedFunction("Spy Selection", lambda game: game.cast.spy.name, occurrence_report),
    #     # TODO ugh, ST can be none if flirt is off...
    #     NamedFunction("ST Choice", (lambda game: game.cast.seduction_target.name
    #         if game.cast.seduction_target is not None else None), occurrence_report),
    #     NamedFunction("Amba Choice", lambda game: game.cast.ambassador.name, occurrence_report),
    #     NamedFunction("DA Choice", lambda game: game.cast.double_agent.name, occurrence_report),
    #     # NamedFunction("Flirt Pairs", flirt_pair, occurrence_report),
    #     NamedFunction("Flirt Waits", flirt_waits, statistic_report),
    #     NamedFunction("Flirt CDs", flirt_cooldowns, statistic_report),
    #     NamedFunction("Flirt DTs", flirt_downtime, statistic_report),
    #     NamedFunction("BB Waits", contact_waits, statistic_report),
    #     NamedFunction("BB LLs", contact_lowlights, occurrence_report),  # also a good spy stat!
    #     NamedFunction("BB Split Times", split_times, statistic_report),
    #     NamedFunction("Bug Attempts", describe_bug_attempts, occurrence_report),
    #     NamedFunction("PSVs", personal_space_violation_descriptors, occurrence_report),
    #     NamedFunction("Contact Attempts", contact_initiations, occurrence_report),
    #     NamedFunction("Statues", describe_statues, occurrence_report),
    #     NamedFunction("Books", describe_books, occurrence_report),
    #     NamedFunction("Drinks", describe_purloin, occurrence_report),
    #     NamedFunction("Fingerprints", fingerprints, occurrence_report),
    #     NamedFunction("Sip Rate", sip_vs_gulp, average_report),
    #     NamedFunction("Sips per Drink", sips_per_drink, statistic_report),
    #     NamedFunction("Bar Sips", sip_at_bar, average_report),
    #     NamedFunction("Drink Durations", drink_durations, statistic_report),
    #     NamedFunction("Toby Response Time", offer_response_time, statistic_report),
    #     NamedFunction("Delegate vs Direct", delegate_vs_direct, average_report),
    #     NamedFunction("Drink Accept Rate", accept_vs_reject, average_report),
    # )
    #
    # sniper_results = {}
    # spy_results = {}
    #
    # print(f"\nSniper Stats: (n={len(sniper_games)})")
    # for func in sniper_functions:
    #     sniper_results[func.description] = func.parse_games(sniper_games)
    #     print()
    #
    # print(f"\nSpy Stats: (n={len(spy_games)})")
    # for func in spy_functions:
    #     spy_results[func.description] = func.parse_games(spy_games)
    #     print()

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


# prompt_user()



# eventually, show the researched player's deviation from mean (of all samples or of only current division)
