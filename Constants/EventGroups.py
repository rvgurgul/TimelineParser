# This file is my replacement for event categories


# [SniperLights, Books] --> marks
marks = {
    "marked book."
}

lights = {
    "marked suspicious.": "Highlight",
    "marked spy suspicious.": "Highlight",
    "marked less suspicious.": "Lowlight",
    "marked spy less suspicious.": "Lowlight",
    "marked neutral suspicion.": "Neutral Light",
    "marked spy neutral suspicion.": "Neutral Light",
    "marked default suspicion.": "Default Light",
    "marked spy default suspicion.": "Default Light",
}
lights_abbreviated = {
    "marked suspicious.": "HL",
    "marked spy suspicious.": "HL",
    "marked less suspicious.": "LL",
    "marked spy less suspicious.": "LL",
    "marked neutral suspicion.": "NL",
    "marked spy neutral suspicion.": "NL",
    "marked default suspicion.": "DL",
    "marked spy default suspicion.": "DL",
}

drink_gulps = {
    "gulped drink.",
    "chomped cupcake."
}
drink_sips = {
    "sipped drink.",
    "bit cupcake.",
    "took last sip of drink.",
    "took last bite of cupcake."
}
drink_finishes = drink_gulps | {
    "took last sip of drink.",
    "took last bite of cupcake."
}

drink_accepts_tray = {
    "got drink from waiter.",
    "got cupcake from waiter.",
}
drink_accepts_bar = {
    "got drink from bartender.",
    "got cupcake from bartender.",
}
drink_accepts = drink_accepts_tray | drink_accepts_bar

drink_offers_tray = {
    "waiter offered cupcake.",
    "waiter offered drink."
}
drink_offers_bar = {
    "bartender offered cupcake.",
    "bartender offered drink."
}
drink_offers = drink_accepts_tray | drink_accepts_bar

drink_end_offers = {
    "waiter stopped offering cupcake.",
    "waiter stopped offering drink."
}

drink_rejects_tray = {
    "rejected drink from waiter.",
    "rejected cupcake from waiter.",
    "waiter gave up."
}
drink_rejects_bar = {
    "rejected drink from bartender.",
    "rejected cupcake from bartender.",
}
drink_rejects = drink_rejects_bar | drink_rejects_tray

drink_requests_tray = {
    "request drink from waiter.",
    "request cupcake from waiter.",
}
drink_requests_bar = {
    "request drink from bartender.",
    "request cupcake from bartender.",
}
drink_requests = drink_requests_tray | drink_requests_bar

drink_demands_bar = {
    "demand drink from bartender.",
    "demand cupcake from bartender.",
}

result_events_spy_win = {
    "missions completed successfully.",
    "sniper shot civilian.",
}
result_events_sniper_win = {
    "spy ran out of time.",
    "sniper shot spy."
}
game_ends = result_events_sniper_win | result_events_spy_win

bb_start = {
    "real banana bread started.",
    "fake banana bread started."
}
bb_utter = {
    "banana bread uttered.",
    "fake banana bread uttered."
}

cooldowns = {
    "flirtation cooldown expired.",
    "delegated purloin timer expired."
}

flirt_percents = {
    'flirt with seduction target: 17%': 17,
    'flirt with seduction target: 18%': 18,
    'flirt with seduction target: 19%': 19,
    'flirt with seduction target: 20%': 20,
    'flirt with seduction target: 21%': 21,
    'flirt with seduction target: 22%': 22,
    'flirt with seduction target: 23%': 23,
    'flirt with seduction target: 24%': 24,
    'flirt with seduction target: 25%': 25,
    'flirt with seduction target: 26%': 26,
    'flirt with seduction target: 27%': 27,
    'flirt with seduction target: 28%': 28,
    'flirt with seduction target: 29%': 29,
    'flirt with seduction target: 30%': 30,
    'flirt with seduction target: 31%': 31,
    'flirt with seduction target: 32%': 32,
    'flirt with seduction target: 33%': 33,
    'flirt with seduction target: 34%': 34,
    'flirt with seduction target: 35%': 35,
    'flirt with seduction target: 36%': 36,
    'flirt with seduction target: 37%': 37,
    'flirt with seduction target: 38%': 38,
    'flirt with seduction target: 39%': 39,
    'flirt with seduction target: 40%': 40,
    'flirt with seduction target: 41%': 41,
    'flirt with seduction target: 42%': 42,
    'flirt with seduction target: 43%': 43,
    'flirt with seduction target: 44%': 44,
    'flirt with seduction target: 45%': 45,
    'flirt with seduction target: 46%': 46,
    'flirt with seduction target: 47%': 47,
    'flirt with seduction target: 48%': 48,
    'flirt with seduction target: 49%': 49,
    'flirt with seduction target: 50%': 50,
    'flirt with seduction target: 51%': 51,
    'flirt with seduction target: 52%': 52,
    'flirt with seduction target: 53%': 53,
    'flirt with seduction target: 54%': 54,
    'flirt with seduction target: 55%': 55,
    'flirt with seduction target: 56%': 56,
    'flirt with seduction target: 57%': 57,
    'flirt with seduction target: 58%': 58,
    'flirt with seduction target: 59%': 59,
    'flirt with seduction target: 60%': 60,
    'flirt with seduction target: 61%': 61,
    'flirt with seduction target: 62%': 62,
    'flirt with seduction target: 63%': 63,
    'flirt with seduction target: 64%': 64,
    'flirt with seduction target: 65%': 65,
    'flirt with seduction target: 66%': 66,
    'flirt with seduction target: 67%': 67,
    'flirt with seduction target: 68%': 68,
    'flirt with seduction target: 69%': 69,
    'flirt with seduction target: 70%': 70,
    'flirt with seduction target: 71%': 71,
    'flirt with seduction target: 72%': 72,
    'flirt with seduction target: 73%': 73,
    'flirt with seduction target: 74%': 74,
    'flirt with seduction target: 75%': 75,
    'flirt with seduction target: 76%': 76,
    'flirt with seduction target: 77%': 77,
    'flirt with seduction target: 78%': 78,
    'flirt with seduction target: 79%': 79,
    'flirt with seduction target: 80%': 80,
    'flirt with seduction target: 81%': 81,
    'flirt with seduction target: 82%': 82,
    'flirt with seduction target: 83%': 83,
    'flirt with seduction target: 84%': 84,
    'flirt with seduction target: 85%': 85,
    'flirt with seduction target: 86%': 86,
    'flirt with seduction target: 87%': 87,
    'flirt with seduction target: 88%': 88,
    'flirt with seduction target: 89%': 89,
    'flirt with seduction target: 90%': 90,
    'flirt with seduction target: 91%': 91,
    'flirt with seduction target: 92%': 92,
    'flirt with seduction target: 93%': 93,
    'flirt with seduction target: 94%': 94,
    'flirt with seduction target: 95%': 95,
    'flirt with seduction target: 96%': 96,
    'flirt with seduction target: 97%': 97,
    'flirt with seduction target: 98%': 98,
    'flirt with seduction target: 99%': 99,
    'flirt with seduction target: 100%': 100,
}

delegate_sends = {
    'delegated purloin to dr. m.',
    'delegated purloin to dr. n.',
    'delegated purloin to mr. a.',
    'delegated purloin to mr. c.',
    'delegated purloin to mr. d.',
    'delegated purloin to mr. g.',
    'delegated purloin to mr. i.',
    'delegated purloin to mr. k.',
    'delegated purloin to mr. p.',
    'delegated purloin to mr. q.',
    'delegated purloin to mr. s.',
    'delegated purloin to mr. u.',
    'delegated purloin to ms. b.',
    'delegated purloin to ms. e.',
    'delegated purloin to ms. f.',
    'delegated purloin to ms. h.',
    'delegated purloin to ms. j.',
    'delegated purloin to ms. l.',
    'delegated purloin to ms. o.',
    'delegated purloin to ms. r.',
    'delegated purloin to ms. t.',
}

fingerprint_starts = {
    'started fingerprinting book.': "Book",
    'started fingerprinting briefcase.': "Briefcase",
    'started fingerprinting cupcake.': "Drink",
    'started fingerprinting drink.': "Drink",
    'started fingerprinting statue.': "Statue",
}
fingerprint_failure = {
    'fingerprinting failed.'
}
fingerprint_success = {
    'fingerprinted book.': "Book",
    'fingerprinted briefcase.': "Briefcase",
    'fingerprinted cupcake.': "Drink",
    'fingerprinted drink.': "Drink",
    'fingerprinted statue.': "Statue",
}
printable_pickups_easy = {
    'picked up fingerprintable briefcase.',
    'picked up fingerprintable statue.',
}
printable_pickups_hard = {
    'picked up fingerprintable briefcase (difficult).',
    'picked up fingerprintable statue (difficult).',
}
printable_pickups = printable_pickups_easy | printable_pickups_hard

audible_cancels = {
    'aborted watch check to add time.': "Beep",
    'purloin guest list aborted.': "Crash",
    'banana bread aborted.': "Cough",
    'dropped statue.': "Clank",
}

action_triggers = {
    'action triggered: bug ambassador',
    'action triggered: check watch',
    'action triggered: contact double agent',
    'action triggered: fingerprint ambassador',
    'action triggered: inspect statues',
    'action triggered: purloin guest list',
    'action triggered: seduce target',
    'action triggered: swap statue',
    'action triggered: transfer microfilm',
}
action_test_contact = {
    'action test canceled: contact double agent': "Canceled",
    'action test green: contact double agent': "Green",
    'action test ignored: contact double agent': "Ignored",
    'action test red: contact double agent': "Red",
    'action test white: contact double agent': "White",
}
action_test_seduce = {
    'action test canceled: seduce target': "Canceled",
    'action test green: seduce target': "Green",
    'action test ignored: seduce target': "Ignored",
    'action test red: seduce target': "Red",
    'action test white: seduce target': "White",
}
action_test_purloin = {
    'action test canceled: purloin guest list': "Canceled",
    'action test green: purloin guest list': "Green",
    'action test ignored: purloin guest list': "Ignored",
    'action test red: purloin guest list': "Red",
    'action test white: purloin guest list': "White",
}
action_test_transfer = {
    'action test green: transfer microfilm': "Green",
    'action test ignored: transfer microfilm': "Ignored",
    'action test red: transfer microfilm': "Red",
    'action test white: transfer microfilm': "White",
}
action_test_swap = {
    'action test green: swap statue': "Green",
    'action test ignored: swap statue': "Ignored",
    'action test red: swap statue': "Red",
    'action test white: swap statue': "White",
}
action_test_fingerprint = {
    'action test green: fingerprint ambassador': "Green",
    'action test ignored: fingerprint ambassador': "Ignored",
    'action test red: fingerprint ambassador': "Red",
}
action_test_inspect = {
    'action test green: inspect statues': "Green",
    'action test ignored: inspect statues': "Ignored",
    'action test red: inspect statues': "Red",
    'action test white: inspect statues': "White",
}
action_test_timeadd = {
    'action test green: check watch': "Green",
    'action test ignored: check watch': "Ignored",
    'action test red: check watch': "Red",
    'action test white: check watch': "White",
}
# action_tests = (
#     action_test_contact |
#     action_test_seduce |
#     action_test_purloin |
#     action_test_transfer |
#     action_test_inspect |
#     action_test_swap |
#     action_test_fingerprint |
#     action_test_timeadd
# )

bug_plant_starts = {
    "begin planting bug while standing.",
    "begin planting bug while walking."
}

mission_completes = {
    "bugged ambassador while standing.": "Bug",
    "bugged ambassador while walking.": "Bug",
    "double agent contacted.": "Contact",
    "target seduced.": "Seduce",
    "transferred microfilm": "Transfer",
    "all statues inspected.": "Inspect",
    "statue swapped.": "Swap",
    "guest list purloined.": "Purloin",
    "guest list returned.": "Purloin",
    "fingerprinted ambassador": "Fingerprint",
}

mission_partials = {
    "hide microfilm in book.": "Transfer",
    "remove microfilm from book.": "Transfer",
    "held statue inspected.": "Inspect",
    "left statue inspected.": "Inspect",
    "right statue inspected.": "Inspect",
    "statue swap pending.": "Swap",
    "guest list purloin pending.": "Purloin",
    "guest list return pending.": "Purloin",
    "45 seconds added to match.": "Time Add",
}

mission_fails = {
    "failed planting bug while walking.": "Bug",
    'banana bread aborted.': "Contact",
    "left alone while attempting banana bread.": "Contact",
    "failed flirt with seduction target.": "Seduce",
    "seduction canceled.": "Seduce",
    "inspection interrupted.": "Inspect",
    "statue inspection interrupted.": "Inspect",
    'purloin guest list aborted.': "Purloin",
    "fingerprinting failed": "Fingerprint",
    'aborted watch check to add time.': "Time Add",
}

game_states = {
    "game started.",
    "missions completed. 10 second countdown.",
    "missions completed. countdown pending.",
    "overtime!"
}

actor_assignments = {
    "flirtation cooldown expired.": "SeductionTarget",
    "ambassador's personal space violated.": "Ambassador",
    "double agent joined conversation with spy.": "DoubleAgent",
    "double agent left conversation with spy.": "DoubleAgent",
    "waiter offered cupcake.": "Waiter",
    "waiter offered drink.": "Waiter",
    "waiter stopped offering cupcake.": "Waiter",
    "waiter stopped offering drink.": "Waiter",
    "waiter gave up.": "Waiter",
    "bartender offered cupcake.": "Bartender",
    "bartender offered drink.": "Bartender",
    "bartender stopped offering cupcake.": "Bartender",
    "bartender stopped offering drink.": "Bartender",
    "bartender picked next customer.": "Bartender"
}

setup_role_cast = {
    "ambassador cast.",
    "civilian cast.",
    "double agent cast.",
    "seduction target cast.",
    "spy cast.",
    "suspected double agent cast."
}
setup_mission_selected = {
    "bug ambassador selected.",
    "contact double agent selected.",
    "fingerprint ambassador selected.",
    "inspect 1 statue selected.",
    "inspect 2 statues selected.",
    "inspect 3 statues selected.",
    "purloin guest list selected.",
    "seduce target selected.",
    "swap statue selected.",
    "transfer microfilm selected."
}
setup_mission_enabled = {
    "bug ambassador enabled.",
    "contact double agent enabled.",
    "fingerprint ambassador enabled.",
    "inspect 1 statue enabled.",
    "inspect 2 statues enabled.",
    "inspect 3 statues enabled.",
    "purloin guest list enabled.",
    "seduce target enabled.",
    "swap statue enabled.",
    "transfer microfilm enabled."
}
setup_events = setup_role_cast | setup_mission_enabled | setup_mission_selected
