
class Game:

    def __init__(self, jason):
        self.spy = jason["spy"]
        self.sniper = jason["sniper"]
        self.__spy = jason["spy_username"]
        self.__sniper = jason["sniper_username"]
        self.uuid = jason["uuid"]
        self.date = jason["start_time"]

        self.venue = jason["venue"]
        self.mode = jason["game_type"]
        self.guests = jason["guest_count"]
        self.clock = jason["start_clock_seconds"]

        self.match = Match(jason)
        self.specific_win_condition, self.general_win_condition = jason["win_type"]

        self.missions_selected = jason["selected_missions"]
        self.missions_complete = []
        # self.mission_progress = {}  # TODO mission_progress with same capability as missions_complete

        self.cast = []
        self.spy_timeline = []
        self.sniper_lights = []
        for event in jason["timeline"]:
            if "Cast" in event["category"]:
                self.cast.append(Character(name=event["cast_name"][0],
                                           role=event["role"][0]))
            elif "MissionSelected" in event["category"] \
                    or "MissionEnabled" in event["category"]:
                continue  # the mission selected/enabled events are useless
            elif event["event"] in unwanted_events:
                continue
            elif "SniperLights" in event["category"]:
                self.sniper_lights.append(TimelineEvent(event))
            elif "MissionComplete" in event["category"]:
                self.missions_complete.append(event["mission"])
                self.spy_timeline.append(TimelineEvent(event))
            else:
                self.spy_timeline.append(TimelineEvent(event))

        self.reaches_mwc = len(self.missions_complete) >= int(self.mode[1])

        # TODO self.shot: Character = ...

    def __str__(self):
        result = "Match:\t" + str(self.match) + " (" + self.date + ")"
        result += "\nVenue:\t" + self.venue + " " + self.mode + ", " + str(len(self.cast)) + " guests, " + str(self.clock) + "s"
        result += "\nResult:\t" + self.specific_win_condition + " (" + self.general_win_condition + ")"
        result += "\nMis'ns:\t" + ", ".join(self.missions_complete)
        result += "\nCast:"
        for mem in self.cast:
            result += "\n\t\t" + str(mem)
        result += "\nEvents:"
        for event in self.spy_timeline:
            result += "\n\t\t" + str(event)
        result += "\nLights:"
        for event in self.sniper_lights:
            result += "\n\t\t" + str(event)
        return result

    # TODO - how to incorporate both/only one timeline
    # def get_events_in_range(self, lb, ub):
    #     return

    def get_role_of_character(self, character):
        for chara in self.cast:
            if chara.name == character:
                return chara.role
        return "Absent"

    def get_characters_in_role(self, role):
        lc = [chara.name for chara in self.cast if chara.role == role]
        # return the only character, multiple characters, or no characters
        return lc[0] if len(lc) == 1 else lc


unwanted_events = {
    "begin flirtation with seduction target.",
    "game started.",
}


class TimelineEvent:

    def __init__(self, event):
        self.time = event["elapsed_time"]
        self.desc = event["event"]
        self.actor = event["actor"]
        self.clock = event["time"]
        self.mission = event["mission"]
        self.action_test = event["action_test"]
        self.categories = event["category"]

        self.characters = [Character(name=event["cast_name"][i],
                                     role=event["role"][i]) for i in range(len(event["role"]))]

        bks = event["books"]
        if len(bks) == 2:
            self.held_book, self.bookshelf = bks

    def get_flirt_percent(self):
        if "flirt with seduction target: " == self.desc[0:30]:
            percent = self.desc.split(": ")[1]
            return int(percent[0:len(percent)-1])

    def __str__(self):
        return str(self.time) + " - " + self.desc  # + " (" + str(self.character) + ")"

    def __eq__(self, other):
        return self.desc == other


class Character:

    def __init__(self, name, role):
        self.name = name
        self.role = role

    def __str__(self):
        return self.name + " (" + self.role + ")"


class Match:

    def __init__(self, jason):
        self.event = jason["event"]
        div = jason["division"]
        self.division = "" if div is None else div if len(div) > 1 else "Group "+div
        self.week = jason["week"]
        self.playerA, self.playerB = sorted([jason["spy"], jason["sniper"]])

    def __str__(self):
        return " ".join([self.event, self.division, "Week", str(self.week), self.playerA, "vs", self.playerB])


# problem events

# 183.7 - action test green: purloin guest list ()
# 183.7 - guest list purloin pending. (Mr. K (Spy))
# 183.7 - rejected drink from waiter. (Mr. K (Spy))
# 183.7 - waiter stopped offering drink. (Mr. K (Spy))

# 19.4 - rejected drink from waiter. (Mr. K (Spy))
# 19.4 - waiter stopped offering drink. (Mr. K (Spy))
