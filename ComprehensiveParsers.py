from Constants.EventGroups import *


def all_bug_info(game):
    if "Bug" not in game.missions_selected:
        return
    bugs = []
    bug_type = ""
    planting = False
    in_convo = False
    transit = False
    for event in game.timeline:
        pass
        if event == "bugged ambassador while walking." or event == "bugged ambassador while standing.":
            bugs.append({
                "time": event.time,
                "type": bug_type,
                "success": True
            })
            return bugs
        elif event == "spy enters conversation.":
            if transit or bug_type == "Exit":
                bug_type = "Twitch"
            elif planting:
                bug_type = "Entry"
            in_convo = True
        elif event == "spy leaves conversation.":
            if transit or bug_type == "Entry":
                bug_type = "Twitch"
            elif planting:
                bug_type = "Exit"
            in_convo = False
        elif event == "begin planting bug while walking.":
            planting = True
            # if holding_case:
            #     bug_type = "Briefcase"
            if in_convo:
                bug_type = "Reverse"
            else:
                bug_type = "Walking"
        elif event == "begin planting bug while standing.":
            planting = True
            bug_type = "Standing"
        elif event == "bug transitioned from standing to walking.":
            transit = True
        elif event == "failed planting bug while walking.":
            bugs.append({
                "time": event.time,
                "type": bug_type,
                "success": False
            })
            planting, transit = False, False
            bug_type = ""
        # elif event.desc in drink_accepts:
        #     holding_left = "Drink"
        # elif event.desc in drink_finishes:
        #     holding_left = None
        # elif event == "get book from bookcase.":
        #     holding_left = "Book"
        # elif event == "put book in bookcase.":
        #     holding_left = None
        # elif event == "spy picks up briefcase.":
        #     holding_case = True
        # elif event == "spy puts down briefcase." or event == "spy returns briefcase.":
        #     holding_case = False
    return bugs


def shot_details(game):
    if game.cast.shot is None:
        return
    finish_ts = 0
    for event in game.timeline[::-1]:
        if "GameEnd" in event.categories:
            finish_ts = event.time
        elif event == "took shot.":
            return {
                "time": event.time,
                "shot": game.cast.shot.name[-1],
                # "role": game.cast.shot.role,  # role is redundant with cast_info
                "latency": round(finish_ts - event.time, 1),
            }


def all_cast_info(game):
    return {
        "Spy": game.cast.spy.name[-1],
        "SeductionTarget": game.cast.seduction_target.name[-1] if game.cast.seduction_target is not None else None,
        "Ambassador": game.cast.ambassador.name[-1],
        "DoubleAgent": game.cast.double_agent.name[-1],
        "SuspectedDoubleAgent": [x.name[-1] for x in game.cast.suspected_agents],
        "Civilian": [x.name[-1] for x in game.cast.civilians]
    }


__intermediate = {
    "action triggered: bug ambassador",
    "spy enters conversation.",
    "spy picks up briefcase.",
    "watch checked.",
    "read book.",
}


def all_book_info(game):
    books = []
    book_color = None
    grab_time = 0
    transfer = None
    taken_away = False
    for event in game.timeline:
        if event == "get book from bookcase.":
            book_color = event.held_book
            grab_time = event.time
        elif event.mission == "Transfer" and event.action_test is not None:
            transfer = {
                "time": event.time,
                "action_test": event.action_test,
            }
        elif book_color is not None and event in __intermediate:
            taken_away = True
        elif event == "put book in bookcase.":
            if event.bookshelf != book_color:
                taken_away = True
            books.append({
                "grab_time": grab_time,
                "source": book_color,
                "transfer": transfer,
                "taken_away": taken_away,
                "destination": event.bookshelf,
                "return_time": event.time
            })
            book_color = None
            grab_time = 0
            transfer = None
            taken_away = False
        elif book_color is not None and "GameEnd" in event.categories:
            books.append({
                "grab_time": grab_time,
                "source": book_color,
                "transfer": transfer,
                "taken_away": taken_away,
                "destination": None,
                "return_time": None
            })
    return books


__printed = {
    "fingerprinted book.",
    "fingerprinted briefcase.",
    "fingerprinted cupcake.",
    "fingerprinted drink.",
    "fingerprinted statue.",
    "fingerprinting failed"
}


def all_fingerprints(game):
    if "Fingerprint" not in game.missions_selected:
        return
    prints = []
    item, last_atr = None, None
    for event in game.timeline:
        if event in fingerprint_starts:
            item = fingerprint_starts[event]
        elif event.mission == "Fingerprint" and event.action_test is not None:
            last_atr = event.action_test
        elif event in __printed:
            prints.append({
                "time": event.time,
                "object": item,
                "action_test": last_atr,
            })
            item, last_atr = None, None
    return prints


__inspected = {
    "held statue inspected.": "inspect_held",
    "left statue inspected.": "inspect_left",
    "right statue inspected.": "inspect_right"
}


def all_statue_info(game):
    if game.venue.statues == 0:
        return
    # if game.venue.name == "Redwoods":  # TODO include book-inspects here rather than the book descriptors
    #     return {"uh oh": "this is a redwoods game"}
    statues = []
    statue = {
        "pickup_time": None,
        "inspect_left": None,
        "inspect_held": None,
        "inspect_right": None,
        "swap": None,
        "putback_time": None
    }
    last_atr = None
    for event in game.timeline:
        if event == "picked up statue.":
            statue["pickup_time"] = event.time
        elif event.mission == "Inspect" and event.action_test is not None:
            last_atr = event.action_test
        elif event.mission == "Swap" and event.action_test is not None:
            statue["swap"] = {
                "action_test": event.action_test,
                "swapper": None,
                "swap_time": None,
            }
        elif event in __inspected:
            statue[__inspected[event]] = last_atr
        # elif event == "held statue inspected.":
        #     statue["inspect_held"] = last_atr
        # elif event == "left statue inspected.":
        #     statue["inspect_left"] = last_atr
        # elif event == "right statue inspected.":
        #     statue["inspect_right"] = last_atr
        elif event == "statue swapped.":
            if event.character is None:
                statue["swap"]["swapper"] = game.cast.spy.name[-1]
                statue["swap"]["swap_time"] = event.time
            else:
                for pickup in statues:
                    if pickup["swap"] is not None:
                        pickup["swap"]["swapper"] = event.character.name[-1]
                        pickup["swap"]["swap_time"] = event.time
                        break
        elif event == "put back statue." or event == "dropped statue.":
            # clanks are treated the same as a normal statue putback
            statue["putback_time"] = event.time
            statues.append(statue)
            statue = {
                "pickup_time": None,
                "inspect_left": None,
                "inspect_held": None,
                "inspect_right": None,
                "swap": None,
                "putback_time": None
            }
        elif "GameEnd" in event.categories and statue["pickup_time"] is not None:
            statues.append(statue)
    return statues


def all_seduce_info(game):
    if "Seduce" not in game.missions_selected:
        return  # for the few games with Seduce off
    flirts = []
    last_atr = None
    for event in game.timeline:
        if event.mission == "Seduce" and event.action_test is not None:
            last_atr = event.action_test
        elif event == "failed flirt with seduction target.":
            flirts.append({
                "flirt_time": event.time,
                "action_test": last_atr,
                "percent": 0 if len(flirts) == 0 else flirts[-1]["percent"],
                "cooldown_time": event.time
            })
        elif "flirt with seduction target" in event:
            percent = int(event.desc.split(": ")[1][0:-1])
            flirts.append({
                "flirt_time": event.time,  # TODO this time should be the action trigger when the talk animation begins
                "action_test": last_atr,
                "percent": percent,
                "cooldown_time": None
            })
        elif event == "flirtation cooldown expired.":
            flirts[-1]["cooldown_time"] = event.time
    return flirts


def all_contact_info(game):
    if "Contact" not in game.missions_selected:
        return  # so few games have contact disabled, this almost isn't worth it
    contacts = []
    dough = {
        "joiner": None,
        "trigger_time": 0,
        "action_test": None,
        "elapsed": 0,
        "initial": None,
        "final": None,
        "split_time": None
    }  # work the dough until it is baked
    baking = None
    enter_ts = 0
    trigger_ts = 0
    at_hit_ts = 0
    utter_ts = 0
    for event in game.timeline:
        if event.mission == "Contact" and event.action_test is not None:
            dough["action_test"] = event.action_test
            at_hit_ts = event.time
        elif event == "spy joined conversation with double agent.":
            dough["joiner"] = "Spy"
            enter_ts = event.time
        elif event == "double agent joined conversation with spy.":
            dough["joiner"] = "DoubleAgent"
            enter_ts = event.time
        elif event in {
            "spy left conversation with double agent.",
            "double agent left conversation with spy."
        } and trigger_ts == 0:
            dough["joiner"] = None
        elif event == "action triggered: contact double agent":
            baking = True
            trigger_ts = event.time
        elif event == "real banana bread started.":
            dough["initial"] = "Real"
        elif event == "fake banana bread started.":
            dough["initial"] = "Fake"
        elif event == "fake banana bread uttered.":
            baking = False
            dough["final"] = "Fake"
            utter_ts = event.time
        elif event == "banana bread uttered.":
            baking = False
            dough["final"] = "Real"
            utter_ts = event.time
        elif event == "left alone while attempting banana bread.":
            baking = False
            # TODO left alone and aborted BBs
        elif event == "banana bread aborted.":
            # end = "COUGH COUGH"
            # if dough["action_test"] == "Red":
            #     end += " COUGH"
            baking = False
        elif (  # utter_ts > 0 and
              len(contacts) > 0 and
              event == "spy leaves conversation."):
            # stay_time defaults to null in the case of the game ending with the spy in the convo
            # instead, the previous (most recent) contact is modified with the stay_time if it exists
            contacts[-1]["split_time"] = event.time
            utter_ts = 0
        if baking is False:
            dough["elapsed"] = round(event.time - at_hit_ts, 1)  # TODO needs work
            dough["wait_time"] = round(trigger_ts - enter_ts, 1)
            contacts.append(dough)
            dough = {
                "joiner": None,
                "wait_time": 0,
                "action_test": None,
                "elapsed": 0,
                "initial": None,
                "final": None,
                "split_time": None
            }  # work the dough until it is baked
            baking = None
            enter_ts = 0
            trigger_ts = 0
            at_hit_ts = 0
            utter_ts = 0
    return contacts


def all_time_info(game):
    notable_time_events = [{
        "time": 0,
        "clock": game.clock,
        "event": "game started."
    }]
    for event in game.timeline:
        if event == "45 seconds added to match.":
            notable_time_events.append({
                "time": event.time,
                "clock": event.clock + 45,
                "event": "45 seconds added to match."
            })
        elif event in {
            "missions completed. 10 second countdown.",
            "missions completed. countdown pending.",
            "overtime!",
        }:
            notable_time_events.append({
                "time": event.time,
                "clock": event.clock,
                "event": event.desc
            })
    return notable_time_events


def all_drink_info_tray(game):
    if game.venue.bar:
        return
    offers = []
    drink_offer = {
        "requested": False,
        "offer_time": 0,
        "response_time": 0,
        "accepted": False,
        "purloin": None,
    }
    for event in game.timeline:
        if event in drink_requests_tray:
            drink_offer["requested"] = True
        elif event == "waiter offered drink.":
            # print("A", event.time)
            drink_offer["offer_time"] = event.time
        elif event.mission == "Purloin" and event.action_test is not None:
            # print("B", event.time)
            drink_offer["purloin"] = {
                "action_test": event.action_test,
                "list_taker": None,
                "fade_time": None
            }
        elif event in drink_accepts:
            # print("C", event.time)
            drink_offer["accepted"] = True
            drink_offer["response_time"] = round(event.time - drink_offer["offer_time"], 1)
        elif event in drink_rejects_tray:
            # accepted = False
            drink_offer["response_time"] = round(event.time - drink_offer["offer_time"], 1)
        elif event in {"guest list purloined.", "guest list returned."}:
            # print("D", event.time)
            if drink_offer["purloin"] is not None:
                drink_offer["purloin"]["list_taker"] = event.character.name[-1]
                drink_offer["purloin"]["fade_time"] = event.time
                continue
            for prev_offer in offers[::-1]:
                if prev_offer["purloin"] is not None:
                    prev_offer["purloin"]["list_taker"] = event.character.name[-1]
                    prev_offer["purloin"]["fade_time"] = event.time
        elif event in {"waiter stopped offering cupcake.", "waiter stopped offering drink."}:
            # print("E", event.time)
            offers.append(drink_offer)
            drink_offer = {
                "requested": False,
                "offer_time": 0,
                "response_time": 0,
                "accepted": False,
                "purloin": None
            }
        # TODO elif event == "purloin guest list aborted.":
    return offers


def all_drink_info_bar(game):
    if not game.venue.bar:
        return
    offers = []
    drink_offer = {
        # "demanded": False,
        "request_time": 0,
        "queue_time": 0,
        "accepted": None,
        "purloin": None
    }
    for event in game.timeline:
        if event in drink_requests_bar:
            if drink_offer["request_time"] > 0:
                offers.append(drink_offer)
                drink_offer = {
                    # "demanded": False,
                    "request_time": 0,
                    "queue_time": 0,
                    "accepted": None,
                    "purloin": None
                }
            drink_offer["request_time"] = event.time
        # elif event in drink_demands_bar:
        #     drink_offer["demanded"] = True
        #     drink_offer["request_time"] = event.time
        elif event in drink_offers_bar:
            drink_offer["queue_time"] = round(event.time - drink_offer["request_time"], 1)
        elif event in drink_accepts_bar:
            drink_offer["accepted"] = True
        elif event in drink_rejects_bar:
            drink_offer["accepted"] = False
        elif event == "delegating purloin guest list.":
            drink_offer["purloin"] = {
                "option": "Delegated",
                "delegate": None,
                "send_time": None,
                "fade_time": None
            }
        elif event.desc.startswith("delegated purloin to "):
            if drink_offer["purloin"] is None:
                for prev_offer in offers[::-1]:
                    if prev_offer["purloin"] is not None:
                        if prev_offer["purloin"]["option"] == "Delegated":
                            prev_offer["purloin"]["delegate"] = event.character.name[-1]
                            prev_offer["purloin"]["send_time"] = event.time
                            break
                continue
            drink_offer["purloin"]["delegate"] = event.character.name[-1]
            drink_offer["purloin"]["send_time"] = event.time
        elif event == "guest list purloined.":
            if event.character.role == "Spy":
                drink_offer["purloin"] = {
                    "option": "Immediate",
                    "delegate": None,
                    "send_time": None,
                    "fade_time": event.time
                }
                offers.append(drink_offer)
                drink_offer = {
                    # "demanded": False,
                    "request_time": 0,
                    "queue_time": 0,
                    "accepted": None,
                    "purloin": None
                }
            else:
                for prev_offer in offers[::-1]:
                    if prev_offer["purloin"] is not None:
                        if prev_offer["purloin"]["option"] == "Delegated":
                            prev_offer["purloin"]["fade_time"] = event.time
                            break
        elif event == "delegated purloin timer expired.":
            offers.append(drink_offer)
            drink_offer = {
                # "demanded": False,
                "request_time": 0,
                "queue_time": 0,
                "accepted": None,
                "purloin": None
            }
    if drink_offer["request_time"] > 0:
        offers.append(drink_offer)
    # TODO still needs some work to resolve 'fade_time' entries
    return offers


__watch_checks = {
    "watch checked.",
    "action test green: check watch",
    "action test ignored: check watch",
    "action test red: check watch",
    "action test white: check watch"
}


def all_watch_info(game):
    checks = []
    for event in game.timeline:
        if event in __watch_checks:
            checks.append({
                "time": event.time,
                "action_test": event.action_test
            })
    return checks


def all_header_info(game):
    return {
        "spy": game.spy,
        "spy_username": game.spy_username,
        "sniper": game.sniper,
        "sniper_username": game.sniper_username,
        "date_played": game.date,
        "venue": game.venue.name,
        "setup": game.mode,
        "missions": {  # lists selected missions and if they are completed or not
            mission: mission in game.missions_complete for mission in game.missions_selected
        },
        "result": game.specific_win_condition
    }

def all_sips_info(game):
    sips = []
    drink_quantity = 0
    for event in game.timeline:
        if event in drink_accepts:
            drink_quantity = 3
        elif event in drink_sips:
            sips.append({
                "time": event.time,
                "sips": 1,
            })
            drink_quantity -= 1
        elif event in drink_gulps:
            sips.append({
                "time": event.time,
                "sips": drink_quantity
            })
    return sips

__non_drink_events = drink_offers | drink_requests | {
    "picked up statue.",
    "got book from bookcase.",
}

__destinations = {
    "spy enters conversation.": "Conversation",
    "watch checked.": "Window",
    "picked up statue.": "Statue",
    "put back statue.": "Statue",
    "get book from bookcase.": "Bookshelf",
    "put book in bookcase.": "Bookshelf",
    "request drink from waiter.": "Toby",
    "request cupcake from waiter.": "Toby",
    "request drink from bartender.": "Bar",
    "demand drink from bartender.": "Bar",
    "request cupcake from bartender.": "Bar",
    "demand cupcake from bartender.": "Bar",
    "spy picks up briefcase.": "Briefcase",
}

def all_spy_start_info(game):
    began_with_drink = None
    control_time = None
    destination = None
    for event in game.timeline:
        if began_with_drink is None:
            if event in drink_finishes:
                began_with_drink = True
            elif event in __non_drink_events:
                began_with_drink = False
        if event == "spy player takes control from ai.":
            # only one of these events so the 'control_time is None' is not necessary
            control_time = event.time
        if destination is None and event in __destinations:
            destination = __destinations[event]
        if (began_with_drink is not None and
            # control_time is not None and
            destination is not None):
            return {
                "take_control_time": control_time,
                "began_with_drink": began_with_drink,
                "first_destination": destination
            }
    # print(f"{game.uuid} resulted in at least one null:")
    # print(f"\ttake_control_time: {control_time}")
    # print(f"\tbegan_with_drink: {began_with_drink}")
    # print(f"\tfirst_destination: {destination}")
    # TODO investigate null began_with_drink and first_destination entries

def all_audible_info(game):
    noises = []

    def __log_noise(evt, typ):
        noises.append({
            "time": evt.time,
            "type": typ
        })
    red_tested_contact = False
    for event in game.timeline:
        if event == "action test red: contact double agent":
            red_tested_contact = True
        elif event == "purloin guest list aborted.":
            __log_noise(event, "Crash")
        elif event in {
            "action test red: check watch",
            "aborted watch check to add time."
        }:
            __log_noise(event, "Beep")
        elif event == "banana bread aborted.":
            if red_tested_contact:
                __log_noise(event, "Cough Cough Cough")
            else:  # TODO verify coughs are correct
                __log_noise(event, "Cough")
        elif red_tested_contact and event in {
            "banana bread uttered.",
            "fake banana bread uttered."
        }:
            __log_noise(event, "BB Cough")
        elif event == "dropped statue.":
            __log_noise(event, "Clank")
        # TODO include microfilm cancels
    # audibles are sparse, so this reduces unnecessary uuid redundancy
    # alternatively, include ALL audible information with normal BB and beeps --> MASSIVE redundance
    return noises if len(noises) > 0 else None





# TODO implement these json_stats:

game_info_lights = {
    "uuid": {
        "A": [],
        "B": [
            {
                "time": 0,
                "light": -1
            }
        ]
    }
}

game_info_marks = {
    "uuid": [
        {
            "time": 0,
            "char": "A",
            "mark": "Blue"
        }
    ]
}
# return None for games after Redwoods update


game_info_conversations = {
    "uuid": [
        {
            "enter_time": None,
            "talks": [
                {
                    "time": 0,
                    "type": "Innocent Talk",
                    "stopped": False  # a stop talk within 15 seconds of starting a talk
                },
                {
                    "time": 1,
                    "type": "Interrupt",
                    "stopped": False
                },
                {
                    "time": 2,
                    "type": "Flirt",  # TODO distinguish timerflirts
                    "stopped": False
                },
                {
                    "time": 3,
                    "type": "Contact",  # green contacts excluded
                    "stopped": False
                },
                {
                    "time": 4,
                    "type": "Guilty Talk",  # for covering reverse/entry bugs
                    "stopped": False
                }
            ],
            "leave_time": None,
        }
    ]
}

game_info_briefcases = {
    "uuid": [
        {
            "pickup_time": 0,
            "returned": False,
            "return_time": 0,
        }
    ]
}

game_info_psv = {
    "uuid": [
        {
            "time": 0,  # time of PSV
            "crowd_time": None  # out of convo PSV
        },
        {
            "time": 1,
            "crowd_time": 7.6  # spy crowded amba
        },
        {
            "time": 2,
            "crowd_time": 3.4  # spy overcrowded amba
        },
        {
            "time": 3,
            "crowd_time": 7.6  # amba crowded spy
        }  # how did I determine the different times before? look back at that
    ]
}

# def all_psv_info(game):
#
#     for event in game.timeline:


game_info_action_tests = {
    "uuid": [
        {
            "trigger": 0,
            "mission": "Contact",
            "result": "Green",
            "hit": 1.2,
        }
    ]
}

