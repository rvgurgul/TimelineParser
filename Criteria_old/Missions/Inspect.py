from Constants.Venues import venue_information


def inspection(jason):
    if "Inspect" not in jason["picked_missions"]:
        return
    needed = venue_information[jason["venue"], "Inspects"]
    pickups = 0
    inspects = []
    holdingStatue = False
    i_completed, i_attempted = 0, 0
    for event in jason["timeline"]:
        if event["event"]=="picked up statue.":
            pickups += 1
            holdingStatue = True
        elif jason["venue"]=="Redwoods" and event["event"]=="get book from bookcase.":
            holdingStatue = True
        elif event["event"]=="put back statue." or event["event"]=="dropped statue." or jason["event"]=="put book in bookcase.":
            holdingStatue = False
            package = i_completed, i_attempted
            inspects.append(i_completed)
            i_completed, i_attempted = 0, 0
        elif event["event"]=="action triggered: inspect statues":
            i_attempted += 1
        elif "statue inspected." in event["event"]:
            i_completed += 1
            i_attempted -= 1
    return pickups, tuple(inspects)