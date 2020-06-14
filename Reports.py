import matplotlib.pyplot as plt
from collections import Counter

def bar_chart(counts, sort_by=None, title="", x_lab="", y_lab="", sample_size=True):
    # todo cast keys to string
    # fixme rotate long x-axis strings
    if sort_by == 'vals':
        pairs = counts.most_common()
        x, y = [pair[0] for pair in pairs], [pair[1] for pair in pairs]
        plt.bar(x, y)
    elif sort_by == 'keys':
        pairs = sorted(counts.items(), key=lambda k: k[0])
        x, y = [pair[0] for pair in pairs], [pair[1] for pair in pairs]
        plt.bar(x, y)
    else:
        x, y = counts.keys(), counts.values()
        plt.bar(x, y)
    if sample_size:
        title += f" (N={sum(y)})"
    # if len(x[0]) > 3:
    #     plt.xticks(rotation=25)
    plt.title(title)
    plt.xlabel(x_lab)
    plt.ylabel(y_lab)
    plt.show()
    # TODO relocate charts/graphs into dataset

class Dataset:
    def __init__(self, vals):
        self.size = len(vals)
        if self.size == 0:
            raise Exception("Empty data set")
        self.vals = sorted(vals)

    def sample_size(self):
        return self.size

    def minimum(self):
        return self.vals[0]

    def median(self):
        return self.vals[self.size//2]

    def mode(self, n=1):
        return Counter(self.vals).most_common(n)

    def maximum(self):
        return self.vals[-1]

    def average(self):
        return sum(self.vals)/self.size

    def binned_average(self, bins=3):
        delta = self.size//bins
        return [sum(self.vals[delta * i:delta * (i + 1)]) / delta for i in range(bins)]

    def stats_report(self, rounding=2):
        categories = {
            "SIZE": self.sample_size,
            "MIN": self.minimum,
            "MAX": self.maximum,
            "MED": self.median,
            "AVG": self.average,
            "Hi/Med/Lo": self.binned_average,
        }
        for cat in categories:
            print(f"{cat.rjust(12)}: {round(categories[cat](), rounding)}")

