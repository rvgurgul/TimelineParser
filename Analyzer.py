from Constants import Triple_Agent as tac
from ListUnpacker import *
from Stats import *

import json
import os

root = "json_gamez/"


def debug(uuid):
    try:
        file = open(root + uuid + ".json", "r")
        lines = "".join([line.strip() for line in file.readlines()])
        file.close()
        jason = json.loads(lines)
        from Classes.Game import Game
        game = Game(jason)
        print(game)
    except FileNotFoundError:
        print("Failed debug of ", uuid, ".json", sep="")


def query_games(constraints=None, limit=tac.PARSED_GAME_COUNT, describe_results=True, display_progress=True):
    data_directory = os.listdir(root)
    accepted, rejected = [], 0
    if display_progress:
        print("Querying games, please wait...")
        print("0%", " " * 21, "25%", " " * 22, "50%", " " * 22, "75%", " " * 21, "100%", sep="")
        prog_bar = 0
    for filename in data_directory:
        try:
            file = open(root + filename, "r")
            lines = "".join([line.strip() for line in file.readlines()])
            file.close()
            jason = json.loads(lines)
            if constraints is None or constraints(jason):
                accepted.append(jason)
                if len(accepted) >= limit:
                    break
            else:
                rejected += 1
            if display_progress:
                delta = (101 * (len(accepted)+rejected) // limit)
                if delta > prog_bar:
                    print(end="|")
                    prog_bar += 1
        except:
            print("Problematic File?\t", filename)
    if display_progress:
        print("|")
    if describe_results:
        total = len(accepted) + rejected
        print("Queried", total, "games:")
        acc_ratio, rej_ratio = round(100 * len(accepted) / total, 1), round(100 * rejected / total, 1)
        print(" Accepted ", len(accepted), " games (", acc_ratio, "%)", sep="")
        if rejected > 0:
            print(" Rejected ", rejected, " games (", rej_ratio, "%)", sep="")
    return accepted


def analyze_games(criterion, games=None, constraints=None, categorization=None):
    if games is None and constraints is None:
        print("Games or constraints must be provided!")
        return
    if constraints is not None:
        if games is None:
            games = query_games(constraints=constraints)
        else:
            print("Did not use provided constraints because games are sufficient.")

    if categorization is None:
        results = []
    else:
        results = {}

    for i, game in enumerate(games):
        try:
            result = criterion(game)
            if result is None:
                continue
            if type(result) is not list:
                result = [result]
        except:
            print(game["uuid"], "caused an error in the criterion function")
            continue

        if categorization is not None:
            try:
                category = categorization(game)
                if type(category) is not list:
                    category = [category]
            except:
                print(game["uuid"], "caused an error in the categorization function")
                continue
            for subcat in category:
                if subcat is None:
                    continue
                elif subcat in results:
                    for item in result:
                        results[subcat].append(item)
                else:
                    results[subcat] = result
        else:
            for item in result:
                results.append(item)

    return results

# Step 1: query_games(
#   limit=int
#   constraints=lambda
#   describe_results=bool
# )
# Step 2: analyze_games(
#   criterion=lambda
#   categorization=lambda
#   games=query_games()
#   display_progress=bool
# )
# Step 2.5: unpack()?
# Step 3: analysis_report()
#   numeric=bool

# moderne_five_eight = query_games(constraints=lambda game: game["venue"] == "Moderne" and game["game_type"] == "a5/8")
# x = analyze_games(criterion=moderne_four_eight, games=moderne_five_eight)
# analysis_report(x)

# from Criteria_old.DrinkOffers import drink_behavior
#
# chex = query_games(constraints=lambda game: game["spy"] == "checker")
# x = analyze_games(criterion=drink_behavior, games=chex)
# occurrence_report(x)
#
# from Criteria_old.DrinkOffers import *
#
# gamz = query_games(limit=50, constraints=lambda game: game["venue"] in bar_venues)
# x = analyze_games(criterion=delegate_description, games=gamz)
# print(x)

# from Criteria_old.BugAttempts import get_bug_attempts
#
# bug_games = query_games()#constraints=lambda game: "Bug" in game["completed_missions"])
# x = analyze_games(games=bug_games, criterion=get_bug_attempts)#, categorization=lambda game: game["venue"])
# analysis_report(x)

# from Criteria_old.Timing.HighlightTension import highlight_tension
# from Constants.Results import shot_win_conditions
#
#
# x = analyze_games(games=query_games(constraints=lambda game: get_specific_win_condition(game) in shot_win_conditions), criterion=highlight_tension,)# categorization=highlight_tension)
# print(x)


# from Constants.Venues import bar_venues
# from Criteria_old.Spy_Missions.Purloin import get_delegate_time
#
# x = analyze_games(constraints=lambda game: game["venue"] in bar_venues and "Purloin" in game["completed_missions"],
#                   categorization=get_delegate_time,
#                   criterion=get_specific_win_condition)
# print(x)


# from Criteria_old.DrinkOffers import inno_drink_takes
#
# sample = query_games()
#
# x = analyze_games(games=sample, criterion=inno_drink_takes)
# y = analyze_games(games=sample, criterion=lambda game: inno_drink_takes(game, exclude_purloin=False))
#
# av1, av2 = round(100*avg(x), 3), round(100*avg(y), 3)
# print("  ", av1, "% drink accepts excl. purloin", sep="")
# print("  ", av2, "% drink accepts incl. purloin", sep="")
# print("  ", round(av2-av1, 3), "% different", sep="")

# from Criteria_old.Spy_Missions.Transfer import describe_microfilm
# from Constants.Venues import bookshelf_venues
#
# test = query_games(constraints=lambda game: game["venue"] in bookshelf_venues)
# x = analyze_games(criterion=lambda game: tuple(describe_microfilm(game, append_shot=True)), games=test, categorization=lambda game: game["venue"])
# analysis_report(x)

# from Criteria_old.AbandonedProgress import absolute_progress
#
# x = analyze_games(criterion=absolute_progress, games=query_games(limit=12))
#
# for y in x:
#     print(y)


# FUNCTIONAL FORMAT: (transition_states, pseudo-variables)
conversation_time = ({
    lambda event: event["event"] == "game started.": [
        ("spy_in_cc", False),
    ],
    lambda event: event["event"] == "spy enters conversation.": [
        ("cc_join_ts", lambda event: event["elapsed_time"]),
        ("spy_in_cc", True),
    ],
    lambda event: event["event"] == "spy leaves conversation.": [
        ("conversation_durations", lambda event: round(event["elapsed_time"] - outputs["cc_join_ts"], 1)),
        ("spy_in_cc", False),
    ],
    lambda event: "GameEnd" in event["category"]: [
        ("conversation_durations", lambda event: round(event["elapsed_time"] - outputs["cc_join_ts"], 1) if outputs["spy_in_cc"] else None),
    ],
}, {  # format: "variable_name": default_value, return_value
    # TODO reimplement return_value bool/lambda
    "conversation_durations": list,
    "spy_in_cc": bool,
    "cc_join_ts": int,
})

# TODO: very promising, still need to define single/limited use states
inputs = {
    lambda event: event["event"] == "spy player takes control from ai.": [
        ("take_control_time", lambda event: event["elapsed_time"])
    ],
    lambda event: event["event"] == "waiter offered drink.": [
        ("first_offer", lambda event: event["cast_name"][0])
    ],
    lambda event: event["event"] == "spy joined conversation with double agent.": [
        ("spy_in_with_da", True)
    ],
    lambda event: event["event"] == "double agent joined conversation with spy.": [
        ("spy_in_with_da", True)
    ],
    lambda event: event["event"] == "spy left conversation with double agent.": [
        ("spy_in_with_da", False)
    ],
    lambda event: event["event"] == "double agent left conversation with spy.": [
        ("spy_in_with_da", False)
    ],
}


outputs = {
    "take_control_time": [],
    "conversation_duration": [],
    "cc_join_ts": 0,
    "spy_in_cc": False,
    "first_offer": [],
    "spy_in_with_da": False,
}


def analyze_twopointoh(games, transition_states, data_dict, categorization=lambda game: None):
    results = {}
    for game in games:
        pseudovars = {x: data_dict[x]() for x in data_dict}
        for event in game["timeline"]:
            for test in transition_states:
                if test(event):
                    for transition in transition_states[test]:
                        key, val = transition
                        if val is None:
                            continue
                        elif callable(val):
                            val = val(event)
                        subdir = pseudovars[key]
                        if type(subdir) is list:
                            subdir.append(val)
                        else:
                            pseudovars[key] = val
        cats = categorization(game)
        if type(cats) is not list:
            cats = [cats]
        for cat in cats:
            if cat not in results:
                results[cat] = [pseudovars]
            else:
                results[cat].append(pseudovars)
    return results


# print(conversation_time[1])
# y = analyze_twopointoh(games=query_games(limit=3),
#                        transition_states=conversation_time[0],
#                        data_dict=conversation_time[1],
#                        categorization=lambda game: game["uuid"])
# print(conversation_time[1])
# print(y)


# want:
#
#   uuid
#       convo_durations
#       contact_inits
#       bug attempts
#       etc.
#
#   venue
#       [convo_durations]
#       [contact_inits]
#
#
#
#
#
#

# player = "Legorve Genine/steam"
# y = analyze_games(criterion=lambda game: (game["start_time"], game["spy"]+" chose "+get_characters_of_role(game, "Spy")+" on "+game["venue"]),
#                   categorization=lambda game: get_match_detail(game),
#                   constraints=lambda game: game["event"] == "SCL5" and (game["spy"] == player or game["sniper"] == player))
# for x in y:
#     print(x)
#     pix = [z[1] for z in sorted(y[x])]
#     for z in pix:
#         print(" ", z)

