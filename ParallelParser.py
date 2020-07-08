from Classes.Game import Game
from datetime import datetime

import json
import os

root = "json_games/"


def debug(uuid):
    try:
        file = open(f"{root}{uuid}.json", "r")
        lines = "".join([line.strip() for line in file.readlines()])
        file.close()
        jason = json.loads(lines)
        from Classes.Game import Game
        game = Game(jason)
        print(game)
        return game
    except FileNotFoundError:
        print(f"Failed debug of {uuid}.json", sep="")


def query_games(constraints=None, categorization_function=None, limit: int = None) -> [Game]:
    try:
        data_dir = os.listdir(root)
    except:
        os.chdir("..")  # If query_games is called in a subdirectory, json_gamez/ is not found at that level
        data_dir = os.listdir(root)
    # TODO hard to do limit/progress bar/query stats with advanced iterable functions :(

    if limit is not None and limit > 0:
        data_dir = data_dir[:limit]

    before = datetime.now()
    print("Querying jsons, please wait...", end="")
    jsons = filter(constraints, [json.load(open(f"{root}{filename}", "r")) for filename in data_dir])
    print(f"done (took {datetime.now() - before})")

    before = datetime.now()
    print("Querying games, please wait...", end="")
    games = list(map(Game, jsons))
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

'''
qg = query_games()
print(len(qg))

qg = query_games(constraints=lambda j: j["spy"] == "skrewwl00se" or j["sniper"] == "skrewwl00se")
print(len(qg))

qg = query_games(constraints=lambda j: j["sniper"] == "krazycaley")
print(len(qg))

qg = query_games(constraints=lambda j: j["spy"] == "Legorve Genine/steam")
print(len(qg))

qg = query_games(constraints=lambda j: j["venue"] == "Ballroom")
print(len(qg))
'''
# TODO load_games(uuids)

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
                delta = (101 * (accepted + rejected) // limit)
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
