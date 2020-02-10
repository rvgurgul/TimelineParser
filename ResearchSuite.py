from Constants.Triple_Agent import player_list_scl_5
from Analyzer import *


def research_player(name):

    user = input("Who would you like to research?\n")
    while user not in player_list_scl_5:
        confirm = input("Replays for '{}' may not be available, continue?".format(user))
        if confirm[0] == 'y':
            break
        else:
            user = input("Who would you like to research?\n")

    spy_games = query_games(constraints=lambda game: game["spy"] == user)
    sni_games = query_games(constraints=lambda game: game["sniper"] == user)

    # SPY:
    # conversation
    #  seduce wait
    #  contact wait
    #  innocent talks?
    #  contact init.
    # progress delay
    # book cook
    # no-control time
    # timer flirt frequency
    # time add ratio
    # inspect behavior
    # common fingerprints
    # drink behavior

    # SNIPER:
    #

    pass


research_player("")

