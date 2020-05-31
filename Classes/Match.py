

class MatchMaker:
    def __init__(self):
        self.matches = {}
        # format:
        #   MATCH: [
        #       game1, game2, ...
        #   ]

    def add(self, game):
        if game.match in self.matches:
            self.matches[game.match].append(game)
        else:
            self.matches[game.match] = [game]


class Match:
    def __init__(self, jason):
        self.event = jason["event"]
        div = jason["division"]
        self.division = "" if div is None else div if len(div) > 1 else "Group "+div
        self.week = jason["week"]
        self.playerA, self.playerB = sorted([jason["spy"], jason["sniper"]])

    def __str__(self):
        return f"{self.event} {self.division} Week {self.week}: {self.playerA} vs {self.playerB}"

    def __hash__(self):
        return hash(str(self))
