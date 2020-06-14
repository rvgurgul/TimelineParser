from collections import Counter
from ResearchSuite import stat_loader, statistic_report

# NOTE: Unless stated otherwise, questions are based on every game played during SCL seasons 4 and 5, including the
# postseason, totaling 10,089 games.

game_lights = stat_loader("json_outputs/game_info/sniper_lights.json")
game_casts = stat_loader("json_outputs/game_info/cast.json")
# 1. Which is most common: highlighting the Ambassador, lowlighting them, or leaving them neutral?
# 2. What's the percentage difference between highlighting and lowlighting the Ambassador?

amba_light_pref = Counter()
for g in game_lights:
    amba = game_casts[g]["Ambassador"]
    lght = -5
    for light in game_lights[g][::-1]:
        if light["chara"] == amba:
            lght = light["light"]
            break
    amba_light_pref[lght] += 1
print(amba_light_pref.most_common())

# 3. When a spy ends the game lowlit, what percentage of the time do they win?
# 4. When a spy ends the game highlit, what percentage of the time do they win?
# 5. When a spy ends the game lowlit, which happens more often: spy shot, or timeout?
# 6. Which spy has been lowlit the most?

# 7. Contact the Double Agent is the most-completed mission on every venue, but there are two venues where it's
#    close. What are they, and what's the next-closest in each?

# 8. What's the overall green action test rate?
# 9. What percentage of action tests result in red tests, NOT counting difficult fingerprints?
# 10. How often do spies win when they hit a green test on a tray Purloin?
# 11. How often do spies win when they hit a white test on a tray Purloin?

# 12. How often does checker purloin when presented with an opportunity? NOTE: this means tray drink offers (
#     requested or not) when Purloin is active, and has not yet taken place.

# 13. Which player has ignored Toby the most times, excluding Challenger matches?
# 14. What percentage of bar purloins are direct, rather than delegated?
# 15. Which bar venue has the highest direct purloin rate, and what is it?
# 16. What percentage of successful bugs are walking, rather than standing bugs?
# 17. What percentage of the time do spies start with drinks?
# 18. Rank the order of fingerprint sources from most to least common.
# 19. In games where Fingerprint was completed, how many involved at least one successful difficult?
# 20. What's the average time it takes for the spy to assume control?
# 21. In how many games did the spy take control instantly?
# 22. Who has the longest average time to take control (minimum 10 games)?
# 23. Who has the shortest average time to take control (minimum 10 games)?
# 24. What's the longest no-control in any of the season 4 or season 5 Championship, Hazard, or Promotion matches?
# 25. Which character has the highest win rate in Diamond?

# 26. When a banana bread comes off over 90 seconds into a game, real or fake, what percentage of the time does a
#     shot take place within 10 seconds?

# 27. How many overtime games have there been in the last two seasons?
# 28. What percentage of those overtime games did the spies win?
# 29. Which spy has reached overtime the most the past two seasons?
# 30. What percentage of microfilm transfers are action-test based rather than direct?
# 31. Which venue has the highest direct microfilm transfer rate?
# 32. Which competitive venue is the only one with a higher action test microfilm rate than a direct microfilm rate?

# 33. How many times in the last two seasons has someone started a fake Contact only to have it turn real because the
#     Double Agent entered after it began?

# 34. On which venue did fake-Contact-into-real occur the most frequently?
# 35. Of the 16 players who had a fake Contact turn into a real, which player did it the most?

# 36. What's the most common final mission? NOTE: this question is literal. It counts the final mission completed in
#     the replay, regardless of outcome or whether it leads to countdown.

# 37. What's the most common hard tell final mission? NOTE: this question is literal. It counts the final hard tell
#     mission completed in the replay, regardless of outcome or whether it leads to countdown.

# 38. What's the most common hard tell mission used to reach mission win countdown?
# 39. What's the most common final mission in games that reach countdown, as a percentage of games where it is active?
# 40. What's the least common final mission in games that reach countdown, as a percentage of games where it is active?

# 41. Which sniper has shot the spies for flirt completion the most, excluding Balcony? NOTE: this means the spy has
#     finished Seduce to trigger countdown, but is shot before the countdown is completed.

# 42. Which venue has the highest number of games where the spy completes Swap, but not Inspect? NOTE: both this
#     answer and the following answer are based on all five SCL seasons, totaling 14,186 games.

# 43. Which venue is more likely to see a completed Swap without completed Inspects: Ballroom, or Library?
# 44. In what percentage of games where Seduce is active does a spy make some flirt progress?
# 45. When a spy makes flirt progress, how often do they complete Seduce?
