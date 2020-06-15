from ParallelParser import query_games
from json import dump

# assemble player list
qg = query_games()

players = {}
def update_players(alias, username):
    if alias not in players:
        players[alias] = username

users = {}
def update_users(alias, username, date):
    steam = alias.endswith("/steam")
    if username not in users:
        users[username] = {
            "current_alias": alias[:-6] if steam else alias,
            "prior_aliases": [] if steam else None,
            "earliest_appearance": date,
            "latest_appearance": date,
        }
    else:
        data = users[username]
        if date > data["latest_appearance"]:
            data["latest_appearance"] = date
            if steam and alias[:-6] != data["current_alias"]:
                data["prior_aliases"].append(data["current_alias"])
                data["current_alias"] = alias[:-6]
        elif date < data["earliest_appearance"]:
            data["earliest_appearance"] = date
            if steam and alias[:-6] != data["current_alias"] and alias[:-6] not in data["prior_aliases"]:
                data["prior_aliases"].append(alias[:-6])

for game in qg:
    update_players(game.spy, game.spy_username)
    update_players(game.sniper, game.sniper_username)
    update_users(game.spy, game.spy_username, game.date)
    update_users(game.sniper, game.sniper_username, game.date)

with open("json_outputs/player_aliases.json", "w") as f:
    dump(players, f, indent=4)

with open("json_outputs/user_aliases.json", "w") as f:
    dump(users, f, indent=4)


