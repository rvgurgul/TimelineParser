

def contact_initation_OLD(jason):
    contacts = []
    baking = None
    joiner, atr, outcome = "Neither", "", ""
    for event in jason["timeline"]:
        if event["event"] == "spy enters conversation.":
            joiner = "Neither"
        elif event["event"] == "spy joined conversation with double agent.":
            joiner = "Spy joins Double Agent"
        elif event["event"] == "double agent joined conversation with spy.":
            joiner = "Double Agent joins Spy"
        elif event["event"] == "double agent left conversation with spy.":
            if baking:
                atr += " (Sunshined)"
            else:
                joiner += ", Double Agent leaves"
        elif event["event"] == "spy left conversation with double agent.":
            joiner += ", Spy splits"
        elif event["event"] == "action triggered: contact double agent":
            baking = True
        elif event["category"] == ["ActionTest"] and event["mission"] == "Contact":
            atr = event["action_test"]
        elif event["event"] == "double agent contacted.":
            baking = False
            outcome = "Real Banana Bread"
        # elif event["event"]=="real banana bread uttered.":
        #    baking = False
        #    outcome = "IS THIS ONE POSSIBLE???"
        elif event["event"] == "fake banana bread uttered.":
            baking = False
            outcome = "Fake Banana Bread"
        elif event["event"] == "banana bread aborted.":
            baking = False
            outcome = "*Cough*"
            if atr == "Red":
                outcome = "*Cough Cough Cough Cough*"
            atr += " (Canceled)"
        elif event["event"] == "left alone while attempting banana bread.":
            baking = False
            outcome = "Banana Bread "

        if not baking:
            baking = None
            package = joiner, atr, outcome
            contacts.append(package)
            if package[1] == '':
                print(jason["uuid"], jason["spy"])
                print(contacts)
            joiner, atr, outcome = "Neither", "", ""

    if len(contacts) > 0:
        return contacts


def contact_initation(jason):
    contacts = []
    baking = None
    joiner, atr, outcome = "Neither", "", ""
    dough, bread = "", ""
    daInWithSpy = False
    for event in jason["timeline"]:

        if event["event"] == "action triggered: contact double agent":
            baking = True
            if daInWithSpy:
                print("should be real contact")
        elif event["event"] == "real banana bread started.":
            dough = "Real"
        elif event["event"] == "fake banana bread started.":
            dough = "Fake"

        elif event["event"] == "double agent contacted.":  # "banana bread uttered.":
            bread = "Real"
            baking = False
        elif event["event"] == "fake banana bread uttered.":
            bread = "Fake"
            baking = False
        elif event["event"] == "banana bread aborted.":
            bread = "Cough"
            baking = False
            if atr == "Red":
                outcome = "*Cough Cough Cough Cough*"
            atr += " (Canceled)"

        elif event["event"] == "spy joined conversation with double agent.":
            joiner = "Spy joins Double Agent"
            daInWithSpy = True
        elif event["event"] == "double agent joined conversation with spy.":
            joiner = "Double Agent joins Spy"
            daInWithSpy = True
        elif event["event"] == "double agent left conversation with spy.":
            daInWithSpy = False
            if baking:
                atr += " (Sunshined)"
            else:
                joiner += ", Double Agent leaves"
        elif event["event"] == "spy left conversation with double agent.":
            daInWithSpy = False
            joiner += ", Spy splits"
        elif event["event"] == "left alone while attempting banana bread.":
            baking = False
            bread = "Raw"

        elif event["category"] == ["ActionTest"] and event["mission"] == "Contact":
            atr = event["action_test"]

        if baking is False:
            baking = None
            if dough == bread:
                outcome = bread
            else:
                outcome = dough + " turned " + bread
            package = joiner, atr, outcome
            contacts.append(package)
            if package[1] == '':
                print(jason["uuid"], jason["spy"])
                print(contacts)
            joiner, atr, outcome = "Neither", "", ""

    if len(contacts) > 0:
        return contacts

