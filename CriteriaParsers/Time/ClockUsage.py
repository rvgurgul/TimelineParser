from Classes.Parser import Parser


class ClockUsage(Parser):

    def __init__(self, game):
        Parser.__init__(self, "Clock Usage")
        self.start_clock = game.clock
        self.end_clock = game.timeline[-3].time
        # this does not violate the parallelization because it is an index, not a loop
        self.results = str(round(100*self.end_clock/self.start_clock, 1))+"%"
        # currently returns a percent (string) of clock time used, how is this a good idea
        # in fact, this is so easily computed, it was possible without the timeline at all (via spyparsey)
        self.complete = True
        # TODO mark all non-parsing parsers (lol what) as complete for eventual removal
        #  if a parser need not parse the timeline, should it just be a game property?


class TimeAddUsage(Parser):

    def __init__(self, game):
        Parser.__init__(self, "Added Time Usage")
        if not game.reaches_mwc:
            self.complete = True
        else:
            self.start_clock = game.clock
            self.time_added = 0

    def parse(self, event):
        if self.complete:
            return
        if event == "45 seconds added to match.":
            self.time_added += 45
        elif self.time_added > 0 and "GameEnd" in event.categories:
            self.results = round(event.time-self.start_clock, 1)


