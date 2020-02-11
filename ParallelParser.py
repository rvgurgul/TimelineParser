from Classes.Parsers.Conversation.ConversationDurations import ConversationDurations
from Classes.Parsers.Conversation.FlirtDowntime import FlirtDowntime
from Classes.Parsers.Conversation.InnocentTalks import InnocentTalks
from Classes.Parsers.Miscellaneous.FlirtPair import FlirtPair
from Classes.Parsers.Missions.Bug import BugAttempts
from Classes.Parsers.Missions.Contact import ContactInitiations
from Classes.Parsers.NonMissions.WatchChecks import WatchChecks
from Classes.Parsers.NonMissions.DrinkOffers import DrinkOffers
from Classes.Parsers.Parser import Parser
from Analyzer import query_games
from Classes.Game import Game


def parallel_parse(games: [Game], parsers: [Parser], categorization=lambda game: game.uuid):
    results = {}
    for game in games:
        active_parsers = [parser(game) for parser in parsers]
        for event in game.spy_timeline:
            for parser in active_parsers:
                parser.parse(event)
        # TODO category merging
        results[categorization(game)] = {parser.critera: parser.get_results() for parser in active_parsers}
    return results


from Classes.Parsers.VenueSpecific.Moderne import ModerneFourEight

qg = query_games()
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
                   ])
for y in x:
    print(y)
    print(x[y])
    # print(json.dumps(x[y], indent=4))

