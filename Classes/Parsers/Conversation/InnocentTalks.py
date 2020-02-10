from Classes.Parser import Parser


def innoTalks(jason):
    count = 0
    triedToBug, inConvo = False, False
    for event in jason["timeline"]:
        if event["event"]=="started talking." and not triedToBug:
            count += 1
        elif event["event"]=="spy enters conversation.":
            inConvo = True
        elif event["event"]=="spy leaves conversation.":
            triedToBug, inConvo = False, False
        elif inConvo and "begin planting bug" in event["event"]:
            triedToBug = True
    return count


class InnocentTalks(Parser):

    def __init__(self):
        Parser.__init__(self, "Inno-Talks")
        self.spy_in_convo = False
        self.tried_to_bug = False
        self.results = 0

    def parse(self, event):
        if event == "started talking." or event == "interrupted speaker.":
            if not self.tried_to_bug:
                self.results += 1
            else:
                print("bug cover")
            self.tried_to_bug = False
        elif event == "spy enters conversation.":
            self.spy_in_convo = True
        elif event == "spy leaves conversation.":
            self.tried_to_bug, self.spy_in_convo = False, False
        elif self.spy_in_convo and "begin planting bug" in event.desc:
            self.tried_to_bug = True


class InnocentTalkWaits(Parser):

    def __init__(self):
        Parser.__init__(self, "Inno-Talk Wait Times")
        self.joined_convo_timestamp = 0

    def parse(self, event):
        if event.desc == "spy enters conversation.":
            self.joined_convo_timestamp = event.time
        elif event.desc == "started talking." or event.desc == "interrupted speaker.":
            self.results.append(round(event.time - self.joined_convo_timestamp, 1))
