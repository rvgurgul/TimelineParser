from CriteriaParsers.Missions.Flirt import *
from CriteriaParsers.Conversations.InnocentTalks import InnocentTalks
from CriteriaParsers.Conversations.ConversationDurations import ConversationDurations
from CriteriaParsers.Conversations.ConversationWaits import *
from CriteriaParsers.Activity.DrinkOffers import DrinkOffers
from CriteriaParsers.Activity.WatchChecks import WatchChecks
from CriteriaParsers.Sniper.LowlightQuickdraw import LowlightQuickdraw
from CriteriaParsers.Sniper.PlagueDoctor import PlagueDoctor

from Classes.Parser import Parser
from Analyzer import query_games
from Classes.Game import Game


def parallel_parse(games: [Game], parsers: [Parser], categorization=lambda game: game.uuid):
    results = {}
    for game in games:
        active_parsers = [parser() for parser in parsers]
        for parser in active_parsers:
            parser.prepare(game)
        for event in game.timeline:
            for parser in active_parsers:
                parser.parse(event)
                # TODO consider removing parsers which have marked themselves complete to reduce load

        # TODO retry multicategorization, is it necessary?
        # TODO solve mono-categorization, particularly, allow integer/tuple/etc. values instead of lists of everything
        category = categorization(game)
        if category not in results:
            results[category] = {parser.critera: [] for parser in active_parsers}
        for parser in active_parsers:
            res = parser.get_results()
            if type(res) is not list:
                res = [res]
            for x in res:
                results[category][parser.critera].append(x)
    return results


qg = query_games(limit=5000)
x = parallel_parse(games=[Game(x) for x in qg],
                   parsers=[
                       PlagueDoctor,
                       LowlightQuickdraw,
                       FlirtCooldowns,
                       FlirtPair,
                       # ConversationDurations,
                       FlirtDowntime,
                       # FlirtWaits,
                       # RealContactWaits,
                       # FakeContactWaits,
                       # InnocentTalkWaits,
                       InnocentTalks,
                       # BugAttempts,
                       # ContactInitiations,
                       WatchChecks,
                       DrinkOffers,
                   ],
                   categorization=lambda game: game.venue)
for y in x:
    print(y)
    print(x[y])
    # print(json.dumps(x[y], indent=4))

