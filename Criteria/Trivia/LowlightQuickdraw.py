from Helpers import get_characters_of_role


def castLowlightTime(jason):
    cast = {"Toby": False, "Damon": False, get_characters_of_role(jason, "Ambassador"): False}
    if jason["venue"] != "Balcony":
        SDAs = get_characters_of_role(jason, "SuspectedDoubleAgent")
        if type(SDAs) is str:
            cast[SDAs] = False
        else:
            for SDA in SDAs:
                cast[SDA] = False
        cast[get_characters_of_role(jason, "DoubleAgent")] = False
        # print(jason["venue"], cast)

    for event in jason["timeline"]:
        if "SniperLights" in event["category"]:
            # exclude any lowlights that occur 'before' the game starts
            if event["elapsed_time"] <= 0:
                return
            if event["cast_name"][0] in cast:
                cast[event["cast_name"][0]] = True
                if sum(cast.values()) == len(cast):
                    return event["elapsed_time"]


# x = analyze(castLowlightTime, categorization=sniper_venue)
# x = analyze(castLowlightTime, categorization=venue)

# for y in x:
#     print(y, "Results")
#     statDump(x[y])