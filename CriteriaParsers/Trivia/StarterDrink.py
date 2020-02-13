from Classes.Parser import Parser
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


class StarterDrink(Parser):

    def __init__(self, game):
        Parser.__init__(self, "Starter Drink")

    def parse(self, event):
        if self.complete:
            return
        # cannot guarantee certainty if the drink was completed during ai-control
        elif event.desc in drink_sips:
            self.results = True
            self.complete = True
        elif event.desc in business:
            self.results = False
            self.complete = True
