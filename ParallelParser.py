from Classes.Game import Game
from collections import Counter
from Constants.Triple_Agent import PARSED_GAME_COUNT

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


def query_games(constraints=None,
                limit=PARSED_GAME_COUNT,
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


# SPF format:
# uuid : []

def parse_games(games, functions):
    results = {}
    # for fx_name in functions:
    #     results[fx_name] = []
    #     fx = functions[fx_name]
    #     for game in games:
    #         result = fx(game)
    #         if result is not None:
    #             if type(result) is list:
    #                 for x in result:
    #                     results[fx_name].append(x)
    #             else:
    #                 results[fx_name].append(result)
    for fx in functions:
        result = fx.parse_games(games)
        results[fx.description] = result
    return results


class NamedFunction:
    def __init__(self, desc, func, output_func=None):
        self.description = desc
        self.function = func
        self.analysis = output_func

    def parse_games(self, games):
        results = []
        for game in games:
            result = self.function(game)
            if result is None:
                continue
            if type(result) is list:
                for x in result:
                    results.append(x)
            else:
                results.append(result)
        if self.analysis is not None:
            print(f"{self.description}")  # \n{'-'*len(self.description)}")
            self.analysis(results)
        return results
