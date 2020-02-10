def takeControlTime(jason):
    for event in jason["timeline"]:
        if event["event"]=="spy player takes control from ai.":
            return event["elapsed_time"]
