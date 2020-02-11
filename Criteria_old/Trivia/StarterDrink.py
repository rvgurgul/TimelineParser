from Constants.Events import drink_sips


business = {
    "get book from bookcase.",
    "picked up statue.",
    "bartender offered cupcake.",
    "bartender offered drink.",
    "waiter offered cupcake.",
    "waiter offered drink.",
    "request cupcake from bartender.",
    "request cupcake from waiter.",
    "request drink from bartender.",
    "request drink from waiter.",
}


def spy_started_with_drink(jason):
    for event in jason["timeline"]:
        # cannot determine if the spy started with a drink which was finished under ai-control.
        if event["event"] in drink_sips:
            return True
        elif event["event"] in business:
            return False
    # return "Maybe"
