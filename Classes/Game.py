from Classes.Venue import Venues
from Classes.Event import Event, Character
from Classes.Match import Match


class Game:
    def __init__(self, jason):
        self.spy = jason["spy"]
        self.sniper = jason["sniper"]
        self.spy_username = jason["spy_username"]
        self.sniper_username = jason["sniper_username"]
        self.uuid = jason["uuid"]
        self.date = jason["start_time"]

        # this date is when the terrace update patch notes were published on steam
        if jason["venue"] == "Terrace" and jason["start_time"] < "2018-06-05T08:05:00":
            self.venue = Venues["Terrace_old"]
        else:
            self.venue = Venues[jason["venue"]]

        self.mode = jason["game_type"]
        self.guests = jason["guest_count"]
        self.clock = jason["start_clock_seconds"]
        if self.clock is None:  # some values are none, so this fills those gaps
            self.clock = jason["timeline"][0]["time"]//1
        self.missions_selected = jason["selected_missions"]

        self.match = Match(jason)
        self.specific_win_condition, self.general_win_condition = jason["win_type"]

        self.cast = Cast()
        self.timeline = []
        self.sniper_lights = []
        self.missions_complete = []
        self.missions_progress = set()
        self.time_added = 0

        in_convo = None
        during_countdown = False
        during_overtime = False
        for json_event in jason["timeline"]:
            # counterintuitive, but the initial value must be the opposite of the event itself
            if json_event["event"] == "spy enters conversation.":
                in_convo = False
                break
            elif json_event["event"] == "spy leaves conversation.":
                in_convo = True
                break

        for json_event in jason["timeline"]:
            if json_event["event"] == "spy enters conversation.":
                in_convo = True
            elif json_event["event"] == "spy leaves conversation.":
                in_convo = False
            elif json_event["event"] == "missions completed. 10 second countdown.":
                during_countdown = True
            elif json_event["event"] == "overtime!":
                during_overtime = True
            elif json_event["event"] == "45 seconds added to match.":
                self.time_added += 45

            if ("MissionSelected" in json_event["category"] or
                    "MissionEnabled" in json_event["category"] or
                    json_event["event"] == "begin flirtation with seduction target."):
                continue

            if "Cast" in json_event["category"]:
                chara = Character(name=json_event["cast_name"][0],
                                  role=json_event["role"][0])
                self.cast.invite(chara)
            else:
                event = Event(
                    json_event,
                    in_convo=in_convo,
                    during_mwc=during_countdown,
                    during_ot=during_overtime,
                )
                self.timeline.append(event)
                if "MissionComplete" in json_event["category"]:
                    self.missions_complete.append(event.mission)
                elif ("MissionPartial" in json_event["category"] or
                      "ActionTriggered" in json_event["category"]):
                    self.missions_progress.add(event.mission)
                elif "SniperLights" in json_event["category"]:
                    self.sniper_lights.append(event)
                elif event == "guest list purloined." and event.character.role != "Spy":
                    self.cast.invite(event.character, "Delegate")
                elif event == "statue swapped." and event.character.role != "Spy":
                    self.cast.invite(event.character, "Swapper")
                elif "SniperShot" in json_event["category"]:
                    self.cast.invite(event.character, "Shot")

        self.reaches_mwc = len(self.missions_complete) >= int(self.mode[1])

        # TODO patch
        # if self.guests is None:
        #     self.guests = len(self.cast)

    def __str__(self):
        result = "Match:\t" + str(self.match) + " (" + self.date + ")"
        result += "\nVenue:\t" + str(self.venue) + " " + self.mode + ", " + str(len(self.cast)) + " guests, " + str(self.clock) + "s"
        result += "\nResult:\t" + self.specific_win_condition + " (" + self.general_win_condition + ")"
        result += "\nMis'ns:\t" + ", ".join(self.missions_complete)
        result += "\nCast:"
        for mem in self.cast:
            result += "\n\t\t" + str(mem)
        result += "\nEvents:"
        for event in self.timeline:
            result += "\n\t\t" + str(event)
        result += "\nLights:"
        # for event in self.sniper_lights:
        #     result += "\n\t\t" + str(event)
        return result

    def get_role_of_character(self, character):
        for chara in self.cast:
            if chara.name == character:
                return chara.role
        return "Absent"

    def get_most_recent_light_for(self, name="", role=""):
        for event in self.sniper_lights[::-1]:
            chara = event.character
            if chara.name == name or chara.role == role:
                return event.desc
        if role == "Spy":
            return "marked spy default suspicion."
        return "marked default suspicion."


class Cast:
    def __init__(self):
        self.__cast_list = set()
        self.spy = None
        self.seduction_target = None
        self.ambassador = None
        self.double_agent = None
        self.suspected_agents = set()
        self.civilians = set()
        self.delegate = None  # only the initial list taker, no return/successive take BS
        self.swapper = None
        self.shot = None

    def __iter__(self):
        return iter(self.__cast_list)

    def __len__(self):
        return len(self.__cast_list)

    def invite(self, chara, override_role=None):
        self.__cast_list.add(chara)
        if override_role == "Delegate":
            self.delegate = chara
        elif override_role == "Swapper":
            self.swapper = chara
        elif override_role == "Shot":
            self.shot = chara
        # mututally exclusive assignments from separate events
        elif chara.role == "Spy":
            self.spy = chara
        elif chara.role == "SeductionTarget":
            self.seduction_target = chara
        elif chara.role == "Ambassador":
            self.ambassador = chara
        elif chara.role == "DoubleAgent":
            self.double_agent = chara
        elif chara.role == "SuspectedDoubleAgent":
            self.suspected_agents.add(chara)
        else:
            self.civilians.add(chara)


# problem events

# 183.7 - action test green: purloin guest list ()
# 183.7 - guest list purloin pending. (Mr. K (Spy))
# 183.7 - rejected drink from waiter. (Mr. K (Spy))
# 183.7 - waiter stopped offering drink. (Mr. K (Spy))

# 19.4 - rejected drink from waiter. (Mr. K (Spy))
# 19.4 - waiter stopped offering drink. (Mr. K (Spy))
