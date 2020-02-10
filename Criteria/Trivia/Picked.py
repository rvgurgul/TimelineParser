

def pickVsSelect(jason):
    if jason["game_type"][0]=="p":
        return jason["picked_missions"], jason["selected_missions"]