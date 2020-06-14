from Constants.EventGroups import *


class Event:
    def __init__(self, json_event, **kwargs):
        self.time = json_event["elapsed_time"]
        self.clock = json_event["time"]

        self.desc = json_event["event"]
        self.mission = json_event["mission"]
        self.action_test = json_event["action_test"] if json_event["action_test"] != "NoAT" else None
        # TODO trivia: coughs/BB with briefcase
        self.in_conversation = kwargs["in_convo"]
        self.during_countdown = kwargs["during_mwc"]
        self.during_overtime = kwargs["during_ot"]

        if self.desc in actor_assignments:
            self.actor = actor_assignments[self.desc]
        elif (self.desc == "statue swapped." or
              self.desc == "guest list purloined." or
              self.desc == "guest list returned.") and len(json_event["role"]) > 0:
            self.actor = json_event["role"][0]
        else:
            self.actor = json_event["actor"].capitalize()

        self.character = (
            Character(name=json_event["cast_name"][0], role=json_event["role"][0])
            if len(json_event["role"]) > 0 else None  # TODO replace None with the actor, if applicable
        )   # TODO purloin attempts without a request (checker purloins)
        # TODO pull character reference from the cast to reduce redundant data

        bks = json_event["books"]
        if len(bks) == 2:
            self.held_book, self.bookshelf = bks
        elif len(bks) == 1:
            self.held_book, self.bookshelf = bks[0], None
        else:
            self.held_book, self.bookshelf = None, None
        # self.held_book, self.bookshelf =   # (bks[0], bks[1]) if len(bks) == 2 else (None, None)

    def __str__(self):
        return f"{self.clock} ({self.time})\t{self.character}({self.actor}) - {self.desc}"
        # f"\n\ti_c? {self.in_conversation}\tmwc? {self.during_countdown}\tbook {self.held_book},{self.bookshelf}"

    # Optional syntax to reduce certain operations by 5 characters
    def __eq__(self, other):
        # allows for exact event matching:      event == "event."
        # alternatively,                        event.desc == "event."
        if type(other) == str:
            return self.desc == other
        # allows event matching from a list:    event == ["ev1", "ev2", "ev3"]
        # alternatively,                        event.desc in ["ev1", "ev2", "ev3"]
        if type(other) == list or type(other) == set or type(other) == tuple:
            for x in other:
                if self.desc == x:
                    return True
        # returns false once the other cases didn't pass
        return False

    def __contains__(self, item):
        # allows for event containing a match:  "keyword" in event
        # alternatively,                        "keyword" in event.desc
        return item in self.desc

    def __hash__(self):
        return hash(self.desc)


# TODO cast data structure:
#  Name, Role, Lights->
#  ex:
#  Ms. B, Spy, Default->Lowlight->Neutral->Highlight->Shot
#  Ms. F, Ambassador, Default->Highlight

class Character:
    def __init__(self, name, role):
        self.name = name
        self.role = role

    def __str__(self):
        return f"{self.name} ({self.role})"

    def __hash__(self):
        return hash((self.name, self.role))

    def __lt__(self, other):
        if type(other) == Character:
            return self.name[-1] < other.name[-1]
        raise TypeError

    def __eq__(self, other):
        return self.name == other.name
