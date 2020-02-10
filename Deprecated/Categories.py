
def by_spy_player(jason):
    return jason["spy"]


def by_sniper_player(jason):
    return jason["sniper"]


def by_division(jason):
    from Helpers import get_division_detail
    return get_division_detail(jason)


def by_venue(jason):
    return jason["venue"]


def by_spy_venue(jason):
    return jason["spy"], jason["venue"]


def by_sniper_venue(jason):
    return jason["sniper"], jason["venue"]


def by_venue_result(jason):
    from Helpers import get_specific_win_condition
    return jason["venue"], get_specific_win_condition(jason["win_type"])


def by_division_venue(jason):
    from Helpers import get_division_detail
    return get_division_detail(jason), jason["venue"]


def by_venue_role(jason, player=""):
    if player == jason["spy"]:
        return jason["venue"], "Spy"
    if player == jason["sniper"]:
        return jason["venue"], "Sniper"


def by_division_venue_result(jason):
    from Helpers import get_division_detail, get_specific_win_condition
    return get_division_detail(jason), jason["venue"], get_specific_win_condition(jason["win_type"])


def by_char_spy(jason):
    from Helpers import get_characters_of_role
    return get_characters_of_role(jason, "Spy")


def by_char_st(jason):
    from Helpers import get_characters_of_role
    return get_characters_of_role(jason, "SeductionTarget")


def by_char_amba(jason):
    from Helpers import get_characters_of_role
    return get_characters_of_role(jason, "Ambassador")


def by_char_rda(jason):
    from Helpers import get_characters_of_role
    return get_characters_of_role(jason, "DoubleAgent")


def by_missions_completed(jason):
    return tuple(jason["completed_missions"])

