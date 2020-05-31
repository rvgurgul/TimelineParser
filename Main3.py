from ParallelParser import *
from ListUnpacker import occurrence_report
from Stats import statistic_report, average_report
from CriteriaParsers.Conversations import conversation_durations
from CriteriaParsers.Characters import statue_animation_times, watch_check_animation_duration
from Reports import bar_chart


# qg = query_games(categorization_function=lambda game: (
#     (game.match.event, game.match.division) if "SCL" in game.match.event else None
# ))
qg = query_games(categorization_function=lambda game: game.cast.spy.name)

fl = (
    # NamedFunction("AT Rate", lambda game: tuple([
    #     "White" if event.action_test == "Ignored" else
    #     "Red" if event.action_test == "Canceled" else
    #     event.action_test for event in game.timeline if event.action_test != "NoAT"
    # ])),  # , occurrence_report),
    # NamedFunction("Conversation Time", conversation_durations),
    NamedFunction("Statue Animations", statue_animation_times),
)

results = {func.description: {cat: [] for cat in qg} for func in fl}
for cat in qg:
    for func in fl:
        # print(f"\n{cat}")
        results[func.description][cat] = func.parse_games(qg[cat])

# print(results)

for chara in results["Statue Animations"]:
    bar_chart(results["Statue Animations"][chara],
              sort_by='keys',
              title=f"{common_nicknames[chara]}'s Statue Animations",
              x_lab="Duration (s)",
              y_lab="Occurrences")
