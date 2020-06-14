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
    shot_time = None
    finish_ts = 0
    mission_complete_time = None
    for event in game.timeline[::-1]:
        if event == "sniper shot too late for sync.":
            print(f"\t{game.uuid}")
        if event in game_ends:
            finish_ts = event.time
        elif event == "took shot.":
            shot_time = event.time
            if not game.reaches_mwc:
                break
        elif mission_complete_time is None and event in game_states_missions_complete:
            mission_complete_time = event.time
            if shot_time is not None:
                break
    return {
        "time": shot_time,
        "chara": game.cast.shot.name[-1],
        "latency": round(finish_ts - shot_time, 1),
        "countdown": round(10 - shot_time + mission_complete_time, 1) if mission_complete_time is not None else None
        # "role": game.cast.shot.role,  # role is redundant with cast_info
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
    if game.venue.bookshelves == 0:
        return
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
                "test": event.action_test,
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
        elif book_color is not None and event in game_ends:
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
                "test": last_atr,
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
                "test": event.action_test,
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
        elif statue["pickup_time"] is not None and event in game_ends:
            statues.append(statue)
    return statues


def all_seduce_info(game):
    if "Seduce" not in game.missions_selected:
        return  # for the few games with Seduce off
    flirts = []
    progress = 0
    talk_time = 0
    last_atr = None
    for event in game.timeline:
        if event == "action triggered: seduce target":
            talk_time = event.time
        elif event.mission == "Seduce" and event.action_test is not None:
            last_atr = event.action_test
        elif event in {
            "failed flirt with seduction target.",
            "seduction canceled.",
        }:
            flirts.append({
                "time": talk_time,
                "test": last_atr,
                "gain": 0,  # 0 if len(flirts) == 0 else flirts[-1]["percent"],
                "cooldown_time": event.time
            })
        elif event in flirt_percents:
            # percent = int(event.desc.split(": ")[1][0:-1])
            percent = flirt_percents[event]
            flirts.append({
                "time": talk_time,
                "test": last_atr,
                "gain": percent - progress,
                "cooldown_time": None
            })
            progress = percent
        elif event == "flirtation cooldown expired.":
            flirts[-1]["cooldown_time"] = event.time
        elif event == "target seduced.":
            break
    return {
        "total": progress,
        "flirts": flirts
    }


def all_contact_info(game):
    if "Contact" not in game.missions_selected:
        return  # so few games have contact disabled, this almost isn't worth it
    contacts = []
    dough = {
        "joiner": None,
        "test": None,
        "trigger_time": 0,
        "utter_time": 0,
        "initial": None,
        "final": None,
        "split_time": None
    }  # work the dough until it is baked
    baking = None
    for event in game.timeline:
        if event in action_test_contact:
            dough["test"] = event.action_test
        elif event == "spy joined conversation with double agent.":
            dough["joiner"] = "Spy"
        elif event == "double agent joined conversation with spy.":
            dough["joiner"] = "DoubleAgent"
        elif event in {"spy left conversation with double agent.", "double agent left conversation with spy."}:
            dough["joiner"] = None
        elif event == "action triggered: contact double agent":
            baking = True
            dough["trigger_time"] = event.time
        elif event == "real banana bread started.":
            dough["initial"] = "Real"
        elif event == "fake banana bread started.":
            dough["initial"] = "Fake"
        elif event == "fake banana bread uttered.":
            baking = False
            dough["final"] = "Fake"
            dough["utter_time"] = event.time
        elif event == "banana bread uttered.":
            baking = False
            dough["final"] = "Real"
            dough["utter_time"] = event.time
        elif event in {"banana bread aborted.", "left alone while attempting banana bread."}:
            baking = False
        elif len(contacts) > 0 and event == "spy leaves conversation.":
            contacts[-1]["split_time"] = event.time

        if baking is False:
            contacts.append(dough)
            dough = {
                "joiner": None,
                "test": None,
                "trigger_time": 0,
                "utter_time": 0,
                "initial": None,
                "final": None,
                "split_time": None
            }  # work the dough until it is baked
            baking = None
    return contacts


def all_time_info(game):
    notable_time_events = []
    green_time_add = False
    green_time_add_expire_time = None
    time_added = 0
    pending = False
    for event in game.timeline:
        if event == "action test green: check watch":
            green_time_add = True
        elif event == "45 seconds added to match.":
            time_added += 45
            if green_time_add:
                if green_time_add_expire_time is None:
                    green_time_add_expire_time = event.time
                green_time_add_expire_time += 90
            notable_time_events.append({
                "time": event.time,
                "clock": event.clock + 45,
                "event": "45 seconds added to match."
            })
        elif event in game_states:
            notable_time_events.append({
                "time": event.time,
                "clock": event.clock,
                "event": event.desc
            })
        elif event in pending_events:
            pending = True
        elif event == "delegated purloin timer expired.":
            pending = False
        elif pending and event.clock < 0:
            notable_time_events.append({
                "time": notable_time_events[0]["clock"],
                "clock": 0.0,
                "event": "hanging overtime..."
            })
            pending = False

        if green_time_add_expire_time is not None and event.time > green_time_add_expire_time:
            notable_time_events.append({
                "time": green_time_add_expire_time,
                "clock": round(notable_time_events[0]["clock"] - green_time_add_expire_time + time_added, 1),
                "event": "sniper clock dilation ends."
            })
            green_time_add_expire_time = None
    return notable_time_events


def all_overtime_info(game):
    if not game.reaches_ot:
        return
    hang_time = None
    beep_time = None
    pending = None
    recent_mission = None
    countdown_time = None
    gta = False
    gtax = 0
    cdp = False
    # TODO handle hanging GTAs
    for event in game.timeline:
        # if event.time > gtax > 0:  # green time add expires
        #     if pending == "Time Add":
        #         pending = None
        #     gtax = 0

        if event == "missions completed. 10 second countdown.":
            countdown_time = event.time
        elif event == "missions completed. countdown pending.":
            cdp = True
        elif event == "overtime!":
            # OT can begin before a pending purloin/swap triggers mission countdown
            beep_time = 10.0 if countdown_time is None else round(countdown_time + 10 - event.time, 1)
            hang_time = 0.0 if event.clock == 0 else -event.clock
        elif event == "guest list purloin pending." or event in delegate_sends:
            pending = "Purloin"
        elif not cdp and pending == "Purloin" and event == "guest list purloined.":
            pending = None
        elif event == "statue swap pending.":
            pending = "Swap"
        elif not cdp and pending == "Swap" and event == "statue swapped.":
            pending = None
        elif event == "action test green: check watch":
            gta = True
        # elif gta and event == "45 seconds added to match.":
        #     pending = "Time Add"
        #     print("   ", game.uuid)
        #     gtax = event.time + 45 if gtax == 0 else gtax + 45
        #     gta = False
        elif countdown_time is None and event in mission_completes:
            recent_mission = mission_completes[event]

    # if beep_time is None:
    #     return  # Return non-OT games??
    return {
        "hang_cause": pending,
        "hang_time": hang_time,
        "beep_time": beep_time,
        "final_mission": recent_mission,
    }


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
                "test": event.action_test,
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
        #  investigate 0mo3ecbwRHezaEft5e_5jA
    return offers


def all_drink_info_bar(game):
    if not game.venue.bar:
        return
    offers = []
    drink_offer = {
        # "demanded": False,
        "request_time": 0,
        "offer_time": 0,
        "response_time": None,
        "accepted": False,
        "purloin": None
    }
    for event in game.timeline:
        if event in drink_requests_bar or event in drink_demands_bar:
            if drink_offer["request_time"] > 0:
                offers.append(drink_offer)
                drink_offer = {
                    # "demanded": False,
                    "request_time": 0,
                    "offer_time": 0,
                    "response_time": None,
                    "accepted": False,
                    "purloin": None
                }
            drink_offer["request_time"] = event.time
        elif event in drink_offers_bar:
            drink_offer["offer_time"] = event.time
        elif event in drink_accepts_bar:
            drink_offer["accepted"] = True
            drink_offer["response_time"] = round(event.time - drink_offer["offer_time"], 1)
        elif event in drink_rejects_bar:
            # drink_offer["accepted"] = False  # defaults to false
            drink_offer["response_time"] = round(event.time - drink_offer["offer_time"], 1)
        elif event == "delegating purloin guest list.":
            drink_offer["purloin"] = {
                "delegate": True,
                "send_time": None,
                "fade_time": None
            }
        elif event.desc.startswith("delegated purloin to "):
            if drink_offer["purloin"] is None:
                for prev_offer in offers[::-1]:
                    if prev_offer["purloin"] is not None:
                        prev_offer["purloin"]["delegate"] = event.character.name[-1]
                        prev_offer["purloin"]["send_time"] = event.time
                        break
                continue
            drink_offer["purloin"]["delegate"] = event.character.name[-1]
            drink_offer["purloin"]["send_time"] = event.time
        elif event == "guest list purloined.":
            if event.character.role == "Spy":
                drink_offer["purloin"] = {
                    "delegate": False,
                    "send_time": None,
                    "fade_time": event.time
                }
                offers.append(drink_offer)
                drink_offer = {
                    # "demanded": False,
                    "request_time": 0,
                    "offer_time": 0,
                    "response_time": None,
                    "accepted": False,
                    "purloin": None
                }
            else:
                for prev_offer in offers[::-1]:
                    if prev_offer["purloin"] is not None:
                        prev_offer["purloin"]["fade_time"] = event.time
                        break
        elif event == "delegated purloin timer expired.":
            offers.append(drink_offer)
            drink_offer = {
                # "demanded": False,
                "request_time": 0,
                "offer_time": 0,
                "response_time": None,
                "accepted": False,
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
                "test": event.action_test
            })
    return checks


def all_header_info(game):
    return {
        "spy_username": game.spy_username,
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
    "spy leaves conversation.": "Conversation",
    "action triggered: check watch": "Window",  # Time Adds happen at windows too
    "picked up statue.": "Statue",
    "put back statue.": "Statue",
    "get book from bookcase.": "Bookshelf",
    "put book in bookcase.": "Bookshelf",
    "request drink from waiter.": "Request Toby",
    "request cupcake from waiter.": "Request Toby",
    "request drink from bartender.": "Bar",
    "demand drink from bartender.": "Bar",
    "request cupcake from bartender.": "Bar",
    "demand cupcake from bartender.": "Bar",
    "spy picks up briefcase.": "Briefcase",
    "spy puts down briefcase.": "Briefcase",
}
__first_actions = {
    "action triggered: inspect statues": "Inspect",
    "action triggered: transfer microfilm": "Microfilm",
    "action triggered: fingerprint ambassador": "Fingerprint",
    "action triggered: contact double agent": "Contact",
    "action triggered: seduce target": "Seduce",
    "begin planting bug while standing.": "Standing Bug",
    "begin planting bug while walking.": "Walking Bug",
    "watch checked.": "Watch Check",
    "watch checked to add time.": "Time Add",
    "statue swap pending.": "Green Swap",
    "statue swapped.": "Swap",
    "delegating purloin guest list.": "Delegate",
    "guest list purloin pending.": "Green Purloin",
    "guest list purloined.": "Purloin",
}


def all_spy_start_info(game):
    began_with_drink = None
    control_time = None
    destination = None
    first_act = None
    for event in game.timeline:
        if began_with_drink is None:
            if event in drink_finishes:
                began_with_drink = True
            elif event in __non_drink_events:
                began_with_drink = False

        if control_time is None and event == "spy player takes control from ai.":
            # only one of these events so the 'control_time is None' is not necessary
            control_time = event.time

        if destination is None and event in __destinations:
            destination = __destinations[event]
        elif event in __destinations and first_act is None:
            # if the spy going to a second destination without performing an action, they're idling
            first_act = "Idle"

        if first_act is None:
            if event in __first_actions:
                first_act = __first_actions[event]
            elif event == "put book in bookcase." and event.bookshelf != event.held_book:
                first_act = "Direct Transfer"

        if (began_with_drink is not None and
                # control_time is not None and
                destination is not None and
                first_act is not None):
            break
    # print(f"{game.uuid} resulted in at least one null:")
    # print(f"\ttake_control_time: {control_time}")
    # print(f"\tbegan_with_drink: {began_with_drink}")
    # print(f"\tfirst_destination: {destination}")
    # TODO investigate null began_with_drink and first_destination entries
    return {
        "take_control_time": control_time,
        "began_with_drink": began_with_drink,
        "first_destination": destination,
        "starting_action": first_act,
    }


def all_audible_info(game):
    noises = []

    def __log_noise(evt, typ):
        noises.append({
            "time": evt.time,
            "type": typ
        })

    red_tested_timeadd = False
    red_tested_contact = False
    for event in game.timeline:
        if event == "action test red: contact double agent":
            red_tested_contact = True
        elif event == "action test red: check watch":
            red_tested_timeadd = True
        elif (
                event == "aborted watch check to add time." or
                (red_tested_timeadd and event == "45 seconds added to match.")
        ):
            __log_noise(event, "*beep*")
            red_tested_timeadd = False
        # TODO missing "*cough* *cough*"
        elif event == "banana bread aborted.":
            if red_tested_contact:
                __log_noise(event, "*cough* *cough* *cough*")
                red_tested_contact = False
            else:
                __log_noise(event, "*cough*")
        elif red_tested_contact and event in bb_utter:
            __log_noise(event, "banana bread *cough*")
        # elif event in bb_utter:  # bb is very redundant
        #     if red_tested_contact:
        #         __log_noise(event, "banana bread *cough*")
        #     else:
        #         __log_noise(event, "banana bread")
        elif event == "dropped statue.":
            __log_noise(event, "*clank*")
        elif event == "purloin guest list aborted.":
            __log_noise(event, "*crash*")
    # audibles are sparse, so this reduces uuid redundancy
    # alternatively, include ALL audible information with normal BB and beeps --> MASSIVE redundance
    return noises if len(noises) > 0 else None


def info_sniper_lights(game):
    return [{
        "time": event.time,
        "chara": event.character.name[-1],
        "light": sniper_lights_numeric[event]
    } for event in game.timeline if event in sniper_lights_numeric]


def info_sniper_marks(game):
    if game.venue.bookshelves == 0:
        return  # can't bookmark if there are no books!
    # if "Transfer" not in game.missions_selected:
    #     return  # couldn't bookmark if transfer isn't selected
    if game.date > "2019-11-06T16:21:00":
        return  # bookmarking was removed after the Redwoods Update
    return [{
        "time": event.time,
        "chara": event.character.name[-1],
        "color": event.held_book
    } for event in game.timeline if event in sniper_marks]


def all_convo_info(game):
    convos = []
    convo = {
        "enter_time": None,
        "talks": [],
        "leave_time": None,
    }

    def __log_talk(evt, typ):
        convo["talks"].append({
            "time": evt.time,
            "type": typ
            # TODO add stop-talk flag
            #  double talks?
            #  convo bails?
        })

    flirted_in_this_convo = False
    for event in game.timeline:
        if event == "spy enters conversation.":
            flirted_in_this_convo = False
            convo["enter_time"] = event.time
        elif event == "spy leaves conversation.":
            convo["leave_time"] = event.time
            convos.append(convo)
            convo = {
                "enter_time": None,
                "talks": [],
                "leave_time": None,
            }
        elif event == "started talking.":
            # TODO guilty talks
            __log_talk(event, "Innocent Talk")
        elif event == "interrupted speaker.":
            __log_talk(event, "Interrupt")
        elif event in delegate_sends:
            __log_talk(event, "Delegate")
        elif event in action_test_contact_talking:
            __log_talk(event, "Contact")
        elif event.in_conversation:
            if event == "action triggered: seduce target":
                if flirted_in_this_convo:
                    __log_talk(event, "Timer Flirt")
                else:
                    __log_talk(event, "Flirt")
                    flirted_in_this_convo = True
    if convo["enter_time"] is not None:
        convos.append(convo)
    return convos


def all_briefcase_info(game):
    cases = []
    case = {
        "pickup_time": 0,
        "putdown_time": None,
        "handoff_time": None,
    }
    for event in game.timeline:
        if event == "spy picks up briefcase.":
            case["pickup_time"] = event.time
        elif event == "spy returns briefcase.":
            case["handoff_time"] = event.time
            cases.append(case)
            case = {
                "pickup_time": 0,
                "putdown_time": None,
                "handoff_time": None,
            }
        elif event == "spy puts down briefcase.":
            case["putdown_time"] = event.time
            cases.append(case)
            case = {
                "pickup_time": 0,
                "putdown_time": None,
                "handoff_time": None,
            }
    # despite the briefcase being available in every game, it is picked up sparsely
    if len(cases) > 0:
        return cases


def all_at_info(game):
    ats = []
    last_trig = 0
    for event in game.timeline:
        if event in action_triggers_with_test:
            last_trig = event.time
        elif event in action_tests:
            ats.append({
                "duration": round(event.time - last_trig, 1),
                "mission": event.mission,
                "test": event.action_test
            })
    return ats


def all_psv_info(game):
    psvs = []
    # (0, 7.1]      = Spy Overcrowded Amba
    # [7.2, 8.0]    = Spy Crowded Amba  (7.6 +- 0.4)
    # [8.1, +inf)   = Amba Crowded Spy
    cc_enter_ts = None
    for event in game.timeline:
        if event == "spy enters conversation.":
            cc_enter_ts = event.time
        elif event == "ambassador's personal space violated.":
            if cc_enter_ts is None:
                psvs.append(None)
            else:
                psvs.append(round(event.time - cc_enter_ts, 1))
                cc_enter_ts = None
    if len(psvs) > 0:
        return psvs
