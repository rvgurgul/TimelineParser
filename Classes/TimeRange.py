from math import inf

class TimeRange:

    def __init__(self, lower: float, upper: float):
        self.lb = -inf if lower is None else lower
        self.ub = inf if upper is None else upper

    def is_inverted(self):
        return self.ub > self.lb

    def to_list(self, steps: int = 1, include_right: bool = False):
        steps = max(1, steps)
        delta = len(self) / steps * bool_to_parity(self.is_inverted())
        return [self.lb + delta * i for i in range(steps + include_right)]

    def __len__(self):
        return abs(self.ub - self.lb)

    def __contains__(self, item: float):
        return self.lb <= item <= self.ub

    def __str__(self):
        return f"[{self.lb}, {self.ub}]" if self.is_inverted() else f"(-inf, {self.ub})U({self.lb}, +inf)"

    def __repr__(self):
        return str(self)


def bool_to_parity(boolean):
    return 1 if boolean else -1
    # return (boolean + 1) * -1
