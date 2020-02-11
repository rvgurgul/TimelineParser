def watchChecks(jason):
    inno, time = 0, 0
    for event in jason["timeline"]:
        if event["event"]=="watch checked to add time.":
            time += 1
        elif event["event"]=="watch checked.":
            inno += 1
    return inno, time
