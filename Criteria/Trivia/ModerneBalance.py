from Helpers import get_specific_win_condition

# returns the original result of the original 5/8 moderne game,
# as well as the result if the game had been played 4/8


def moderne_four_eight(jason):
    if jason["venue"] != "Moderne" or jason["game_type"] != "a5/8":
        return

    original = get_specific_win_condition(jason)
    if len(jason["completed_missions"]) < 4:
        return original, original

    missions, countdown = 0, 0
    for event in jason["timeline"]:
        if countdown > 0:
            if event["elapsed_time"] <= countdown:
                if "SniperShot" in event["category"]:
                    return original, "Retroactive Countdown " + event["role"][0] + "Shot"
            else:
                return original, "Retroactive MissWin"
        elif missions < 4 and "MissionComplete" in event["category"]:
            missions += 1
            if missions == 4:
                countdown = event["elapsed_time"] + 10
    return original, "Retroactive MissWin"
