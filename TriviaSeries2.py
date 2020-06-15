from Classes.StatLoader import StatLoader
from Reports import *
loader = StatLoader()

game_heads = loader.get_stat("json_outputs/game_info/header.json")
game_casts = loader.get_stat("json_outputs/game_info/cast.json")
game_flirts = loader.get_stat("json_outputs/game_info/seduce.json")
events = loader.get_stat("json_outputs/events_matches.json")

# Rarely, Spies are able to complete their missions completely undetected by the Sniper.
# . In how many games did the Spy complete missions while retaining their default, neutral light?
#    (Note: games where the spy is LL/HL at all do not count)
# . Which Spy has achieved this the most?



# In order to Contact the Double Agent, the Spy must be in a conversation with the Double Agent.
# . How often does the Double Agent join the Spy leading up to a real Banana Bread? (Compared to the Spy joining the DA)



# The Ambassador walks away from crowded positions if their personal space is violated for 7.5 seconds.
# . What percentage of the time has the Ambassador joined the spy in a conversation position that violates their
# personal space? (Cinoared to the Spy crowding the Ambassador)



# While at windows, the Spy can check their watch innocently or to add time to the clock.
# . What percentage of spy watch checks are time adds?



# In the waning moments of many time-out games, spies try to hastily check their watch to add time, but fail to do so
# before the clock expires.
# . Which characters most commonly fail to add time before the clock expires? (Top 3, 1pt each)
# . Which character - other than Mr. S, of course, with his rapid watch check - has never failed to add time before
#    the clock expires?


game_sips = loader.get_stat("json_outputs/game_info/sips.json")
# Every drink served by Toby is filled with 3 sips of the guests' drink of choice.
# . On average, how many sips do spies take of their drinks?


# Some snipers habitually high/low-light their entire cast at the beginning of the game. Some snipers do this
# with great efficiency.
# . What is the fastest time a Sniper has lit their cast?
# . Which sniper has done this the fastest, and on which venue do they hold the record?
# . Of games where the Sniper lights their cast within the first minute, what is the average time they took do to so?
# . Of games where the Sniper lights their cast within the first minute, AND Mr. S is one of those cast members,
#     what is the average time they took to do so?


# Hitting a green test on a Swap or tray Purloin will cause that mission to go into a pending state.
# . What is the longest time that a Purloin has been pending for?
# . What is the longest time that a Swap has been pending for?
# . In how many games did the spy complete another final mission than the one which caused pending overtime?
# . Which mission was the most commonly completed during pending overtime (other than purloin/swap)?


# Hitting a red test Contact causes the Spy to cough after saying Banana Bread, often prompting a shot.
# . How often does a shot come off within 10 seconds following a BB cough (regardless of whether or not the shot is
#     correct)?


# When attempting to Contact the Double Agent or flirt with the Seduction Target, they sometimes decide to walk away
# from the Spy before the action is completed, resulting in a 'sunshine'.
# . What percentage of the time does the spy get sunshined?



# Action Test Microfilm Transfer if commonly viewed to be very difficult for the spy to survive, with even its green
# result causing an instant shot, if seen.
# . Which stage of the indirect Microfilm Transfer are spies more commonly shot (within 10 seconds) for?
# . What percentage of the time is microfilm transferred while standing in an empty conversation?




# Some Snipers lowlight guests for AI-like behavior, and some spies counterplay this by attempting to get lowlit:
# . When the Spy is lowlit, which hard tell most often causes the Sniper to realize their mistake and shoot the spy
#     within 10 seconds?
# . In how many games was the Spy lowlit while under AI control?
# . Of those games, what percent did the Spy go on to win?




# Following pwndnoob's Spooky Invitational, the community rallied behind Moderne 4/8, resulting in its change for SCL 6.
# . What percent of games played on Moderne 5/8 would have resulted differently had they been played as 4/8?
#     (ie. The spy survives for 10 seconds after their 4th mission completion)
#     (Players would obviously make different decisions if their original game were a different setup, but this is a
#     data-driven hypothetical)



# A timerflirt occurs when the Spy waits out the full 45 second flirt cooldown in conversation with their Seduction
# Target.
# . What percent of flirts are timerflirts?
# . Which spies have the highest timerflirt rate?


# There are many intricate varieties of Bug, with several classifications: Standing, Reverse, Walking, Exit, Entry, and
# Twitch Bugs
# . What kind of bug is most commonly failed when attempted?







# . Which role is most commonly delegated to Purloin on bar venues?
# . How often does the Spy delegate to a Suspected Double Agent?


# . What percent of the time does the Spy sip at the bar (within 5 seconds of accepting their drink)?
# . What is the longest time the Spy has queued to receive a drink at the bar? On which venue did this occur?


# "The Book Cook Cookbook"
# A direct transfer occurs when the Spy returns a book to the incorrect shelf, transferring the microfilm inside. Spies
# tend to hold onto or 'cook' their books for a while before going for the return.
# . What is the average time the Spy cooked their book leading up to a successful direct transfer?
#   (ie they were not shot within 10s)
# . What is the average time the Spy cooked their book leading up to an unsuccessful direct transfer?
#   (ie they were shot within 10s)


# . What is the average flirt percentage across all games with flirt selected?
all_flirts = Dataset([game_flirts[g]["total"] for g in game_flirts])
print(all_flirts.stats_report())

# . Which Sniper induces the lowest flirt percentage from their opponents? (with at least 10 games)
sniper_flirt_grades = {}
for g in game_flirts:
    sni = game_heads[g]["sniper"]
    if sni in sniper_flirt_grades:
        sniper_flirt_grades[sni].append(game_flirts[g]["total"])
    else:
        sniper_flirt_grades[sni] = [game_flirts[g]["total"]]
for sni in sniper_flirt_grades:
    vals = sniper_flirt_grades[sni]
    if len(vals) < 10:
        continue
    grade = Dataset(vals)
    avg = grade.average()
    print(f"{sni} flirt report:\t{avg} ({number_to_grade(avg)})")

# . Which character has been seduced most frequently when selected as the Seduction Target?
# TODO normalize
seduced_targets = Counter([
    game_casts[g]["SeductionTarget"] for g in game_heads
    # Seduce is a mission and seduce was completed
    if "Seduce" in game_heads[g]["missions"] and game_heads[g]["missions"]["Seduce"]
])
print(seduced_targets.most_common())

# . What percent of matches have had the Queen + General flirt pair?
gq_pair_games = {g for g in game_casts if f"{game_casts[g]['Spy']}{game_casts[g]['SeductionTarget']}" in {"GJ", "JG"}}
gq_spies = Counter()
match_count = 0
for event in events:
    for division in events[event]:
        matches = events[event][division]
        match_count += len(matches)
        for match in matches:
            for game in match["games"]:
                if game in gq_pair_games:
                    gq_spies[game_heads[game]["spy"]] += 1
print(len(gq_pair_games))
print(f"match count: {match_count}")  # TODO if the percent isn't interesting, ask about match count
print(gq_spies.most_common())

# . Which has the highest spy win-rate:
#   a) White purloin in conversation
#   b) White purloin out of conversation
#   c) Green purloin in conversation
#   d) Green purloin out of conversation


# . What is the average number of lowlights taken in the 10 seconds following a Banana Bread?
# . What is the difference between the number of lowlights between Red and other BBs?

# . What is the greatest number of lowlights taken following a mission-completing Banana Bread and a correct shot?
#   And which player achieved this?

# . How often does the Spy perform a Banana Split, leaving conversation within 1 second of uttering Banana Bread?

# . How many times have Spies began talking to mitigate the arm snapback animation of a Bug?
# . What is the average number of innocent talk animations the Spy does per game?


# . How often do Spies complete their inspects in 1 statue visit?


# TODO trivia: coughs/BB with briefcase
# TODO purloin attempts without a request (checker purloins)

