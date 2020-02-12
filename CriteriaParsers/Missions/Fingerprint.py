from Classes.Parser import Parser


printable = {
    "started fingerprinting book.": "Book",
    "started fingerprinting briefcase.": "Briefcase",
    "started fingerprinting cupcake.": "Drink",
    "started fingerprinting drink.": "Drink",
    "started fingerprinting statue.": "Statue",
}


class DescribeFingerprints(Parser):

    def __init__(self, game):
        Parser.__init__(self, "Fingerprint Attempts")
        self.last_atr = "NoAT"
        self.item = ""

    # TODO track fingerprintable statue/briefcase which were not printed
    def parse(self, event):
        if event.desc in printable:
            self.item = printable[event.desc]
        elif "fingerprinted" in event.desc or event == "fingerprinting failed":
            pkg = (self.item, self.last_atr)
            self.results.append(pkg)
            self.last_atr = "NoAT"
        elif "ActionTest" in event.categories and event.mission == "Fingerprint":
            self.last_atr = event.action_test
