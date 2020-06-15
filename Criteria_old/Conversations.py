


# class InnocentTalks(Parser):
#
#     def __init__(self, game):
#         Parser.__init__(self, "Inno-Talks")
#         self.spy_in_convo = False
#         self.tried_to_bug = False
#         self.results = 0
#
#     def parse(self, event):
#         if event == "started talking." or event == "interrupted speaker.":
#             if not self.tried_to_bug:
#                 self.results += 1
#             self.tried_to_bug = False
#         elif event == "spy enters conversation.":
#             self.spy_in_convo = True
#         elif event == "spy leaves conversation.":
#             self.tried_to_bug, self.spy_in_convo = False, False
#         elif self.spy_in_convo and "begin planting bug" in event.desc:
#             self.tried_to_bug = True


def rushed_stop_talk(game, sensitivity=1.8):
    last_talk_ts = 0
    results = []
    for event in game.timeline:
        if "uttered" in event or "flirt with seduction target:" in event:
            last_talk_ts = event.time + sensitivity
        elif last_talk_ts > 0:
            if event.time < last_talk_ts:
                if event == "stopped talking.":
                    results.append(True)
                    last_talk_ts = 0
            else:
                results.append(False)
                last_talk_ts = 0
    return results

