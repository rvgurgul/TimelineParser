from Classes.Parsers.Parser import Parser


class FlirtPair(Parser):

    def __init__(self, game):
        Parser.__init__(self, "Flirt Pair")
        self.results = (game.get_characters_in_role("Spy"), game.get_characters_in_role("SeductionTarget"))
