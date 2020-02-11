printable = {
    "fingerprinted briefcase.": "Briefcase",
    "fingerprinted statue.": "Statue",
    "fingerprinted book.": "Book",
    "fingerprinted drink.": "Drink",
    "fingerprinted cupcake.": "Drink"
}


def fingerprints(jason, only_success=True):
    prints = []
    item, atr = "", ""
    for event in jason["timeline"]:
        if event["event"] in printable:
            item = printable[event["event"]]
            if only_success and "Fail" in atr:
                continue
            prints.append(item + atr)
        elif event["category"] == ["ActionTest"] and event["mission"] == "Fingerprint":
            if event["action_test"] == "Green":
                atr = " (Difficult Success)"
            else:
                atr = " (Difficult Failure)"
    if len(prints) > 0:
        return prints
