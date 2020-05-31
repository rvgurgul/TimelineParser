
def moderne_four_eight(game):
    if game.venue.name != "Moderne" or game.mode != "a5/8":
        return

    original = game.specific_win_condition
    if len(game.missions_complete) < 4:
        return original

    missions, countdown = 0, 0
    for event in game.timeline.events:
        if countdown > 0:
            if event.time <= countdown:
                if "SniperShot" in event.categories:
                    if event.character.role == "Spy":
                        return "Retroactive Countdown SpyShot"
                    return "Retroactive Countdown CivilianShot"
            else:
                return "Retroactive MissWin"
        elif missions < 4 and "MissionComplete" in event.categories:
            missions += 1
            if missions == 4:
                countdown = event.time + 10
    return "Retroactive MissWin"
