import json
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np


def bar_chart(values, sort_by=None, title="", x_lab="", y_lab=""):
    ctr = Counter(values)
    if sort_by == 'keys':
        pairs = sorted((k, ctr[k]) for k in ctr)
        x, y = [pair[0] for pair in pairs], [pair[1] for pair in pairs]
        plt.bar(x, y)
    elif sort_by == 'vals':
        pairs = sorted((ctr[k], k) for k in ctr)
        x, y = [pair[1] for pair in pairs], [pair[0] for pair in pairs]
        plt.bar(x, y)
        # plt.xticks(np.arange(min(x), max(x), 1.0))
    else:
        plt.bar(ctr.keys(), ctr.values())
    plt.title(title)
    plt.xlabel(x_lab)
    plt.ylabel(y_lab)
    plt.show()


# TODO build functionality to dump parsed statistics to a json file

# TODO build functionality to analyze the results of parsed games
def getJSON(jason):
    return jason


# with open('data.json', 'w') as f:
#     json.dump(data, f)

# y = json.dumps(x, indent=4)
# print(y)
