

def binned_average(arr, bins=3, rounding=2):
    delta = len(arr)//bins
    ordered = sorted(arr)
    return [round(avg(ordered[delta*i:delta*(i+1)]), rounding) for i in range(bins)]


def median(arr):
    return sorted(arr)[len(arr)//2]


def avg(arr):
    return 0 if len(arr) == 0 else sum(arr)/len(arr)


DEFAULT_DUMP_STATISTICS = {
    "Size:\t\t\t": len,
    "Average:\t\t": avg,
    "Minimum:\t\t": min,
    "Maximum:\t\t": max,
    "Median:\t\t\t": median,
    "Low/Med/High:\t": binned_average
}


def statistic_dump(arr, funcs=None, rounding=2):
    if funcs is None:
        funcs = DEFAULT_DUMP_STATISTICS
    if type(funcs) is dict:
        for name in funcs:
            value = funcs[name](arr)
            if type(value) is float:
                value = round(value, rounding)
            print(name, value)
    elif type(funcs) is list or type(funcs) is tuple:
        for func in funcs:
            value = func(arr)
            if type(value) is float:
                value = round(value, rounding)
            print(value)

