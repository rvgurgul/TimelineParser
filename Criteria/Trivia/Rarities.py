def tooLate(jason):
    for event in jason["timeline"][-1:-10:-1]:
        if "sniper shot too late for sync."==event["event"]:
            return jason["sniper"]
        if event["event"]=="left alone while attempting banana bread.":
            pass
        elif event["event"]=="cast member picked up pending statue.":
            pass