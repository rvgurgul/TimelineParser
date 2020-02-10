

def get_first_test_for_action(jason, mission):
    for event in jason["timeline"]:
        if "ActionTest" in event["category"] and event["mission"] == mission:
            return event["action_test"]


def get_tests_for_action(jason, mission):
    tests = []
    for event in jason["timeline"]:
        if "ActionTest" in event["category"] and event["mission"] == mission:
            tests.append(event["action_test"])
    return tests
