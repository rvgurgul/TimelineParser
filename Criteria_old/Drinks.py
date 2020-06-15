from Constants.EventGroups import *


def drink_durations(game):
    drink_acc_ts = 0
    drinks = []
    for event in game.timeline:
        if event in drink_accepts:
            drink_acc_ts = event.time
        elif event in drink_finishes:
            drinks.append(round(event.time - drink_acc_ts, 1))
    return drinks


def sip_at_bar(game, sensitivity=7):
    if not game.venue.bar:
        return None

    sip_expire = 0
    results = []
    for event in game.timeline:
        if event in {"got cupcake from bartender.", "got drink from bartender."}:
            sip_expire = event.time + sensitivity
        elif sip_expire > 0:
            if event.time < sip_expire:
                if event in {"sipped drink.", "bit cupcake."}:
                    results.append(True)
                    sip_expire = 0
            else:
                results.append(False)
                sip_expire = 0

    return results


def bar_drink_time_held(game):
    if not game.venue.bar:
        return None

    results = []
    delegating = False
    finish_ts = 0
    expire_ts = 0
    for event in game.timeline:
        if event == "delegating purloin guest list.":
            delegating = True
        elif delegating:
            if event in drink_accepts:
                expire_ts = event.time + 60  # delegate timer expiration
            elif event in drink_finishes:
                if expire_ts > 0:
                    results.append(round(expire_ts - event.time, 1))
                    expire_ts = 0
                else:
                    finish_ts = event.time
            elif event == "delegated purloin timer expired.":
                if finish_ts > 0:
                    results.append(round(event.time - finish_ts, 1))
                    finish_ts = 0
                else:
                    expire_ts = event.time
                delegating = False
    return results


# TODO move to trivia subdirectory
def toby_reoffer(game):
    prev_offer_ts = 0
    for event in game.timeline:
        if event in {"waiter stopped offering cupcake.", "waiter stopped offering drink."}:
            prev_offer_ts = event.time
        elif event in drink_requests_tray:
            prev_offer_ts = 0
        elif prev_offer_ts > 0 and event in {"waiter offered cupcake.", "waiter offered drink."}:
            return round(event.time - prev_offer_ts, 1)
