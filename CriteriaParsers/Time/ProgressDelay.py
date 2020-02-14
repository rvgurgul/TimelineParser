from Classes.Parser import Parser


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


class ProgressDelay(Parser):

    def __init__(self, game):
        Parser.__init__(self, "First Progress")

    def parse(self, event):
        if self.complete:
            return

        if event.desc in progress:
            self.results = (event.time, progress[event.desc])
            self.complete = True
        # Direct Transfers never involve an 'action triggered: transfer microfilm' event
        elif event == "put book in bookcase.":
            if event.held_book != event.bookshelf:
                self.results = (event.time, "Transfer")
                self.complete = True


class TakeControlTime(Parser):

    def __init__(self, game):
        Parser.__init__(self, "No-Control Time")

    def parse(self, event):
        if self.complete:
            return
        # TODO package first spy destination
        #  (leave convo, put down statue, put back book, watch, Toby, etc.)
        if event == "spy players takes control from ai.":
            self.results = event.time
            self.complete = True
