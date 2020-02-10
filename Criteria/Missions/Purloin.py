from Constants.Venues import bar_venues


def get_delegate_time(jason):
    if "Purloin" not in jason["completed_missions"] or jason["venue"] not in bar_venues:
        return
    ts = 0
    for event in jason["timeline"]:
        if event["event"] == "delegating purloin guest list.":
            ts = event["elapsed_time"]
        elif event["event"] == "delegated purloin timer expired.":
            ts = 0
        elif event["event"] == "guest list purloined.":
            # only return the time difference if it was a delegated purloin
            return round(event["elapsed_time"] - ts, 1) if ts > 0 else None
