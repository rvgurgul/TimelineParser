from Classes.Parser import Parser


# it is possible, but unlikely, the spy walks away from a bookcase then returns without one of these events occurring
intermediate = {
    "action triggered: bug ambassador",
    "spy enters conversation.",
    "spy leaves conversation.",
    "spy picks up briefcase.",
    "watch checked.",
    "read book.",
}
# can briefcase, can conversate, can read, can bug, can check watch
# cannot statue, cannot drink


class BookCookCookbook(Parser):

    def __init__(self, game):
        Parser.__init__(self, "Book Cook")
        self.takeout_timestamp = 0
        self.taken_away = False
        self.at_micro = None

    def parse(self, event):
        if event == "get book from bookcase.":
            self.takeout_timestamp = event.time
            self.taken_away = False
            # self.printable = False
            # self.fingerprint = "Innocent"
        # elif event == "started fingerprinting book.":
        #     self.printable = True
        # elif self.printable and event == "fingerprinted book.":
        #     self.fingerprint = "Printable"
        # elif self.printable and "ActionTest" in event.categories and "Fingerprint" == event.mission:
        #     if event.action_test == "Green":
        #         self.fingerprint = "DFP_hit"
        #     else:
        #         self.fingerprint = "DFP_miss"
        #     self.printable = False
        elif event == intermediate:
            self.taken_away = True
        elif event == "remove microfilm from book.":
            self.at_micro = ("Remote " if self.taken_away else "")+"{} Microfilm Take".format(event.bookshelf)
        elif event == "hide microfilm in book.":
            self.at_micro = ("Remote " if self.taken_away else "")+"{} Microfilm Hide".format(event.bookshelf)
        elif event == "put book in bookcase.":
            cat = self.at_micro if self.at_micro is not None \
                else "Direct Transfer ({} to {})".format(event.held_book, event.bookshelf) if event.held_book != event.bookshelf \
                else "Innocent Return" if self.taken_away \
                else "Innocent Visit"
            # TODO printable books
        # TODO held books when the game ends are untracked
        # elif "GameEnd" in event.categories and self.at_micro is not None:

            pkg = (cat, round(event.time-self.takeout_timestamp, 1))
            self.results.append(pkg)
