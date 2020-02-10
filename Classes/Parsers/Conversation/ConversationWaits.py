from Classes.Parsers.Parser import Parser


class FlirtWaits(Parser):

    def __init__(self, game):
        Parser.__init__(self, "Flirt Wait Times")
        self.spy_in_convo = False
        self.joined_convo_timestamp = 0
        self.flirt_cooldown = False

    def parse(self, event):
        if event.desc == "spy enters conversation.":
            self.spy_in_convo = True
            self.joined_convo_timestamp = event.time
        elif event.desc == "spy leaves conversation.":
            self.spy_in_convo = False
        elif event.desc == "action triggered: seduce target" and self.spy_in_convo:
            self.results.append(round(event.time - self.joined_convo_timestamp, 1))
        # elif "flirt with seduction target:" in event.desc:
        #     self.flirt_cooldown = True
        elif event.desc == "flirtation cooldown expired." and self.spy_in_convo:
            # self.flirt_cooldown = False
            self.joined_convo_timestamp = event.time


class RealContactWaits(Parser):

    def __init__(self, game):
        Parser.__init__(self, "Real Contact Wait Times")
        self.joined_convo_timestamp = 0
        # self.spy_in_convo = False
        # self.spy_in_with_da = False

    def parse(self, event):
        if event.desc == "spy enters conversation.":
            # self.spy_in_convo = True
            self.joined_convo_timestamp = event.time
        # elif event.desc == "spy leaves conversation.":
        #     self.spy_in_convo = False
        # elif event.desc == "spy joined conversation with double agent." \
        #         or event.desc == "double agent joined conversation with spy.":
        #     self.spy_in_with_da = True
        # elif event.desc == "spy left conversation with double agent." \
        #         or event.desc == "double agent left conversation with spy.":
        #     self.spy_in_with_da = False
        elif event.desc == "real banana bread started.":
            self.results.append(round(event.time - self.joined_convo_timestamp, 1))


class FakeContactWaits(Parser):

    def __init__(self, game):
        Parser.__init__(self, "Fake Contact Wait Times")
        self.joined_convo_timestamp = 0

    def parse(self, event):
        if event.desc == "spy enters conversation.":
            self.joined_convo_timestamp = event.time
        elif event.desc == "fake banana bread started.":
            self.results.append(round(event.time - self.joined_convo_timestamp, 1))

