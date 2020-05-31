
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
