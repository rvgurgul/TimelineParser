from ParallelParser import *
from ListUnpacker import occurrence_report
from Stats import statistic_report, average_report
from CriteriaParsers.Seduce import *
from CriteriaParsers.Drinks import *
from CriteriaParsers.Books import *
from CriteriaParsers.Sniper import lowlight_quickdraw

qg = query_games(categorization_function=lambda game: game.sniper)
# nf = NamedFunction("Flirt Cooldowns", flirt_cooldowns, statistic_report)
# nf.parse_games(qg)

fl = (
    # NamedFunction("Sips per drink", sips_per_drink, statistic_report),
    # NamedFunction("Microfatality", micro_fatality, occurrence_report),
    # NamedFunction("Toby Response Time", offer_response_time, average_report),
    NamedFunction("LL Quickdraw", lowlight_quickdraw, statistic_report),
)

for cat in qg:
    for func in fl:
        print("\n", cat)
        func.parse_games(qg[cat])
