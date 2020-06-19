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

def pie_chart(counts, title="", x_lab="", y_lab="", sample_size=True):
    y = [float(v) for v in counts.values()]
    plt.pie(y, labels=counts.keys(), autopct=None)
    if sample_size:
        title = f"{title} (N={sum(y)})"
    plt.title(title)
    plt.xlabel(x_lab)
    plt.ylabel(y_lab)
    plt.show()

class Dataset:
    def __init__(self, vals):
        self.size = len(vals)
        if self.size == 0:
            raise Exception("Empty data set")
        self.vals = sorted(vals)
        self.counts = Counter(self.vals)

    def sample_size(self):
        return self.size

    def minimum(self):
        return self.vals[0]

    def median(self):
        return self.vals[self.size//2]

    def mode(self, n=1):
        return self.counts.most_common(n)

    def maximum(self):
        return self.vals[-1]

    def average(self):
        return average(self.vals)

    def binned_average(self, bins=3):
        delta = self.size//bins
        return [sum(self.vals[delta * i:delta * (i + 1)]) / delta for i in range(bins)]

    def stats_report(self, rounding=2):
        categories = {
            "SIZE": self.sample_size,
            "MIN": self.minimum,
            "MED": self.median,
            "AVG": self.average,  # TODO returns list of tuples..
            # "MODE": self.mode,
            "MAX": self.maximum,
            # "Lo/Med/Hi": self.binned_average,  # TODO returns list which can't be rounded
        }
        for cat in categories:
            result = categories[cat]()
            print(f"{cat.rjust(5)}: {round(result, rounding)}")

def average(array, rounding=2):
    return round(sum(array) / len(array), rounding)

def number_to_grade(percent):
    beg_dig = percent // 10
    end_dig = percent % 10
    return "%s%s" % (
        "F" if beg_dig < 6 else "D" if beg_dig < 7 else "C" if beg_dig < 8 else "B" if beg_dig < 9 else "A",
        "-" if end_dig < 4 else "+" if end_dig > 6 else ""
    )
