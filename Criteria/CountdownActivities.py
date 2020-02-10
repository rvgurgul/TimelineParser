from Helpers import event_lookahead

desired = [
    'demand drink from bartender.',
    'request drink from bartender.',
    'got drink from bartender.',
    'rejected drink from bartender.',
    'request drink from waiter.',
    'got drink from waiter.',
    'rejected drink from waiter.',
    # 'waiter gave up',
    'sipped drink.',
    'took last sip of drink.',
    'gulped drink.',

    # 'demand cupcake from bartender.',
    # 'request cupcake from bartender.',
    # 'got cupcake from bartender.',
    # 'rejected cupcake from bartender.',
    # 'request cupcake from waiter.',
    # 'got cupcake from waiter.',
    # 'rejected cupcake from waiter.',
    # 'bit cupcake',
    # 'took last bite of cupcake.',
    # 'chomped cupcake.',

    'picked up statue.',
    'put back statue.',

    'spy enters conversation.',
    'spy leaves conversation.',

    'spy picks up briefcase.',
    'spy puts down briefcase.',
    'spy returns briefcase.',

    'get book from bookcase.',
    'put book in bookcase.',
    'read book.',

    'action triggered: bug ambassador',
    'action triggered: check watch',
    'action triggered: contact double agent',
    'action triggered: fingerprint ambassador',
    'action triggered: inspect statues',
    'action triggered: purloin guest list',
    'action triggered: seduce target',
    'action triggered: swap statue',
    'action triggered: transfer microfilm'
]

def countdownActivities(jason):
    for i, event in enumerate(jason["timeline"]):
        if "missions completed" in event["event"]:
            return [x["event"] for x in jason["timeline"][i + 1::] if x["event"] in desired]





def activityBeforeBB(jason):
    for i, event in enumerate(jason["timeline"]):
        if "banana bread uttered." in event["event"]:
            return [x["event"] for x in event_lookahead(jason, i, reverse=True) if x["event"] in desired]


def activityAfterBB(jason):
    for i, event in enumerate(jason["timeline"]):
        if "banana bread uttered." in event["event"]:
            return [x["event"] for x in event_lookahead(jason, i, reverse=True) if x["event"] in desired]
