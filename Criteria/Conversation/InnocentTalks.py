# count innocent talks
def simpleInnoTalks(jason):
    return len([0 for event in jason["timeline"] if event["event"]=="started talking."])
    count = 0
    for event in jason["timeline"]:
        if event["event"]=="started talking.":
            count += 1
    return count

# contacts and flirts are implicitly excluded
# bug covers are explicity excluded
def innoTalks(jason):
    count = 0
    triedToBug, inConvo = False, False
    for event in jason["timeline"]:
        if event["event"]=="started talking." and not triedToBug:
            count += 1
        elif event["event"]=="spy enters conversation.":
            inConvo = True
        elif event["event"]=="spy leaves conversation.":
            triedToBug, inConvo = False, False
        elif inConvo and "begin planting bug" in event["event"]:
            triedToBug = True
    return count

# total (incl): 5451
# total (excl): 5255
# talks to cover for bugs: 196
