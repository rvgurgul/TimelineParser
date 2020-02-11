from Classes.Parser import Parser


class TimerFlirts(Parser):

    def __init__(self, game):
        Parser.__init__(self, "Timer Flirts")
        self.spy_in_convo = False
        self.has_flirted_in_cc = False
        self.flirts_in_this_cc = []

    def parse(self, event):
        if event.desc == "spy enters conversation.":
            self.spy_in_convo = True
            self.has_flirted_in_cc = False
        elif event.desc == "spy leaves conversation.":
            self.spy_in_convo = False
            self.has_flirted_in_cc = False
        elif event.desc == "action triggered: seduce target" and self.spy_in_convo:
            self.has_flirted_in_cc = True
        # elif "flirt with seduction target:" in event.desc:
        #     self.flirt_cooldown = True
        elif event.desc == "flirtation cooldown expired." and self.spy_in_convo:
            # self.flirt_cooldown = False
            pass


# Spent the evening renovating my json-timeline project. I'd like some input on a data-output roadblock.
# I was rewriting my timer flirt parser and am now wondering what the best output would be: not only providing useful information (total/partial percent, action tests, etc) on its own, but also having some derived value (number of TFs, time invested, etc) as well.
# My initial approach was to return bundled percentage increases if they were in the same conversation (ex: [[33], [65, 100]]) From that, you can interpret there was 1 timer flirt and the last one was a (necessary) green
# Any thoughts on what would provide the most useful data?