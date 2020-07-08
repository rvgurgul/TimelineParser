from EventGroups import *


def all_bug_info(game):
    if "Bug" not in game.missions_selected:
        return
    bugs = []
    planting, transit = False, False
    for event in game.timeline:
        if event == "action triggered: bug ambassador":
            bugs.append({
                "time": event.time,
                "type": None,
                "took": None,
                "confirm_time": None,
            })
            planting = True
        elif event == "begin planting bug while standing.":
            bugs[-1]["type"] = "Standing"
        elif event == "begin planting bug while walking.":
            if event.in_conversation:
                bugs[-1]["type"] = "Reverse"
            else:
                bugs[-1]["type"] = "Walking"
        elif event == "spy enters conversation.":
            if transit or bugs[-1]["type"] == "Exit":
                bugs[-1]["type"] = "Twitch"
            elif planting:
                bugs[-1]["type"] = "Entry"
        elif event == "spy leaves conversation.":
            if transit or bugs[-1]["type"] == "Standing":
                bugs[-1]["type"] = "Twitch"
            elif planting:
                bugs[-1]["type"] = "Exit"
        elif event == "bug transitioned from standing to walking.":
            transit = True
        elif event == "failed planting bug while walking.":
            bugs[-1]["took"] = False
            bugs[-1]["confirm_time"] = event.time
            planting, transit = False, False
        elif event == "bugged ambassador while walking." or event == "bugged ambassador while standing.":
            bugs[-1]["took"] = True
            bugs[-1]["confirm_time"] = event.time
            break
    return bugs


def shot_details(game):
    if game.cast.shot is None:
        return
    tlfs = False
    shot_time = None
    finish_ts = 0
    mission_complete_time = None
    for event in game.timeline[::-1]:
        if event in game_ends:
            finish_ts = event.time
        elif event == "sniper shot too late for sync.":
            tlfs = True
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
        "latency": None if tlfs else round(finish_ts - shot_time, 1),
        "countdown": round(10 - shot_time + mission_complete_time, 1) if mission_complete_time is not None else None
        # "role": game.cast.shot.role,  # role is redundant with cast_info
    }


def all_cast_info(game):
    return {
        "Spy": game.cast.spy.name[-1],
        "SeductionTarget": game.cast.seduction_target.name[-1] if game.cast.seduction_target is not None else "",
        "Ambassador": game.cast.ambassador.name[-1],
        "DoubleAgent": game.cast.double_agent.name[-1],
        "SuspectedDoubleAgent": "".join(x.name[-1] for x in game.cast.suspected_agents),
        "Civilian": "".join(x.name[-1] for x in game.cast.civilians)
    }


__intermediate = {
    "action triggered: bug ambassador",
    "spy enters conversation.",
    "spy picks up briefcase.",
    "watch checked.",
    "read book.",
}


def all_book_info(game):
    if not game.venue.bookshelves:
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
        elif event in action_test_transfer:
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
                "microfilm": transfer,
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
                "microfilm": transfer,
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
        elif event in action_test_fingerprint:
            last_atr = event.action_test
        elif event in __printed:
            prints.append({
                "time": event.time,
                "item": item,
                "test": last_atr,
            })
            item, last_atr = None, None
    return prints

def all_statue_info(game):
    if game.venue.statues == 0:
        return
    bookspects = game.venue.name == "Redwoods"
    statues = []
    statue = {
        "pickup_time": None,
        "printable": None,
        "inspect": [],
        "swap": None,
        "putback_time": None
    }
    for event in game.timeline:
        if event == "picked up statue.":
            statue["pickup_time"] = event.time
            statue["printable"] = 0
        elif bookspects and event == "get book from bookcase." and event.held_book in {"Red", "Green"}:
            statue["pickup_time"] = event.time
        elif event == 'picked up fingerprintable statue (difficult).':
            statue["printable"] = 1
        elif event == 'picked up fingerprintable statue.':
            statue["printable"] = 2
        elif event in action_test_inspect:
            statue["inspect"].append({
                "time": event.time,
                "test": event.action_test,
                "which": None,  # unknown until the inspect is complete
            })
        elif event in action_test_swap:
            statue["swap"] = {
                "time": event.time,
                "test": event.action_test,
                "swapper": None,
                "swap_time": None,
            }
        elif event in inspect_completed:
            statue["inspect"][-1]["which"] = inspect_completed[event]
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
        elif event == "put back statue." or (event == "dropped statue." and statue["pickup_time"] is not None):
            # clanks are treated the same as a normal statue putback, can be determined with audibles.json
            statue["putback_time"] = event.time
            statues.append(statue)
            statue = {
                "pickup_time": None,
                "printable": None,
                "inspect": [],
                "swap": None,
                "putback_time": None
            }
        elif bookspects and event == "put book in bookcase." and event.bookshelf in {"Red", "Green"}:
            statue["putback_time"] = event.time
            statues.append(statue)
            statue = {
                "pickup_time": None,
                "printable": None,
                "inspect": [],
                "swap": None,
                "putback_time": None
            }
    if statue["pickup_time"] is not None:
        statues.append(statue)
    return statues


def all_seduce_info(game):
    if "Seduce" not in game.missions_selected:
        return  # for the few games with Seduce off
    flirts = []
    progress = 0
    for event in game.timeline:
        if event == "action triggered: seduce target":
            flirts.append({
                "time": event.time,
                "test": None,
                "gain": None,
                "cooldown_time": None,
            })
        elif event in action_test_seduce:
            flirts[-1]["test"] = action_test_seduce[event]
        elif event in {
            "failed flirt with seduction target.",
            "seduction canceled.",
        }:
            flirts[-1]["gain"] = 0
        elif event in flirt_percents:
            percent = flirt_percents[event]
            flirts[-1]["gain"] = percent - progress
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
    for event in game.timeline:
        if event == "action triggered: contact double agent":
            contacts.append({
                "time": event.time,
                "test": None,
                "initial": None,
                "final": None,
                "utter_time": None,
                "confirm_time": None,
            })
        elif event in action_test_contact:
            contacts[-1]["test"] = event.action_test
        elif event == "real banana bread started.":
            contacts[-1]["initial"] = "Real"
        elif event == "fake banana bread started.":
            contacts[-1]["initial"] = "Fake"
        elif event == "fake banana bread uttered.":
            contacts[-1]["final"] = "Fake"
            contacts[-1]["utter_time"] = event.time
        elif event == "banana bread uttered.":
            contacts[-1]["final"] = "Real"
            contacts[-1]["utter_time"] = event.time
        elif event == "double agent contacted.":
            contacts[-1]["confirm_time"] = event.time
    return contacts

def all_da_intersects(game):
    da_convos = []
    for event in game.timeline:
        if event == "spy joined conversation with double agent.":
            da_convos.append({
                "joiner": "Spy",
                "enter_time": event.time,
                "leave_time": None,
                "leaver": None
            })
        elif event == "double agent joined conversation with spy.":
            da_convos.append({
                "joiner": "DoubleAgent",
                "enter_time": event.time,
                "leave_time": None,
                "leaver": None
            })
        elif event == "spy left conversation with double agent.":
            if len(da_convos) > 0:
                da_convos[-1]["leave_time"] = event.time
                da_convos[-1]["leaver"] = "Spy"
            else:
                da_convos.append({
                    "joiner": None,
                    "enter_time": None,
                    "leave_time": event.time,
                    "leaver": "Spy"
                })
        elif event == "double agent left conversation with spy.":
            if len(da_convos) > 0:
                da_convos[-1]["leave_time"] = event.time
                da_convos[-1]["leaver"] = "DoubleAgent"
            else:
                da_convos.append({
                    "joiner": None,
                    "enter_time": None,
                    "leave_time": event.time,
                    "leaver": "DoubleAgent"
                })
    return da_convos

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
        "offer_time": None,
        "response_time": None,
        "accepted": None,
        "purloin": None,
    }
    for event in game.timeline:
        if event in drink_requests_tray:
            drink_offer["requested"] = True
        elif event in drink_offers_tray:
            drink_offer["offer_time"] = event.time
        elif event in action_test_purloin:
            drink_offer["purloin"] = {
                "test": event.action_test,
                "list_taker": None,
                "fade_time": None
            }
        elif event in drink_accepts:
            drink_offer["accepted"] = True
            if drink_offer["offer_time"] is None:
                print(game.uuid, drink_offer)
                return
            drink_offer["response_time"] = round(event.time - drink_offer["offer_time"], 1)
        elif event in drink_rejects_tray:
            drink_offer["accepted"] = False
            if drink_offer["offer_time"] is None:
                print(game.uuid, drink_offer)
                return
            drink_offer["response_time"] = round(event.time - drink_offer["offer_time"], 1)
        elif event in {"guest list purloined.", "guest list returned."}:
            if drink_offer["purloin"] is not None:
                drink_offer["purloin"]["list_taker"] = event.character.name[-1]
                drink_offer["purloin"]["fade_time"] = event.time
                continue
            for prev_offer in offers[::-1]:
                if prev_offer["purloin"] is not None:
                    prev_offer["purloin"]["list_taker"] = event.character.name[-1]
                    prev_offer["purloin"]["fade_time"] = event.time
        # elif event == "purloin guest list aborted.":
        #     offers[-1]["purloin"] = {
        #         "test": "Canceled",
        #         "list_taker": None,
        #         "fade_time": None
        #     }
        # TODO crashes still fuzzy
        #  0mo3ecbwRHezaEft5e_5jA
        elif event in {"waiter stopped offering cupcake.", "waiter stopped offering drink."}:
            offers.append(drink_offer)
            drink_offer = {
                "requested": False,
                "offer_time": None,
                "response_time": None,
                "accepted": None,
                "purloin": None
            }
        # elif event == "waiter gave up." and drink_offer["offer_time"] is not None:
        #     drink_offer["response_time"] = round(event.time - drink_offer["offer_time"], 1)
        #     offers.append(drink_offer)
        #     drink_offer = {
        #         "requested": False,
        #         "offer_time": None,
        #         "response_time": None,
        #         "accepted": None,
        #         "purloin": None
        #     }
    if drink_offer["offer_time"] or drink_offer["purloin"] or drink_offer["requested"]:
        offers.append(drink_offer)
    return offers


def all_drink_info_bar(game):
    if not game.venue.bar:
        return
    offers = []
    for event in game.timeline:
        if event in drink_requests_bar:
            offers.append({
                "request_time": event.time,
                "demand_time": None,
                "notice_time": None,
                "offer_time": None,
                "response_time": None,
                "accepted": None,
                "purloin": None,
            })
        elif event in drink_demands_bar:
            if len(offers) == 0:
                offers.append({
                    "request_time": None,
                    "demand_time": event.time,
                    "offer_time": None,
                    "notice_time": None,
                    "response_time": None,
                    "accepted": None,
                    "purloin": None,
                })
            else:  # TODO may be able to overwrite existing entries by not appending a new offer
                offers[-1]["demand_time"] = event.time
        elif event == 'bartender picked next customer.':
            offers[-1]["notice_time"] = event.time
        elif event in drink_offers_bar:
            offers[-1]["offer_time"] = event.time
        elif event in drink_accepts_bar:
            offers[-1]["response_time"] = event.time
            offers[-1]["accepted"] = True
        elif event in drink_rejects_bar:
            offers[-1]["response_time"] = event.time
            offers[-1]["accepted"] = False
        elif event == "action triggered: purloin guest list" and not event.in_conversation:
            offers[-1]["purloin"] = {
                "time": event.time,
                "delegate": None,
                "send_time": None,
                "fade_time": None
            }
        elif event == "delegating purloin guest list.":
            offers[-1]["purloin"]["delegate"] = True
            if offers[-1]["accepted"] is None:
                offers[-1]["accepted"] = False  # delegate reject patch
        elif event in delegate_sends:
            for prev_offer in offers[::-1]:
                if prev_offer["purloin"]:
                    prev_offer["purloin"]["delegate"] = event.character.name[-1]
                    prev_offer["purloin"]["send_time"] = event.time
                    break
        elif event == "guest list purloined.":
            if event.character.role == "Spy":
                offers[-1]["purloin"]["delegate"] = False
            for prev_offer in offers[::-1]:
                if prev_offer["purloin"]:
                    prev_offer["purloin"]["fade_time"] = event.time
                    break
        # elif event == "delegated purloin timer expired.":
        #     offers.append(drink_offer)
        #     drink_offer = {
        #         # "demanded": False,
        #         "request_time": 0,
        #         "offer_time": 0,
        #         "response_time": None,
        #         "accepted": False,
        #         "purloin": None
        #     }

    # TODO still needs some work to resolve 'fade_time' entries
    return offers


def all_watch_info(game):
    checks = []
    for event in game.timeline:
        if event == "action triggered: check watch":
            checks.append({
                "time": event.time,
                "test": None,
                "done": None,
            })
        elif event == "watch checked to add time.":
            checks[-1]["test"] = "Triggered"
        elif event in action_test_timeadd:
            checks[-1]["test"] = action_test_timeadd[event]
        elif event == "45 seconds added to match.":
            checks[-1]["done"] = event.time
        elif event == "aborted watch check to add time.":
            checks[-1]["done"] = False
    return checks


def all_header_info(game):
    return {
        "spy": game.spy_username,
        "sniper": game.sniper_username,
        "date_played": game.date,
        "venue": game.venue.name,
        "result": game.specific_win_condition,
    }

def all_mission_info(game):
    if game.mode[0] == 'k':
        a = o = int(game.mode[1])
    elif game.mode[0] == 'a':
        a = int(game.mode[1])
        o = int(game.mode[3])
    else:
        a = 0
        o = 0
    wip_format = {
        "any": a,
        "of": o,
        "missions": {mission: -2 for mission in mission_names}
    }
    for mission in game.venue.missions:
        wip_format["missions"][mission] = -1
    for mission in game.missions_selected:
        wip_format["missions"][mission] = 0
    for event in game.timeline:
        if event in mission_completes:
            wip_format["missions"][mission_completes[event]] = event.time
    return wip_format

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
    "get book from bookcase.",
}
__destinations = {
    "spy enters conversation.": "Conversation",
    "spy leaves conversation.": "Conversation",
    "double agent joined conversation with spy.": "Conversation",
    "double agent left conversation with spy.": "Conversation",
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

        if event == "spy player takes control from ai.":
            control_time = event.time

        if control_time is not None:
            if event in __destinations:
                if destination is None:
                    destination = __destinations[event]
                elif first_act is None:
                    # if the spy going to a second destination without performing an action, they idled to start
                    first_act = "Idle"

            if first_act is None:
                if event in __first_actions:
                    first_act = __first_actions[event]
                elif event == "put book in bookcase." and event.bookshelf != event.held_book:
                    first_act = "Direct Transfer"

    # print(f"{game.uuid} resulted in at least one null:")
    # print(f"\ttake_control_time: {control_time}")
    # print(f"\tbegan_with_drink: {began_with_drink}")
    # print(f"\tfirst_destination: {destination}")
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
        elif event == "action test canceled: contact double agent":
            __log_noise(event, "*cough* *cough*")
        elif (
                event == "aborted watch check to add time." or
                (red_tested_timeadd and event == "45 seconds added to match.")
        ):
            __log_noise(event, "*beep*")
            red_tested_timeadd = False
        elif event == "banana bread aborted.":
            if red_tested_contact:
                __log_noise(event, "*cough* *cough* *cough*")
                red_tested_contact = False
            else:
                __log_noise(event, "*cough*")
        elif red_tested_contact and event in bb_utter:
            __log_noise(event, "banana bread *cough*")
            red_tested_contact = False
        elif event == "dropped statue.":
            __log_noise(event, "*clank*")
        elif event == "purloin guest list aborted.":
            __log_noise(event, "*crash*")
    # audibles are sparse, so this reduces uuid redundancy
    return noises if len(noises) > 0 else None


def info_sniper_lights(game):
    prelim = [{
        "time": event.time,
        "chara": event.character.name[-1],
        "light": sniper_lights_numeric[event]
    } for event in game.timeline if event in sniper_lights_numeric]
    i = 1  # removes lights where the character is repeated twice in a row because they are not very meaningful
    while i < len(prelim):
        if prelim[i - 1]["chara"] == prelim[i]["chara"]:
            prelim.pop(i - 1)
            continue
        i += 1
    return prelim

def info_sniper_marks(game):
    if game.venue.bookshelves == 0:
        return  # can't bookmark if there are no books!
    if game.date > "2019-11-06T16:00:00":
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
            "type": typ,
            "stop": False,
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
            flirted_in_this_convo = False
        elif event == "started talking.":
            __log_talk(event, "Talk")
        elif event == "interrupted speaker.":
            __log_talk(event, "Interrupt")
        elif event in delegate_sends:
            __log_talk(event, "Delegate")
        elif event in action_test_contact_talking:
            __log_talk(event, "Contact")
        elif event == "action triggered: seduce target" and event.in_conversation:
            if flirted_in_this_convo:
                __log_talk(event, "Timer Flirt")
            else:
                __log_talk(event, "Flirt")
                flirted_in_this_convo = True
        elif event == "stopped talking.":
            if len(convo["talks"]) == 0:  # AI must have began talking
                convo["talks"].append({
                    "time": None,
                    "type": "AI Talk",
                    "stop": event.time
                })
                continue
            convo["talks"][-1]["stop"] = event.time
    if convo["enter_time"] is not None:
        convos.append(convo)
    return convos


def all_briefcase_info(game):
    cases = []
    for event in game.timeline:
        if event == "spy picks up briefcase.":
            cases.append({
                "pickup_time": event.time,
                "printable": 0,
                "returned": None,
                "putback_time": None,
            })
        elif event == 'picked up fingerprintable briefcase (difficult).':
            if len(cases) == 0:
                cases.append({
                    "pickup_time": None,
                    "printable": 1,
                    "returned": None,
                    "putback_time": None,
                })
            else:
                cases[-1]["printable"] = 1
        elif event == 'picked up fingerprintable briefcase.':
            if len(cases) == 0:
                cases.append({
                    "pickup_time": None,
                    "printable": 2,
                    "returned": None,
                    "putback_time": None,
                })
            else:
                cases[-1]["printable"] = 2
        elif event == "spy returns briefcase.":
            if len(cases) == 0:
                cases.append({
                    "pickup_time": None,
                    "printable": None,
                    "returned": True,
                    "putback_time": event.time,
                })
            else:
                cases[-1]["returned"] = True
                cases[-1]["putback_time"] = event.time
        elif event == "spy puts down briefcase.":
            if len(cases) == 0:
                cases.append({
                    "pickup_time": None,
                    "printable": None,
                    "returned": False,
                    "putback_time": event.time,
                })
            else:
                cases[-1]["returned"] = False
                cases[-1]["putback_time"] = event.time
    # despite the briefcase being available in every game, it is picked up sparsely
    if len(cases) > 0:
        return cases


def all_at_info(game):
    ats = []
    for event in game.timeline:
        if event in action_triggers_with_test:
            ats.append({
                "time": event.time,
                "test": None,
                "mission": action_triggers_with_test[event],
                "duration": None,
            })
        elif event in action_tests:
            test, _ = action_tests[event]
            ats[-1]["test"] = test[0]
            ats[-1]["duration"] = round(event.time - ats[-1]["time"], 1)
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
