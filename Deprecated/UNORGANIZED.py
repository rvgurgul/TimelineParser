def spyAmbaLightPair(jason):
    a, s = getAmba(jason), getSpy(jason)
    timestamp = 0
    attempts = []
    for i, event in enumerate(jason["timeline"]):
        if event["event"] == "action triggered: bug ambassador":
            #timestamp = event["time_elapsed"]
            al = mostRecentLight(jason, a, i)
            sl = mostRecentLight(jason, s, i)
            tup = (al, sl, unspecWinCon(jason["win_type"]))
            attempts += [tup]
    if len(attempts)>0:
        return attempts#, a, s, jason["win_type"]

x = analyze(spyAmbaLightPair, 2000)
counter = {}
for y in x:
    for z in y:
        if z not in counter:
            counter[z] = 1
        else:
            counter[z] += 1
for x in counter:
    print(x,"\t",counter[x])




def flirtPair(jason):
    return getSpy(jason), getST(jason)


data = analyze(flirtPair)


pairs = {}
for spy in playable_cast:
    for st in playable_cast:
        pairs[spy,st]=0


for pair in data:
    if pair[0] is None or pair[1] is None:
        print("Missing Spy/ST")
    else:
        pairs[pair] += 1
print(pairs)









# how many games of Moderne 5/8 would have had the same result had they been Moderne 4/8?
def moderneBalance(jason):
    if jason["venue"] != "Moderne":
        return
    completed = 0
    timestamp = 0
    for event in jason["timeline"]:
        print(event["category"], completed)
        if "MissionComplete" in event["category"]:
            completed += 1
            if completed is 4:
                timestamp = event["elapsed_time"]
                fakeMissionCountdown = lookAhead(jason, timestamp)
                print(fakeMissionCountdown)
        elif "SniperShot" in event["category"]:
            if event["role"] == "Spy":
                return "SpyShot"
            else:
                return "CivShot"


# if no shot happens, then MissWin
# if no 5th mission and TimeOut, then MissWin
# if spy completed a 5th mission, and
#    is not shot then MissWin
#    is shot then Inconclusive
#    civ is shot, then CivShot

analyze(moderneBalance, 100)






def lookAhead(jason, initial, time=10):
    events = []
    print(initial, time)
    for event in jason["timeline"]:
        if initial <= event["elapsed_time"] and event["elapsed_time"] < initial + time:
            print("\t",event["elapsed_time"],"is in range")
            events.append(event)
    return events













def threeGreenBalcony(jason):
    if jason["venue"] != "Balcony":
        return
    if jason["completed_missions"] != ["Seduce", "Contact"]:
        return
    tests = []
    for event in jason["timeline"]:
        if "ActionTest" in event["category"]:
            if event["mission"]=="Seduce" or event["mission"]=="Contact":
                if event["action_test"]=="Green":
                    result = event["action_test"]+" "+event["mission"]
                    tests.append(result)
                else:
                    return
            else:
                return
        elif event["event"]=="action triggered: bug ambassador":
            return
    if len(tests)==3:
        return specWinCon(jason["win_type"]), jason["spy"]+" vs "+jason["sniper"]
analyze(threeGreenBalcony)












