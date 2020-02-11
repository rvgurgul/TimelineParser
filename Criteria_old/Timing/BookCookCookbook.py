def cookbook(jason):
    takeout = 0
    for event in jason["timeline"]:
        if event["event"] == "get book from bookcase.":
            takeout = event["elapsed_time"]
        elif event["event"] == "put book in bookcase.":
            if event["books"][0] != event["books"][1]:
                return round(event["elapsed_time"] - takeout, 1)

