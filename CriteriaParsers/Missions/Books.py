from Classes.Parser import Parser


intermediate = {
    "action triggered: bug ambassador",
    "spy enters conversation.",
    "spy leaves conversation.",
    "spy picks up briefcase.",
    "watch checked.",
    "read book.",
}
# can briefcase, can conversate, can read, can bug, can watch
# cannot statue, cannot drink


class BookCookCookbook(Parser):

    def __init__(self, game):
        Parser.__init__(self, "Book Cook")
        self.takeout_timestamp = 0
        self.taken_away = False
        # TODO retry fingerprintable books
        # self.printable = False
        # self.fingerprint = "Innocent"

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
        elif event.desc in intermediate:
            self.taken_away = True
        elif event == "put book in bookcase.":
            cat = "Direct Transfer" if event.held_book != event.bookshelf \
                else "Innocent Return" if self.taken_away \
                else "Innocent Read"

            pkg = (cat, round(event.time-self.takeout_timestamp, 1))
            self.results.append(pkg)
