

def timerFlirts(jason):
    spyInConvo, hasFlirtedInConvo = False, False
    flirtsInThisConvo = []
    flirts = []
    count = 0
    for event in jason["timeline"]:
        if event["event"] == "spy enters conversation.":
            spyInConvo = True
            hasFlirtedInConvo = False
        elif event["event"] == "spy leaves conversation.":
            spyInConvo = False
            hasFlirtedInConvo = False
            if len(flirtsInThisConvo) > 0:
                flirts.append(flirtsInThisConvo)
                flirtsInThisConvo = []
        elif "flirt with seduction target:" in event["event"]:
            percent = event["event"].split(":")[1]
            percent = int(percent[1:len(percent) - 1])

            if hasFlirtedInConvo:
                count += 1

            if spyInConvo:
                flirtsInThisConvo.append(percent)
                hasFlirtedInConvo = True
            else:
                flirts.append([percent])

    if len(flirtsInThisConvo) > 0:
        flirts.append(flirtsInThisConvo)
    if len(flirts) > 0:
        return count, flirts, jason["spy"]
