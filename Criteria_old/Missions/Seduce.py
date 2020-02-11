

def seduce_composition(jason, include_fails=False):
    flirts = []
    lastAT, percent = "NoAT", "0"
    for event in jason["timeline"]:
        if event["event"]=="action triggered: seduce target":
            lastAT, percent = "None", "0"
        elif event["category"]==["ActionTest"] and event["mission"]=="Seduce":
            lastAT = event["action_test"]
        elif "flirt with seduction target:" in event["event"]:
            percent = event["event"].split(":")[1]
            percent = int(percent[1:len(percent)-1])
            if len(flirts)>0:
                percent -= sum([flirt[0] for flirt in flirts[-1::-1]])
            package = percent, lastAT
            flirts.append(package)
        elif include_fails:
            if event["event"]=="failed flirt with seduction target.":
                package = 0, lastAT
                flirts.append(package)
            elif event["event"]=="seduction canceled.":
                if lastAT != "Canceled":
                    lastAT += ", Canceled"
                package = 0, lastAT
                flirts.append(package)
    if len(flirts) > 0:
        return flirts
