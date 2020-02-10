from Classes.Parsers.Parser import Parser


class DrinkOffers(Parser):

    def __init__(self, game):
        Parser.__init__(self, "Drink Accept Ratio")

    def parse(self, event):
        if event.desc in [
            "got drink from bartender.",
            "got drink from waiter.",
            "got cupcake from bartender.",
            "got cupcake from waiter.",
        ]:
            self.results.append(True)
        elif event.desc in [
            "rejected drink from bartender.",
            "rejected drink from waiter.",
            "rejected cupcake from bartender.",
            "rejected cupcake from waiter.",
        ]:
            self.results.append(False)
        # TODO differentiate purloin and fingerprintable drinks
