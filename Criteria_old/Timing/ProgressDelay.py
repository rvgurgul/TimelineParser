progress = {
    'action triggered: bug ambassador': "Bug",
    'action triggered: contact double agent': "Contact",
    'action triggered: fingerprint ambassador': "Fingerprint",
    'action triggered: inspect statues': "Inspect",
    'action triggered: purloin guest list': "Purloin",
    'action triggered: seduce target': "Seduce",
    'action triggered: swap statue': "Swap",
    'action triggered: transfer microfilm': "Transfer",
    'watch checked to add time.': "Time Add"
}
def progressDelay(jason):
    takeControl = 0
    for event in jason["timeline"]:
        if event["event"]=="spy player takes control from ai.":
            takeControl = event["elapsed_time"]
        elif event["event"] in progress:
            return takeControl, event["elapsed_time"], progress[event["event"]]

