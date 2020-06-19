import json
from collections import Counter
from ParallelParser import query_games

from CharacterParsers import *

qg = query_games()

funx = {
    "chara_info/watch_check_durations": watch_check_durations,
    "chara_info/statue_hold_durations": statue_hold_times,
}

for fx in funx:
    results = {ch: Counter() for ch in "ABCDEFGHIJKLMNOPQRSTU"}
    print(f"analyzing {fx}")
    for game in qg:
        res = funx[fx](game)
        if res is not None:
            chara = game.cast.spy.name[-1]
            if type(res) is not list:
                results[chara][res] += 1
            else:
                results[chara].update(res)
    with open(f"json_outputs/{fx}.json", "w") as file:
        json.dump(results, file, indent=1)

