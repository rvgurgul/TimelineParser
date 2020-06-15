from Constants.EventGroups import lights_abbreviated, lights

def lowlight_quickdraw(game):
    cast = {"Toby": False, "Damon": False, game.cast.ambassador.name: False}
    if game.venue != "Balcony":
        for sda in game.cast.suspected_agents:
            cast[sda.name] = False
        cast[game.cast.double_agent.name] = False

    for event in game.timeline:
        if event.categories == {"SniperLights"}:
            # if event.time < 0:
            #     print("DISQUALIFIED")
            #     return
            chara = event.character.name
            if chara in cast:
                cast[chara] = True
                if all(cast.values()):
                    return event.time


def lowlight_speedrun(game):
    cast = {"Toby": None, "Damon": None, game.cast.ambassador.name: None}
    if game.venue != "Balcony":
        for sda in game.cast.suspected_agents:
            cast[sda.name] = None
        cast[game.cast.double_agent.name] = None

    for event in game.timeline:
        if event.categories == {"SniperLights"}:
            # if event.time < 0:
            #     print("DISQUALIFIED")
            #     return
            chara = event.character.name
            if chara in cast and cast[chara] is None:
                cast[chara] = event.time
                # print(cast)
                if all(cast.values()):
                    return cast
    return cast


def plague_doctor(game):
    if game.cast.shot is None:
        return
    red_tested = False
    cough_ts = 0
    for event in game.timeline:
        if "ActionTest" in event.categories and event.mission == "Contact" and event.action_test == "Red":
            red_tested = True
        elif red_tested and "uttered." in event.desc:
            cough_ts = event.time
            red_tested = False
        elif event == "banana bread aborted.":
            cough_ts = event.time
        elif cough_ts > 0 and "SniperShot" in event.categories:
            diff = round(event.time - cough_ts, 1)
            return diff, event.character.role


def highlight_tension(game):
    if game.cast.shot is None:
        return
    shot_ts = 0
    for event in game.timeline[::-1]:
        if "SniperShot" in event.categories:
            shot_ts = event.time
        elif ["SniperLights"] == event.categories and event.character == game.character_shot:
            return round(shot_ts - event.time, 1)
    # no prior sniper light (default neutral)
    return shot_ts


def contact_lowlights(game, bunched=False):
    snapshot = {}
    suspects = {c.name: "DL" for c in game.cast if c.role in {"Spy", "SeductionTarget", "Civilian"}}
    if game.venue.name == "Balcony":  # unknown double agent
        suspects[game.cast.double_agent] = "DL"

    bb_ts = 0
    results = []
    for event in game.timeline:
        if "banana bread uttered" in event:
            bb_ts = event.time + 10
            snapshot = suspects.copy()
        elif event.categories == {"SniperLights"}:
            chara = event.character.name
            if chara in suspects:
                suspects[chara] = lights_abbreviated[event.desc]
        elif bb_ts > 0 and (event.time > bb_ts or "GameEnd" in event.categories):
            changed = (
                f"{snapshot[chara]}->{suspects[chara]}" for chara in suspects if suspects[chara] != snapshot[chara]
            )
            if bunched:
                results.append(changed)
            else:
                for chara in changed:
                    results.append(chara)
            bb_ts = 0
    return results


def exterminator(game):
    spy_light, amba_light = "Default Light", "Default Light"
    outcome = "No Reaction"
    bug_ts = 0
    attempts = []
    for event in game.timeline:
        if event.categories == {"SniperLights"}:
            if event.character.role in {
                "Spy", "Ambassador"
            }:
                spy_light = lights[event]
        elif "begin planting bug" in event:
            bug_ts = event.time + 10

        if event.time < bug_ts:
            if event == [
                "marked spy suspicious.",
                "marked spy neutral suspicion.",
                "marked spy less suspicious.",
            ]:
                outcome = event.desc
            elif event == [
                "sniper shot spy.",
                "missions completed successfully.",
                "spy ran out of time.",
            ]:
                # must separate game ending outcomes because no events follow to push to results
                attempts.append((spy_light, amba_light, event.desc))
        elif event.time > bug_ts > 0:  # PogChamp I didn't know this could be done
            attempts.append((spy_light, amba_light, outcome))
            bug_ts = 0
            outcome = "No reaction"
    return attempts

