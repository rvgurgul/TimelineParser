from ParallelParser import query_games
from json import dump

# assemble player list
qg = query_games()[None]

players = {}
for game in qg:
    if game.spy not in players:
        players[game.spy] = game.spy_username
        # print(f"inserted new alias: {game.spy}")
    if game.sniper not in players:
        players[game.sniper] = game.sniper_username
        # print(f"inserted new alias: {game.sniper}")

with open("json_stats/player_aliases.json", "w") as f:
    dump(players, f, indent=4)


