from Classes.Parser import Parser


class ConversationDurations(Parser):

    def __init__(self, game):
        Parser.__init__(self, "Conversation Durations")
        self.spy_in_convo = False
        self.convo_timestamp = 0

    def parse(self, event):
        if event.desc == "spy enters conversation.":
            self.spy_in_convo = True
            self.convo_timestamp = event.time
        elif event.desc == "spy leaves conversation.":
            self.spy_in_convo = False
            self.results.append(round(event.time - self.convo_timestamp, 1))
        elif "GameEnd" in event.categories and self.spy_in_convo:
            self.results.append(round(event.time - self.convo_timestamp, 1))
