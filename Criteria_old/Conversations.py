
def conversation_durations(game):
    spy_in_convo = False
    cc_join_ts = 0
    results = []
    for event in game.timeline:
        if spy_in_convo:
            if not event.in_conversation:  # spy has left
                spy_in_convo = False
                results.append(round(event.time - cc_join_ts, 1))
            elif "GameEnd" in event.categories:  # game has ended
                results.append(round(event.time - cc_join_ts, 1))
        else:  # spy not in convo
            if event.in_conversation:  # spy has entered
                spy_in_convo = True
                cc_join_ts = event.time
    return results


def innocent_talk_waits(game):
    # tried_to_bug = False
    cc_join_ts = 0
    results = []
    for event in game.timeline:
        if event == "spy enters conversation.":
            cc_join_ts = event.time
        elif event in {"started talking.", "interrupted speaker."}:
            results.append(round(event.time - cc_join_ts, 1))
        # elif "begin planting bug" in event.desc and event.in_conversation:
        #     tried_to_bug = True
        # TODO discount amba-related talks


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


def number_of_talks(game):
    count = 0
    for event in game.timeline:
        if event in {
            "started talking.",
            "interrupted speaker.",
            "action test white: contact double agent",
            "action test red: contact double agent",
            "action test ignored: contact double agent",
        }:
            count += 1
        elif event.in_conversation and event == "action triggered: seduce target":
            count += 1
    return count


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

