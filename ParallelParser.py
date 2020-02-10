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

g = [Game(x) for x in query_games(limit=30, constraints=lambda game: game["venue"] == "Moderne" and game["game_type"] == "a5/8")]

x = parallel_parse(games=g,
                   parsers=[ModerneFourEight])
                   # parsers=[
                   #     FlirtPair,
                   #     ConversationDurations,
                   #     FlirtDowntime,
                   #     # FlirtWaits,
                   #     # RealContactWaits,
                   #     # FakeContactWaits,
                   #     # InnocentTalkWaits,
                   #     InnocentTalks,
                   #     BugAttempts,
                   #     ContactInitiations,
                   #     WatchChecks,
                   #     DrinkOffers,
                   # ])
for y in x:
    print(y)
    print(x[y])
    # print(json.dumps(x[y], indent=4))

