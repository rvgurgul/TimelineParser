
def micro_fatality(game):
    anim_ts = 0
    atts = 0
    for event in game.timeline:
        if event == "action triggered: transfer microfilm":
            anim_ts = event.time + 10
            atts += 1
        elif 0 < event.time < anim_ts and event == "took shot." and event.character.role == "Spy":
            return atts
