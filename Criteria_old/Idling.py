
# sum times between innocent actions IF no suspicious action occurs in between

# joins empty conversation (no flirts occur within the conversation and the double agent is not in too)

# bookcase is ok IF no fingerprint or microfilm occurs
# briefcase is ok IF there is not even a difficult print
# statue is ok IF inspect is complete AND the spy does not print/swap
# conversation is ok IF the double agent is out AND no purloin/bug/fingerprint/seduce occurs
# time between two of these events is ok IF there is no purloin/bug/fingerprint/seduce/transfer/time add occurs
# if contact has been completed, then the double agent is irrelevant

# if toby is ignored, that time is not considered idling because the spy's attention was elsewhere
# if the spy takes out a book and does action test microfilm with that book, then none of the time with the book is idle
# if the spy takes out a book and eventually direct transfers that book, then none of the time with the book is idle


# from Constants.Gameplay import missions
#
# inno_actions = {
#     'bartender offered cupcake.',
#     'bartender offered drink.',
#     'bartender picked next customer.',
#     'bit cupcake.',
#     'cast member picked up pending statue.',
#     'character picked up pending statue.',
#     'chomped cupcake.',
#     'double agent left conversation with spy.',
#     'game started.',
#     'get book from bookcase.',
#     'got cupcake from bartender.',
#     'got cupcake from waiter.',
#     'got drink from bartender.',
#     'got drink from waiter.',
#     'interrupted speaker.',
#     'picked up statue.',
#     'put back statue.',
#     'put book in bookcase.',
#     'read book.',
#     'rejected cupcake from bartender.',
#     'rejected cupcake from waiter.',
#     'rejected drink from bartender.',
#     'rejected drink from waiter.',
#     'request cupcake from bartender.',
#     'request cupcake from waiter.',
#     'request drink from bartender.',
#     'request drink from waiter.',
#     'sipped drink.',
#     'spy enters conversation.',
#     'spy leaves conversation.',
#     'spy picks up briefcase.',
#     'spy player takes control from ai.',
#     'spy puts down briefcase.',
#     'spy returns briefcase.',
#     'started talking.',
#     'took last bite of cupcake.',
#     'took last sip of drink.',
#     'waiter offered cupcake.',
#     'waiter offered drink.',
#     'waiter stopped offering cupcake.',
#     'waiter stopped offering drink.',
#     'watch checked.'
# }
#
#
# # TODO verify the results of this function (time between correct events matches self-calculated replay analysis)
# def idle_time(jason, normalized=False):
#     total, last_action = 0, 0
#     contacted, idling = False, True
#
#     # sum times between innocent actions IF no suspicious action occurs in between
#
#     # joins empty conversation (no flirts occur within the conversation and the double agent is not in too)
#
#     # bookcase is ok IF no fingerprint or microfilm occurs
#     # briefcase is ok IF there is not even a difficult print
#     # statue is ok IF inspect is complete AND the spy does not print/swap
#     # conversation is ok IF the double agent is out AND no purloin/bug/fingerprint/seduce occurs
#     # time between two of these events is ok IF there is no purloin/bug/fingerprint/seduce/transfer/time add occurs
#     # if contact has been completed, then the double agent is irrelevant
#
#     for event in jason["timeline"]:
#         if event["actor"] == "sniper":
#             # ignore sniper actions (like lights and bookmarks)
#             continue
#
#         if "MissionComplete" in event["category"] and event["mission"] == "Contact":
#             contacted = True
#         elif event["event"] in inno_actions:
#             if idling:
#                 total += event["elapsed_time"] - last_action
#                 last_action = event["elapsed_time"]
#             idling = True
#         else:
#             idling = False
#
#         if not contacted:
#             if event["event"] == "spy joined conversation with double agent." \
#                     or event["event"] == "double agent joined conversation with spy.":
#                 idling = False
#                 last_action = event["elapsed_time"]
#             elif event["event"] == "double agent left conversation with spy." \
#                     or event["event"] == "spy left conversation with double agent.":
#                 if idling:
#                     total += event["elapsed_time"] - last_action
#                     last_action = event["elapsed_time"]
#                 idling = True
#
#     if normalized:
#         duration = jason["timeline"][-1]["elapsed_time"]
#         return total / duration
#     return round(total, 1)
