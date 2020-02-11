
def conversationLengths(jason):
    temp = 0
    conversations = []
    spyInConvo = False
    for event in jason["timeline"]:
        if event["event"] == "spy enters conversation.":
            temp = event["elapsed_time"]
            spyInConvo = True
        elif event["event"] == "spy leaves conversation.":
            difference = round(event["elapsed_time"] - temp, 1)
            conversations.append(difference)
            spyInConvo = False
        elif "GameEnd" in event["category"] and spyInConvo:
            difference = round(event["elapsed_time"] - temp, 1)
            conversations.append(difference)
    return conversations

def totalConversationLength(jason):
    return round(sum(conversationLengths(jason)), 1)

# which spies spend the most time in conversation?
# which venues have the most time in conversation?
# does time in conversation at all impact win chances?
# if so, which snipers are able to shoot spies who spent more/less time in conversation?