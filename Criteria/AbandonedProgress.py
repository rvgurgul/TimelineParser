

def absolute_progress(jason, missions=[]):
    # complete may either be False (0), True (1), or n in Z > 1 representing which attempt finalized the mission
    # restated, "Attempts"["Complete"] returns the mission-finishing action

    blank = {"Complete": False, "Attempts": []}

    progress = {}
    #     "Bug": {
    #         "Complete": 0,      # true indicates [-1] was a successful bug
    #         "Attempts": [],
    #     },
    #     "Contact": {
    #         "Complete": 0,      # int indicates the nth contact was real
    #         "Attempts": [],     # each includes who joined who, who split, action test, start/end bb status and timestamps
    #     },
    #     "Seduce": {
    #         "Complete": 0,      # int indicates the number of flirts it took to complete seduce
    #         "Attempts": [],     # each includes the action test, the percent increase, the location (vaguely; convo, statue, books, bar, or other), timestamp, and isTimerFlirt
    #     },
    #     "Inspects": {
    #         "Complete": 0,
    #         "Attempts": [],     # each includes the action test, and the interrupted, if applicable
    #     },
    #     "Microfilm": {
    #         "Complete": 0,
    #         "Attempts": []
    #     },
    #     "Fingerprint": {
    #         "Complete": 0,
    #         "Attempts": []      # each includes the object type and difficulty, as well as action test where applicable
    #     },
    #     "Swap": {
    #         "Complete": 0,      # true once the statue has been swapped, not during pending
    #         "Attempts": []      # includes the action test, and if applicable, pending time
    #     },
    #     "Purloin": {
    #         "Complete": 0,      # true once the list has been purloined, not during pending
    #         "Attempts": []      # includes the action test, and if applicable, pending time
    #     },
    #     "Time": {
    #         "Complete": 0,      # always false
    #         "Attempts": []      # includes the action_test, timestamp (before), and if applicable, cancellation or overtime
    #     }
    # }

    last_mis, last_atr, last_out = "", "", ""
    for event in jason["timeline"]:
        if "ActionTriggered" in event["category"]:
            last_mis = event["mission"]
            if last_mis == "NoMission":
                last_mis = "Time"
            if last_mis not in progress:
                progress[last_mis] = {
                    "Complete": False,
                    "Attempts": []
                }
        elif "ActionTest" in event["category"]:
            last_atr = event["action_test"]
            last_mis = event["mission"]
            if last_mis == "NoMission":
                last_mis = "Time"
            progress[last_mis]["Attempts"].append(last_atr)
        elif "MissionComplete" in event["category"]:
            progress[event["mission"]]["Complete"] = True
        elif "MissionPartial" in event["category"]:
            progress[event["mission"]]["Attempts"].append(event["event"])
        # elif "flirt with seduction target: " in event["event"]:
        #     percent = event["event"].split(":")[1]
        #     percent = int(percent[1:len(percent)-1])
        # elif event["event"] == "seduction canceled.":
        #     pass

    return progress


def abandoned(jason):
    incomplete = {
        "FailedBugAttempts": 0,
        "SeductionPercent": 0,
        "FakeBananaBreads": 0,
        "PartialInspects": 0,
        "PendingSwap": False,
        "PendingPurloin": False,
        "MicrofilmInPocket": "",
        "FingerprintAttempts": 0
    }
    for event in jason["timeline"]:
        if "MissionPartial" in event["category"] and event["mission"] in incomplete:
            incomplete[event["mission"]] += 1
        elif "Purloin" in incomplete and event["event"] == "guest list purloin pending.":
            incomplete["Purloin"] = "Pending"
        elif "Swap" in incomplete and event["event"] == "statue swap pending.":
            incomplete["Swap"] = "Pending"
        elif "Bug" in incomplete and "failed planting bug" in event["event"]:
            incomplete["Bug"] += 1
    return incomplete

