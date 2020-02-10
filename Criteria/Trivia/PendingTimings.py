# if the game goes into pending overtime, what caused the OT, what was the last mission, what was the result?
def pendingOvertime(jason):
    pend_ts = 0
    pend_mi = ""
    pending = False
    for event in jason["timeline"]:
        if event["event"] == "missions completed. countdown pending.":
            print(event)
            pend_ts = event["elapsed_time"]
            pending = True
        elif pending and event["event"] == "missions completed. 10 second countdown.":
            pend_ts = round(event["elapsed_time"] - pend_ts, 1)
            print(pend_mi, "was pending for", pend_ts, "\bs")
        elif "MissionComplete" in event["category"]:
            pend_mi = event["mission"]


def pendingDurations(jason):
    if "Swap" not in jason["completed_missions"] and "Purloin" not in jason["completed_missions"]:
        return
    gsts, gpts = 0, 0
    psc, ppc = False, False
    for event in jason["timeline"]:
        if event["event"] == "statue swap pending.":
            gsts = event["elapsed_time"]
        elif event["event"] == "guest list purloin pending.":
            gpts = event["elapsed_time"]
        elif gsts > 0 and event["event"] == "statue swapped.":
            gsts = round(event["elapsed_time"] - gsts, 1)
            psc = True
        elif gpts > 0 and event["event"] == "guest list purloined.":
            gpts = round(event["elapsed_time"] - gpts, 1)
            ppc = True

    if psc and ppc:
        return ("Green Swap", gsts), ("Green Purloin", gpts)
    if not psc and ppc:
        return ("Green Purloin", gpts),
    if psc and not ppc:
        return ("Green Swap", gsts),
