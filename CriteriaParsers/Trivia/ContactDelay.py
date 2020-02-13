from Classes.Parser import Parser


class ContactFudge(Parser):

    def __init__(self, game):
        Parser.__init__(self, "Contact Delay")
        if "Contact" not in game.missions_complete:
            self.complete = True
        else:
            self.rbbts = 0

    def parse(self, event):
        if self.complete:
            return

        if event == "banana bread uttered.":
            if self.rbbts > 0:
                print("WEE WOO")
            self.rbbts = event.time
        elif event == "double agent contacted.":
            self.results = round(event.time-self.rbbts, 1)
            self.complete = True

# Querying games, please wait...
# 0%                     25%                      50%                      75%                     100%
# |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
# Queried 13476 games:
#  Accepted 13476 games (100.0%)
# WEE WOO
# WEE WOO
# WEE WOO
# WEE WOO
# WEE WOO
# WEE WOO
# WEE WOO
# WEE WOO
# WEE WOO
# WEE WOO
# WEE WOO
# WEE WOO
# WEE WOO
# WEE WOO
# WEE WOO
# WEE WOO
# WEE WOO
# WEE WOO
# WEE WOO
# None
# 4737x	(53.27%)	0.5
# 3864x	(43.45%)	0.6
# 77x		 (0.87%)	0.4
# 47x		 (0.53%)	1.2
# 46x		 (0.52%)	1.1
# 41x		 (0.46%)	1.3
# 34x		 (0.38%)	1.0
# 17x		 (0.19%)	1.4
# 15x		 (0.17%)	0.7
# 9x		 (0.1%)	0.9
# 3x		 (0.03%)	0.8
# 1x		 (0.01%)	91.0
# 1x		 (0.01%)	75.7
# 1x		 (0.01%)	0.3
