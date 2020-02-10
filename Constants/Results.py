specific_win_conditions = {
    "SpyShot",
    "MissionsWin",
    "CivilianShot",
    "TimeOut"
}

general_win_conditions = {
    "SpyWin",
    "SniperWin"
}

shot_win_conditions = {
    "CivilianShot",
    "SpyShot"
}
hold_win_conditions = specific_win_conditions - shot_win_conditions
