from Constants.Triple_Agent import player_list_scl_5
from Analyzer import *
from ParallelParser import parallel_parse


def prompt_user():
    user = input("Who would you like to research?\n")
    while user not in player_list_scl_5:
        confirm = input("Replays for '{}' may not be available, continue?".format(user))
        if confirm[0] == 'y':
            break
        else:
            user = input("Who would you like to research?\n")

    research_player(user)


def research_player(name):
    # TODO categorized queries: avoid double querying for two separate game pools
    spy_games = query_games(constraints=lambda game: game["spy"] == name)
    sni_games = query_games(constraints=lambda game: game["sniper"] == name)

    spy_results = parallel_parse(games=spy_games,
                                 parsers=[

                                 ],
                                 categorization=lambda game: game.venue)

    sni_results = parallel_parse(games=sni_games,
                                 parsers=[

                                 ],
                                 categorization=lambda game: game.venue)

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


prompt_user()
