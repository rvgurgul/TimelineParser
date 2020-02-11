from Constants.Venues import bookless_venues


def describe_microfilm(jason, append_test=False, append_shot=False, prepend_stage=False):
    if jason["venue"] in bookless_venues:
        return "", ""
    if append_shot:
        ts = 0
    if append_test:
        atr = ""
    micro = []
    for event in jason["timeline"]:
        if event["event"] == "remove microfilm from book." or event["event"] == "hide microfilm in book.":
            item = event["books"][1]
            if prepend_stage:
                item = str(len(micro)+1) + ": " + item
            if append_test:
                item += " ({})".format(atr)
            micro.append(item)
            if append_shot:
                ts = event["elapsed_time"] + 10
        elif append_shot and len(micro) > 0:
            if event["event"] == "sniper shot spy." and event["elapsed_time"] < ts:
                micro[-1] += " [Shot]"
            elif event["event"] == "put book in bookcase.":
                ts = event["elapsed_time"] + 10
        elif append_test and "ActionTest" in event["category"] and event["mission"] == "Transfer":
            atr = event["action_test"]
    if len(micro) > 0:
        return micro
