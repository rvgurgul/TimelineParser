from Classes.StatLoader import StatLoader

def player_lookup(alias) -> str:
    loader = StatLoader()
    players = loader.get_stat("player_aliases")
    if alias in players:  # uses the efficient search first
        return players[alias]
    steamed = f"{alias}/steam"
    if steamed in players:
        return players[steamed]

    a_lower = alias.lower()
    s_lower = steamed.lower()
    for player in players:  # then tries a less efficient, case insensitive search
        p_lower = player.lower()
        if p_lower == a_lower or p_lower == s_lower:
            return players[player]
    print(f"No player by the name of '{alias}' was found.")

def convert_time_to_clock(game, time) -> float:
    loader = StatLoader()
    time_lookup = loader.get_stat("game_info/clock")
    events = time_lookup[game]
    for i in range(len(events) - 1):  # try to find a suitable time interval
        if events[i]["time"] < time < events[i + 1]["time"]:
            return events[i]["clock"] - time + events[i]["time"]
    return events[-1]["clock"] - time + events[-1]["time"]  # handles the last or only element
    # TODO return 0:00 for hanging OT

def get_alias(username):
    loader = StatLoader()
    users_to_alias = loader.get_stat("json_outputs/user_aliases.json")
    if username in users_to_alias:
        return users_to_alias[username]["current_alias"]
    raise Exception(f"username {username} not found")

def get_username(alias):
    loader = StatLoader()
    alias_to_users = loader.get_stat("json_outputs/player_aliases.json")
    if alias in alias_to_users:
        return alias_to_users[alias]
    raise Exception(f"alias {alias} not found")
