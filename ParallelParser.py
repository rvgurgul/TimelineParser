from CriteriaParsers.Missions.Seduce import *
from CriteriaParsers.Conversations.InnocentTalks import InnocentTalks
from CriteriaParsers.Conversations.ConversationDurations import ConversationDurations
from CriteriaParsers.Conversations.ConversationWaits import *
from CriteriaParsers.Missions.Purloin import DrinkOffers
from CriteriaParsers.Time.WatchChecks import WatchChecks
from CriteriaParsers.Sniper.LowlightQuickdraw import LowlightQuickdraw
from CriteriaParsers.Sniper.PlagueDoctor import PlagueDoctor
from CriteriaParsers.Missions.Fingerprint import DescribeFingerprints
from CriteriaParsers.Missions.Statues import DescribeStatues
from CriteriaParsers.Missions.Books import BookCookCookbook
from CriteriaParsers.Sniper.HighlightTension import HighlightTension
from CriteriaParsers.Time.ProgressDelay import ProgressDelay
from CriteriaParsers.Time.Overtime import Overtime
from CriteriaParsers.Time.ClockUsage import *
from CriteriaParsers.Trivia.StarterDrink import StarterDrink
from CriteriaParsers.Sniper.SniperLatency import SniperLatency
from CriteriaParsers.Trivia.ContactDelay import ContactFudge
from CriteriaParsers.Time.Activity import CountdownActivity, ContactActivity
from CriteriaParsers.Time.PendingTimings import PendingDurations
from CriteriaParsers.Missions.Bug import BugAttempts
from CriteriaParsers.Missions.Purloin import DescribePurloin
from CriteriaParsers.Trivia.WatchCheckAnimations import WatchCheckAnimations
from CriteriaParsers.Sniper.BugExterminator import BugExterminator
from CriteriaParsers.Sniper.ContactLowlights import ContactLowlights

from Classes.Parser import Parser
from Analyzer import query_games
from Classes.Game import Game


def parallel_parse(games: [Game], parsers: [Parser], categorization=lambda game: game.uuid):
    results = {}
    for game in games:
        # instantiate the parser classes
        active_parsers = [parser(game) for parser in parsers]
        for event in game.timeline:
            for parser in active_parsers:
                parser.parse(event)
                # if parser.complete:  # increased load checking for parser completion,
                #     active_parsers.pop(i)  # reduced load removing completed parsers

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


do_first = True
if do_first:
    qg = query_games(limit=1500)
    x = parallel_parse(games=[Game(x) for x in qg],
                       parsers=[
                           ContactLowlights,
                           BugExterminator,
                           WatchCheckAnimations,
                           BookCookCookbook,
                           FlirtIncreases,
                           DescribePurloin,
                           BugAttempts,
                           PendingDurations,
                           # ContactActivity,
                           # CountdownActivity,
                           ClockUsage,
                           TimeAddUsage,
                           StarterDrink,
                           Overtime,
                           ProgressDelay,
                           # HighlightTension,
                           DescribeStatues,
                           DescribeFingerprints,
                           # PlagueDoctor,
                           LowlightQuickdraw,
                           FlirtCooldowns,
                           FlirtPair,
                           # ConversationDurations,
                           FlirtDowntime,
                           # FlirtWaits,
                           # RealContactWaits,
                           # FakeContactWaits,
                           # InnocentTalkWaits,
                           # InnocentTalks,
                           # BugAttempts,
                           # ContactInitiations,
                           # WatchChecks,
                           # DrinkOffers,
                       ],
                       categorization=lambda game: game.venue)

else:
    qg = query_games()
    x = parallel_parse(games=[Game(x) for x in qg],
                       parsers=[ContactFudge],
                       categorization=lambda game: None)

for y in x:
    print(y)
    for z in x[y]:
        print(" ", z, "\t\t", x[y][z])

