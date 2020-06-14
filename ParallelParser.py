from Classes.Game import Game
from collections import Counter
from datetime import datetime

import json
import os

root = "json_gamez/"


def debug(uuid):
    try:
        file = open(f"{root}{uuid}.json", "r")
        lines = "".join([line.strip() for line in file.readlines()])
        file.close()
        jason = json.loads(lines)
        from Classes.Game import Game
        game = Game(jason)
        print(game)
    except FileNotFoundError:
        print(f"Failed debug of {uuid}.json", sep="")

def query_games(constraints=None, categorization_function=None) -> [Game]:
    data_dir = os.listdir(root)
    before = datetime.now()
    # TODO hard to do limit/progress bar/query stats with advanced iterable functions :(
    print("Querying games, please wait...", end="")
    games = list(map(Game, filter(constraints, [
        json.load(open(f"{root}{filename}", "r")) for filename in data_dir
    ])))  # easily the most complicated line of code I've written
    print(f"done (took {datetime.now() - before})")
    if categorization_function is None:
        return games
    categories = {}
    for g in games:
        cat = categorization_function(g)
        if cat in categories:
            categories[cat].append(g)
        else:
            categories[cat] = [g]
    return categories

def old_query_games(constraints=None,
                limit=13477,
                describe_results=True,
                display_progress=True,
                categorization_function=lambda game: None):
    data_directory = os.listdir(root)
    categories = {}
    accepted, rejected = 0, 0
    if display_progress:
        print("Querying games, please wait...")
        print(f"0%{'.' * 21}25%{'.' * 22}50%{'.' * 22}75%{'.' * 21}100%")
        prog_bar = 0
    for filename in data_directory:
        try:
            file = open(root + filename, "r")
            lines = "".join([line.strip() for line in file.readlines()])
            file.close()
            jason = json.loads(lines)
            if constraints is None or constraints(jason):
                game = Game(jason)
                category = categorization_function(game)
                if category in categories:
                    categories[category].append(game)
                else:
                    categories[category] = [game]
                accepted += 1
                if accepted >= limit:
                    break
            else:
                rejected += 1
            if display_progress:
                delta = (101 * (accepted+rejected) // limit)
                if delta > prog_bar:
                    print(end="|")
                    prog_bar += 1
        except:
            print(f"Problematic File?\t{filename}")
    if display_progress:
        print("|")
    if describe_results:
        total = accepted + rejected
        print(f"Queried {total} games:")
        acc_ratio, rej_ratio = round(100 * accepted / total, 1), round(100 * rejected / total, 1)
        print(f" Accepted {accepted} games ({acc_ratio}%)")
        if rejected > 0:
            print(f" Rejected {rejected} games ({rej_ratio}%)")
    return categories
