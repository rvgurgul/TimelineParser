from Constants.Events import *
from Constants.Venues import bar_venues


# returns a boolean list which can be averaged to easily find someone's rate of drink accepts vs rejects
def inno_drink_takes(jason, exclude_purloin=True):
    offers = []
    purloin_test = None
    for event in jason["timeline"]:
        if event["event"] in drink_accepts:
            if purloin_test is not None and purloin_test != "Green":
                purloin_test = None
                continue
            offers.append(True)
        elif event["event"] in drink_rejects:
            if purloin_test == "Green":
                purloin_test = None
                continue
            offers.append(False)
        elif exclude_purloin and "ActionTest" in event["category"] and event["mission"] == "Purloin":
            purloin_test = event["action_test"]
    return offers


# TODO translate to parser
def general_delegate_description(jason):
    if "Purloin" not in jason["picked_missions"]:
        return "Purloin Disabled"
    if "Purloin" not in jason["completed_missions"]:
        return "Purloin Incomplete"
    for event in jason["timeline"]:
        if event["event"] == "guest list purloined.":
            return "Direct Purloin" if event["role"] == ["Spy"] else "Delegated Purloin"


# TODO translate to parser
def specific_delegate_description(jason, only_real=True):
    if "Purloin" not in jason["picked_missions"]:
        return "Purloin Disabled"
    if only_real and "Purloin" not in jason["completed_missions"]:
        return "Purloin Incomplete"
    if jason["venue"] not in bar_venues:
        return "Nonexistant Bar"

    # TODO frick terrace >:( exclude terrace games before the bar update
    # if jason["venue"] == "Terrace"

    attempts = []
    current = []
    took_drink = False
    for event in jason["timeline"]:
        if event["event"] == "guest list purloined.":
            if event["role"] == ["Spy"]:
                attempts.append("Direct take.")
            else:
                current.append("took.")
                attempts.append(" ".join(current))
                current = []
        elif event["event"] == "delegating purloin guest list.":
            current.append("Delegate")
            took_drink = False
        elif event["event"] in drink_accepts:
            took_drink = True
        elif "delegated purloin to" in event["event"]:
            if not took_drink:
                current.append("cheese")
                took_drink = True
            current.append("to "+event["role"][0])
        elif event["event"] == "delegated purloin timer expired.":
            if not took_drink:
                current.append("cheese")
                took_drink = True
            current.append("expired.")
            attempts.append(" ".join(current))
            current = []

    return attempts[-1] if only_real else attempts
