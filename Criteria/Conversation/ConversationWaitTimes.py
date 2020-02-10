

def flirt_wait_times(jason):
    waits = []
    in_convo = False
    # cooldown = False
    entrance = 0
    for event in jason["timeline"]:
        if event["event"] == "spy enters conversation.":
            in_convo = True
            entrance = event["elapsed_time"]
        elif event["event"] == "spy leaves conversation.":
            in_convo = False
        elif event["event"] == "action triggered: seduce target":
            if in_convo:
                flirtation = event["elapsed_time"]
                difference = round(flirtation - entrance,1)
                waits.append(difference)
        elif "flirt with seduction target:" in event["event"]:
            # cooldown = True
            continue
        elif event["event"] == "flirtation cooldown expired.":
            # cooldown = False
            entrance = event["elapsed_time"]
    if len(waits) > 0:
        return waits


def contact_wait_times(jason, real=True, fake=False):
    waits = []
    in_convo = False
    da_in = False
    entrance = 0
    for event in jason["timeline"]:
        if event["event"] == "spy enters conversation.":
            entrance = event["elapsed_time"]
        elif fake and event["event"] == "fake banana bread started.":
            diff = round(event["elapsed_time"] - entrance, 1)
            waits.append(diff)
        elif real and event["event"] == "real banana bread started.":
            diff = round(event["elapsed_time"] - entrance, 1)
            waits.append(diff)
    if len(waits) > 0:
        return waits
