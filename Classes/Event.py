from EventGroups import *


class Event:
    def __init__(self, json_event, **kwargs):
        self.time = round(json_event["elapsed_time"], 1)  # some of the json_games contain unrounded floats :(
        self.clock = round(json_event["time"], 1)

        self.desc = json_event["event"]
        # TODO retire .action_test
        self.action_test = json_event["action_test"] if json_event["action_test"] != "NoAT" else None
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
        )

        self.held_book, self.bookshelf = None, None
        bks = json_event["books"]
        if len(bks) == 2:
            self.held_book, self.bookshelf = bks[0], bks[1]
        elif len(bks) == 1:
            self.held_book = bks[0]

    def __str__(self):
        return (
            f"{self.clock} ({self.time})".ljust(14) +
            f" - {self.desc}".ljust(50) +
            f" - {self.character}"
            # f"\t{self.bookshelf} {self.held_book}"
            # f"\n\t{'out of' if not self.in_conversation else 'in'} conversation"
            # f"\n\t{'out of' if not self.during_countdown else 'in'} mission countdown"
            # f"\n\t{'out of' if not self.during_overtime else 'in'} overtime"
        )

    def __eq__(self, other):
        # allows for exact event matching:      event == "event."
        # alternatively,                        event.desc == "event."
        if type(other) == str:
            return self.desc == other
        return False

    def __contains__(self, item):
        # allows for event containing a match:  "keyword" in event
        # alternatively,                        "keyword" in event.desc
        return item in self.desc

    def __hash__(self):
        # allows event matching from a list:    event in ["ev1", "ev2", "ev3"]
        # alternatively,                        event.desc in ["ev1", "ev2", "ev3"]
        return hash(self.desc)

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
