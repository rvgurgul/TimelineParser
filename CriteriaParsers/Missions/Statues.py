from Classes.Parser import Parser


class DescribeStatues(Parser):

    def __init__(self, game):
        Parser.__init__(self, "Statue Description")
        if game.venue == "Balcony":
            self.complete = True
        else:
            self.results = ""
            self.visited = False
            self.holding = False

    def parse(self, event):
        if self.complete:
            return

        if event == "picked up statue.":
            if self.visited:
                self.results += " "
            self.visited = True
            self.holding = True
        elif "statue inspected." in event.desc:
            self.results += "I"
        elif event == "inspection interrupted.":
            self.results += "i"
        elif event == "statue swap pending.":
            self.results += "s"
        elif event == "cast member picked up pending statue.":
            self.results += "~"
        elif event == "statue swapped.":
            self.results += "S"
        elif event == "fingerprinted statue.":
            self.results += "P"
        elif self.holding and event == "fingerprinting failed.":
            self.results += "p"
        elif self.holding and "flirt with seduction target: " in event.desc:
            self.results += "F"
        elif self.holding and event == "seduction canceled.":
            self.results += "f"
        elif event == "put back statue.":
            self.results += "."
            self.holding = False
        # elif self.holding and event == "sniper shot spy.":
        #     self.results += "[X]"
