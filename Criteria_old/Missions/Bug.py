

def get_bug_attempts(jason, only_real=True):
    if only_real and "Bug" not in jason["picked_missions"]:
        return "Bug Disabled"
    if only_real and "Bug" not in jason["completed_missions"]:
        return "Bug Incomplete"
    att = []
    bug_type = ""
    planting, in_convo, transit = False, False, False
    for event in jason["timeline"]:
        # TODO twitch bug edge cases
        if event["event"] == "spy enters conversation.":
            if transit or bug_type == "Exit":
                bug_type = "Twitch"
            elif planting:
                bug_type = "Entry"
            in_convo = True
        elif event["event"] == "spy leaves conversation.":
            if transit or bug_type == "Entry":
                bug_type = "Twitch"
            elif planting:
                bug_type = "Exit"
            in_convo = False
        elif "bugged ambassador while" in event["event"]:
            if only_real:
                return bug_type
            att.append(bug_type)
            return att
        elif event["event"] == "begin planting bug while walking.":
            planting = True
            if in_convo:
                bug_type = "Reverse"
            else:
                bug_type = "Walking"
        elif event["event"] == "begin planting bug while standing.":
            planting = True
            bug_type = "Standing"
        elif event["event"] == "bug transitioned from standing to walking.":
            transit = True
        elif event["event"] == "failed planting bug while walking.":
            planting, transit = False, False
            bug_type += " (Failed)"
            att.append(bug_type)
            bug_type = ""
    return att

    # action triggered: bug ambassador
    # begin planting bug while standing.
    # begin planting bug while walking.
    # bug ambassador enabled.
    # bug ambassador selected.
    # bug transitioned from standing to walking.
    # bugged ambassador while standing.
    # bugged ambassador while walking.
    # failed planting bug while walking.
