from ParallelParser import *
from Stats import statistic_report, average_report
from ListUnpacker import occurrence_report

from CriteriaParsers.Books import *
from CriteriaParsers.Bug import *
from CriteriaParsers.Characters import *
from CriteriaParsers.Contact import *
from CriteriaParsers.Conversations import *
from CriteriaParsers.Drinks import *
from CriteriaParsers.Fingerprint import *
from CriteriaParsers.Random import *
from CriteriaParsers.Seduce import *
from CriteriaParsers.Statues import *
from CriteriaParsers.Sniper import *
from CriteriaParsers.Time import *


# qg = query_games(limit=1500)
# fl = {
#     # "Purloin Descs": describe_purloin,
#     "Bar Sips": sip_at_bar,
#     "Bar Drinks": bar_drink_time_held,
#     "Bar Queues": bar_queue_time,
#     "Return to the scene of the crime": return_to_bar_after_purloin,
#     # "Statue Behav.": describe_statues,
#     # "PAWS": paws,
#     "Bad Stoptalks": rushed_stop_talk,
#     "Audibles": audibles,
#     "Destination": initial_destination,
#     "Initations": contact_initiations,
# }

qg = query_games(limit=1500)
function_list = (
    # NamedFunction("Bar Sips", sip_at_bar, average_report),
    # NamedFunction("Returning to the scene of the crime", return_to_bar_after_purloin, average_report),
    # NamedFunction("Direct Purloin Rate", delegate_vs_direct, average_report),
    # NamedFunction("Bug Take Rate", bug_connections, average_report),
    # NamedFunction("Improper Stoptalks", rushed_stop_talk, average_report),
    # NamedFunction("Time Add Rate", watch_check_ratio, average_report),
    # NamedFunction("Sip Gulp Rate", sip_vs_gulp, average_report),
    NamedFunction("Bug Attempts", describe_bug_attempts, occurrence_report),
    NamedFunction("Initiations", contact_initiations, occurrence_report),
    NamedFunction("Statue Descriptions", describe_statues, occurrence_report),
    NamedFunction("Purloin Descriptions", describe_purloin, occurrence_report),
    NamedFunction("Flirt Downtime", flirt_downtime, statistic_report),
    NamedFunction("Flirt Pair", flirt_pair, occurrence_report),
    NamedFunction("Fingerprints", fingerprints, occurrence_report),

    # NamedFunction("Destination", initial_destination, occurrence_report),
)
for category in qg:
    for fx in function_list:
        fx.parse_games(qg[category])

