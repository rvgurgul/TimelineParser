from json import load
from datetime import datetime

class StatLoader:
    __instance__ = None

    def __init__(self):
        if StatLoader.__instance__ is None:  # Singleton design paradigm
            StatLoader.__instance__ = {}
        self.stat_dict = StatLoader.__instance__

    def get_stat(self, stat, verbose=True):
        if not stat.startswith("json_outputs/"):
            stat = f"json_outputs/{stat}"
        if not stat.endswith(".json"):
            stat += ".json"
        try:
            if stat not in self.stat_dict:
                before = datetime.now()
                with open(stat, "r") as f:
                    if verbose: print(f"Loading {stat} for the first time...", end="")
                    self.stat_dict[stat] = load(f)
                    if verbose: print(f"done (took {datetime.now() - before})")
            return self.stat_dict[stat]
        except:
            print(f"Loading {stat} failed...")
