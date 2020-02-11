from Classes.Parsers.Conversation.FlirtDowntime import FlirtDowntime
from CriteriaParsers.Conversations.InnocentTalks import InnocentTalks
from Classes.Parsers.Miscellaneous.FlirtPair import FlirtPair
from Classes.Parsers.NonMissions.WatchChecks import WatchChecks
from Classes.Parsers.NonMissions.DrinkOffers import DrinkOffers
from Classes.Parser import Parser
from Analyzer import query_games
from Classes.Game import Game


def parallel_parse(games: [Game], parsers: [Parser], categorization=lambda game: game.uuid):
    results = {}
    for game in games:
        active_parsers = [parser(game) for parser in parsers]
        for event in game.timeline:
            for parser in active_parsers:
                parser.parse(event)

        # TODO retry multicategorization, is it necessary?
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

