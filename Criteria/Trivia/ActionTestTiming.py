

def action_test_result_timings(jason):
    actionTests = []
    ts = 0
    for event in jason["timeline"]:
        if "action triggered:" in event["event"]:
            ts = event["elapsed_time"]
        elif "ActionTest" in event["category"]:
            result = event["action_test"]
            if result != "Canceled":
                mission = event["mission"]
                if mission != "Fingerprint":
                    if mission == "NoMission":
                        mission = "Time Add"
                    package = round(event["elapsed_time"] - ts, 1), result, mission
                    actionTests.append(package)

    if len(actionTests) > 0:
        # print(actionTests)
        return actionTests

