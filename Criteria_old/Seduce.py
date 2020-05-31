
def flirt_waits(game):
    cc_join_ts = 0
    results = []
    for event in game.timeline:
        if event.in_conversation and event == "action triggered: seduce target":
            results.append(round(event.time - cc_join_ts, 1))
        elif event == "spy enters conversation.":
            cc_join_ts = event.time
    return results


def flirt_before_grab(game, sensitivity=7):
    # TODO return True for before, False for after, None for no flirt
    pass

